import uuid
from database.db import db

class Ator(db.Model):
    __tablename__ = 'atores'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    inicio_intervencao = db.Column(db.Date, nullable=False)
    reg_profissional = db.Column(db.String(50))
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone_celular = db.Column(db.String(20))
    telefone_fixo = db.Column(db.String(20))

    unidade = db.Column(db.Integer, db.ForeignKey('instituicao.id'), nullable=False, index=True)
    idioma_id = db.Column(db.Integer, db.ForeignKey('idiomas.id'), nullable=False, index=True)
    profissao_id = db.Column(db.Integer, db.ForeignKey('tipo_ou_profissoes.id'), nullable=False, index=True)
    modalidade_ensino_id = db.Column(db.Integer, db.ForeignKey('modalidades_ensino.id'), nullable=False, index=True)
    

    endereco = db.Column(db.String(255) )
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    pais = db.Column(db.String(50))
    foto = db.Column(db.Text, )

    status = db.Column(db.Integer, nullable=False, default=1)
    ano_sessao = db.Column(db.String(4), nullable=False)

    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False, unique=True, index=True)  

