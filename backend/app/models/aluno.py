import uuid
from datetime import datetime, date

from sqlalchemy import Column, String, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), unique=True, nullable=False)
    personal_trainer_id = Column(UUID(as_uuid=True), ForeignKey("personal_trainers.id"), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    telefone = Column(String(30), nullable=True)
    objetivo = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="aluno")
    personal_trainer = relationship("PersonalTrainer", back_populates="alunos")
