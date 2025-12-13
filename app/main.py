from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sweet Shop Management System")


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
def register_user(payload: RegisterRequest):
    # TEMPORARY implementation (no DB yet)
    return {
        "id": 1,
        "email": payload.email
    }
