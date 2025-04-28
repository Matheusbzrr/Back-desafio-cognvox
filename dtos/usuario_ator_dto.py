from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
import re

class UsuarioAtorDTO(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    senha: str = Field(..., min_length=8)
    nome: str = Field(..., min_length=3, max_length=100)
    email: str
    cod_empresa: int
    cod_grupo_usuario: int
    
    telefone_celular: Optional[str] = None
    telefone_fixo: Optional[str] = None
    data_nascimento: date
    data_inicio_intervencao: date
    reg_profissional: Optional[str] = None
    unidade: int
    idioma_id: int
    profissao_id: int
    modalidade_ensino_id: int
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = None
    foto: Optional[str] = None
    ano_sessao: int

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$'
        if not re.match(pattern, v):
            raise ValueError('A senha deve ter pelo menos 8 caracteres, incluir letras minúsculas, maiúsculas, números e caracteres especiais.')
        return v

    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, v):
            raise ValueError('Email inválido.')
        return v
