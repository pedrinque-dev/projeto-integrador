from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def criar_access_token(dados: dict) -> str:
    to_encode = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decodificar_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
