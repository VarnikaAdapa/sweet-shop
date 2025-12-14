from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
#from app.core.database import get_db
#from app.models.user import User
#from fastapi.security import OAuth2PasswordBearer
#from fastapi import Depends


pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

MAX_PASSWORD_LENGTH = 72

SECRET_KEY = "super-secret-key"  # fine for assignment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    safe_password = password[:MAX_PASSWORD_LENGTH]
    return pwd_context.hash(safe_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = plain_password[:MAX_PASSWORD_LENGTH]
    return pwd_context.verify(safe_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


