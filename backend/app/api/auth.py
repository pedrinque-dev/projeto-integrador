from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.usuario import PersonalTrainerRegistro, AlunoRegistro, TokenOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])


@router.post("/registrar/personal", response_model=TokenOut, status_code=201)
def registrar_personal(dados: PersonalTrainerRegistro, db: Session = Depends(get_db)):
    service = AuthService(db)
    usuario, token = service.registrar_personal(dados)
    return TokenOut(access_token=token, usuario=usuario)


@router.post("/registrar/aluno", response_model=TokenOut, status_code=201)
def registrar_aluno(dados: AlunoRegistro, db: Session = Depends(get_db)):
    service = AuthService(db)
    usuario, token = service.registrar_aluno(dados)
    return TokenOut(access_token=token, usuario=usuario)


@router.post("/login", response_model=TokenOut)
def login(email: str, senha: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    usuario, token = service.autenticar(email, senha)
    return TokenOut(access_token=token, usuario=usuario)
