from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "c5ee404d03cc7908402421310a89619ce1a16212a47c1ac8e5ae46c13de0e581"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
