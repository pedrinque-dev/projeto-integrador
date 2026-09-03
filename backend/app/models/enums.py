import enum

class TipoUsuario(str, enum.Enum):
    PERSONAL = "personal"
    ALUNO = "aluno"
