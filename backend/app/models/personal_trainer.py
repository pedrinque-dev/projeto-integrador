import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class PersonalTrainer(Base):
    __tablename__ = "personal_trainers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), unique=True, nullable=False)
    bio = Column(String(500), nullable=True)
    especialidade = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="personal_trainer")
    alunos = relationship("Aluno", back_populates="personal_trainer")
