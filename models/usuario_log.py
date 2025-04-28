from database.db import db

class UsuarioLog(db.Model):
    __tablename__ = 'usuario_log'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.String(36), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    cod_status = db.Column(db.Integer, default=1)
    acao = db.Column(db.String(20), nullable=False)  
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    criado_por = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=True)
    
