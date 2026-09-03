from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.models.personal_trainer import PersonalTrainer
from app.models.aluno import Aluno


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def criar_usuario(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def criar_personal_trainer(self, personal: PersonalTrainer) -> PersonalTrainer:
        self.db.add(personal)
        self.db.commit()
        self.db.refresh(personal)
        return personal

    def criar_aluno(self, aluno: Aluno) -> Aluno:
        self.db.add(aluno)
        self.db.commit()
        self.db.refresh(aluno)
        return aluno

    def buscar_personal_por_id(self, personal_id) -> PersonalTrainer | None:
        return self.db.query(PersonalTrainer).filter(PersonalTrainer.id == personal_id).first()
