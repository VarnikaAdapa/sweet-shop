from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models import user, sweet
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.core.security import verify_password
#from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.security import create_access_token
from app.models.sweet import Sweet
from typing import List
from app.core.deps import get_current_user
from typing import Optional
from sqlalchemy import and_


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = "super-secret-key"  # later move to env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Sweet Shop Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


class RegisterRequest(BaseModel):
    email: str
    password: str
    is_admin: bool = False


class RegisterResponse(BaseModel):
    id: int
    email: str


class LoginRequest(BaseModel):
    email: str
    password: str

class SweetCreate(BaseModel):
    name: str
    category: str | None = None
    price: float
    quantity: int = 0



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


@app.post("/api/auth/login")
def login_user(payload: LoginRequest, db=Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Temporary fake token (we’ll replace this with real JWT next)
    access_token = create_access_token(
    data={"sub": str(user.id)}
	)

    return {
    "access_token": access_token,
    "token_type": "bearer"
	}



@app.get("/api/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id":current_user.id,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
    }

@app.post("/api/sweets", status_code=201)
def create_sweet(
    payload: SweetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sweet = Sweet(
        name=payload.name,
        category=payload.category,
        price=payload.price,
        quantity=payload.quantity,
    )

    db.add(sweet)
    db.commit()
    db.refresh(sweet)

    return sweet
@app.get("/api/sweets")
def list_sweets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sweets = db.query(Sweet).all()
    return sweets

@app.get("/api/sweets/search")
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))

    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))

    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)

    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    return query.all()


@app.put("/api/sweets/{sweet_id}")
def update_sweet(
    sweet_id: int,
    payload: SweetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    sweet.name = payload.name
    sweet.category = payload.category
    sweet.price = payload.price
    sweet.quantity = payload.quantity

    db.commit()
    db.refresh(sweet)

    return sweet


@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db.delete(sweet)
    db.commit()

    return {"detail": "Sweet deleted"}



@app.post("/api/sweets/{sweet_id}/purchase")
def purchase_sweet(
    sweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")

    sweet.quantity -= 1
    db.commit()
    db.refresh(sweet)

    return {
        "id": sweet.id,
        "quantity": sweet.quantity,
    }


@app.post("/api/sweets/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    quantity: int = 1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity")

    sweet.quantity += quantity
    db.commit()
    db.refresh(sweet)

    return {
        "id": sweet.id,
        "quantity": sweet.quantity,
    }

