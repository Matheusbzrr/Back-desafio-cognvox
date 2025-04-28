from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
import re

class UsuarioAtorUpdateDTO(BaseModel):
    login: Optional[str] = None
    senha: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    cod_empresa: Optional[int] = None
    cod_grupo_usuario: Optional[int] = None
    data_nascimento: Optional[date] = None
    data_inicio_intervencao: Optional[date] = None
    reg_profissional: Optional[str] = None
    telefone_celular: Optional[str] = None
    telefone_fixo: Optional[str] = None
    idioma_id: Optional[int] = None
    profissao_id: Optional[int] = None
    modalidade_ensino_id: Optional[int] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = None
    foto: Optional[str] = None
    status: Optional[str] = None
    ano_sessao: Optional[int] = None

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v):
        if v:
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$'
            if not re.match(pattern, v):
                raise ValueError('A senha deve ter pelo menos 8 caracteres, incluir minúsculas, maiúsculas, números e caracteres especiais.')
        return v

    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if v:
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, v):
                raise ValueError('Email inválido.')
        return v
