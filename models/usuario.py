import uuid
import bcrypt
from database.db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.LargeBinary(60), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    cod_empresa = db.Column(db.Integer, db.ForeignKey('instituicao.id'), nullable=False, index=True)
    cod_status = db.Column(db.Integer, nullable=False, default=1)
    cod_grupo_usuario = db.Column(db.Integer, db.ForeignKey('grupo_acessos.id'), nullable=False, index=True)
    cod_nivel = db.Column(db.Integer, nullable=False, default=1)
    primeiro_acesso = db.Column(db.Boolean, nullable=False, default=1)
    erros_login = db.Column(db.Integer, nullable=False, default=0)
    criado_por = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=True)

    def __init__(self, **kwargs):
        senha_pura = kwargs.pop('senha', None) 
        super().__init__(**kwargs)
        if senha_pura:
            self.senha_hash = bcrypt.hashpw(senha_pura.encode('utf-8'), bcrypt.gensalt())

    def verificar_senha(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash)
