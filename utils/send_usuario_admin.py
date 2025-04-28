from models.usuario import Usuario
from models.ator import Ator
from models.referenciais import Idioma, Instituicao, TipoOuProfissao, ModalidadeEnsino, GrupoAcessos
from database.db import db

def send_usuario_admin():
    admin_login = "admin"
    admin_email = "admin@email.com"
    admin_senha = "Admin@123"

    existente = Usuario.query.filter_by(login=admin_login).first()
    if existente:
        print("[SEND] Usuário admin já existe.")
        return

    idioma = Idioma.query.filter_by(nome="Português").first()
    instituicao = Instituicao.query.filter_by(nome="COGNVOX").first()
    profissao = TipoOuProfissao.query.filter_by(nome="Outros").first()
    modalidade = ModalidadeEnsino.query.filter_by(nome="MODALIDADE COGNVOX").first()
    nivel = GrupoAcessos.query.filter_by(nome="Administrador").first()

    if not all([idioma, instituicao, profissao, modalidade, nivel]):
        print("[SEND] Não foi possível criar admin: faltam referenciais.")
        return

    try:
        novo_usuario = Usuario(
            login=admin_login,
            senha=admin_senha,
            nome="Administrador do Sistema",
            email=admin_email,
            cod_empresa=instituicao.id,
            cod_grupo_usuario=nivel.id
        )
        db.session.add(novo_usuario)
        db.session.flush()

        novo_ator = Ator(
            nome="Administrador do Sistema",
            data_nascimento="2000-01-01",
            inicio_intervencao="2025-01-01",
            reg_profissional="ADM-000",
            email=admin_email,
            unidade=instituicao.id,
            idioma_id=idioma.id,
            profissao_id=profissao.id,
            modalidade_ensino_id=modalidade.id,
            endereco="",
            cidade="",
            estado="",
            pais="Brasil",
            foto=None,
            ano_sessao="2025",
            usuario_id=novo_usuario.id
        )
        db.session.add(novo_ator)

        db.session.commit()

        print("[SEND] Usuário e Ator admin criados com sucesso.")
    except Exception as e:
        db.session.rollback()
        print(f"[ERRO] Falha ao criar usuário e ator admin: {e}")
