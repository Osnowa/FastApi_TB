from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config import Config
import bcrypt

config = Config.from_env()

SECRET_KEY = config.SECRET_KEY  # в реальности из .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


# --- Пароли ---

def hash_password(password: str) -> str:
    '''Шифрование пароля'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверка пароля (расшифровка)'''
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


# --- JWT ---

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None