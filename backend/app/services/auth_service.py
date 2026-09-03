from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.models.personal_trainer import PersonalTrainer
from app.models.aluno import Aluno
from app.models.enums import TipoUsuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import PersonalTrainerRegistro, AlunoRegistro
from app.core.security import hash_senha, verificar_senha, criar_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UsuarioRepository(db)

    def registrar_personal(self, dados: PersonalTrainerRegistro) -> tuple[Usuario, str]:
        if self.repo.buscar_por_email(dados.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )

        usuario = Usuario(
            nome=dados.nome,
            email=dados.email,
            senha_hash=hash_senha(dados.senha),
            tipo=TipoUsuario.PERSONAL,
        )
        usuario = self.repo.criar_usuario(usuario)

        personal = PersonalTrainer(
            usuario_id=usuario.id,
            bio=dados.bio,
            especialidade=dados.especialidade,
        )
        self.repo.criar_personal_trainer(personal)

        token = criar_access_token({"sub": str(usuario.id), "tipo": usuario.tipo.value})
        return usuario, token

    def registrar_aluno(self, dados: AlunoRegistro) -> tuple[Usuario, str]:
        if self.repo.buscar_por_email(dados.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )

        if dados.personal_trainer_id:
            personal = self.repo.buscar_personal_por_id(dados.personal_trainer_id)
            if not personal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Personal trainer não encontrado",
                )

        usuario = Usuario(
            nome=dados.nome,
            email=dados.email,
            senha_hash=hash_senha(dados.senha),
            tipo=TipoUsuario.ALUNO,
        )
        usuario = self.repo.criar_usuario(usuario)

        aluno = Aluno(
            usuario_id=usuario.id,
            personal_trainer_id=dados.personal_trainer_id,
            telefone=dados.telefone,
            objetivo=dados.objetivo,
        )
        self.repo.criar_aluno(aluno)

        token = criar_access_token({"sub": str(usuario.id), "tipo": usuario.tipo.value})
        return usuario, token

    def autenticar(self, email: str, senha: str) -> tuple[Usuario, str]:
        usuario = self.repo.buscar_por_email(email)
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )

        token = criar_access_token({"sub": str(usuario.id), "tipo": usuario.tipo.value})
        return usuario, token
