from passlib.context import CryptContext

# bcrypt o'rniga pbkdf2_sha256 ishlatamiz (xatosiz va juda xavfsiz)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Parolni xavfsiz shifrlash (heshlash)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Parolni tekshirish
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)