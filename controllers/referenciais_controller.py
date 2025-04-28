from database.db import db
from models.referenciais import Idioma, Instituicao, TipoOuProfissao, ModalidadeEnsino, GrupoAcessos
from flask_jwt_extended import  jwt_required
from flask import request, jsonify
@jwt_required()
def inserir_registros(modelo, nomes):
    try:
        registros = []
        for nome in nomes:
            registro = modelo(nome=nome)
            db.session.add(registro)
            registros.append({
                "nome": registro.nome
            })

        db.session.commit()

        return {
            "mensagem": f"{len(registros)} registros criados com sucesso.",
            "dados": registros
        }, 201

    except Exception as e:
        db.session.rollback()
        return {
            "erro": "Erro ao criar registros.",
            "detalhes": str(e)
        }, 400

@jwt_required()
def listar_referenciais():
    idiomas = Idioma.query.all()
    instituicoes = Instituicao.query.all()
    tipos_ou_profissoes = TipoOuProfissao.query.all()
    modalidades_ensino = ModalidadeEnsino.query.all()
    grupos_acessos = GrupoAcessos.query.all()

    return jsonify({
        "idiomas": [{"id": idioma.id, "nome": idioma.nome} for idioma in idiomas],
        "instituicoes": [{"id": inst.id, "nome": inst.nome} for inst in instituicoes],
        "tipos_ou_profissoes": [{"id": tipo.id, "nome": tipo.nome} for tipo in tipos_ou_profissoes],
        "modalidades_ensino": [{"id": modalidade.id, "nome": modalidade.nome} for modalidade in modalidades_ensino],
        "grupos_acessos": [{"id": grupo.id, "nome": grupo.nome} for grupo in grupos_acessos]
    })