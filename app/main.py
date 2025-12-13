from app.core.database import Base, engine
from app.models import user, sweet
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User


app = FastAPI(title="Sweet Shop Management System")
Base.metadata.create_all(bind=engine)


class RegisterRequest(BaseModel):
    email: str
    password: str
    is_admin: bool = False


class RegisterResponse(BaseModel):
    id: int
    email: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/auth/register", status_code=201, response_model=RegisterResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        is_admin=payload.is_admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email
    }
