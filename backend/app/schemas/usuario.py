import uuid
from pydantic import BaseModel, EmailStr

from app.models.enums import TipoUsuario


class PersonalTrainerRegistro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    bio: str | None = None
    especialidade: str | None = None


class AlunoRegistro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: str | None = None
    objetivo: str | None = None
    personal_trainer_id: uuid.UUID | None = None


class UsuarioOut(BaseModel):
    id: uuid.UUID
    nome: str
    email: EmailStr
    tipo: TipoUsuario

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut
