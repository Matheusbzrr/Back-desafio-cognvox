from flask import Blueprint, request, jsonify
from models.referenciais import Idioma, Instituicao, TipoOuProfissao, ModalidadeEnsino, GrupoAcessos
from database.db import db
from controllers.referenciais_controller import inserir_registros, listar_referenciais  

referenciais_bp = Blueprint('referenciais_bp', __name__)

@referenciais_bp.route('/referenciais', methods=['POST'])
def seed():
    dados = request.get_json()

    tipo = dados.get('tipo')
    nomes = dados.get('nomes')

    if not tipo or not nomes:
        return jsonify({"erro": "Campos 'tipo' e 'nomes' são obrigatórios."}), 400

    modelos = {
        "idioma": Idioma,
        "instituicao": Instituicao,
        "profissao": TipoOuProfissao,
        "modalidade": ModalidadeEnsino,
        "nivel": GrupoAcessos
    }

    modelo = modelos.get(tipo.lower())

    if not modelo:
        return jsonify({"erro": f"Tipo '{tipo}' inválido. Opções válidas: idioma, instituicao, profissao, modalidade, nivel."}), 400

    resposta, status = inserir_registros(modelo, nomes)
    return jsonify(resposta), status

referenciais_bp.route('/referenciais', methods=['GET'])(listar_referenciais)