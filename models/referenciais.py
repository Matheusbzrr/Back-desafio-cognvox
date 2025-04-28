from database.db import db

class Idioma(db.Model):
    __tablename__ = 'idiomas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

class Instituicao(db.Model):
    __tablename__ = 'instituicao'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

class TipoOuProfissao(db.Model):
    __tablename__ = 'tipo_ou_profissoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

class ModalidadeEnsino(db.Model):
    __tablename__ = 'modalidades_ensino'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

class GrupoAcessos(db.Model):
    __tablename__ = 'grupo_acessos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
