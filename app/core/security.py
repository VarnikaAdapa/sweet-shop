from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)

MAX_PASSWORD_LENGTH = 72


def hash_password(password: str) -> str:
    # bcrypt has a 72-byte limit; truncate defensively
    safe_password = password[:MAX_PASSWORD_LENGTH]
    return pwd_context.hash(safe_password)
