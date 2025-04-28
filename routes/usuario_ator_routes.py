from flask import Blueprint
from controllers.usuario_ator_controller import criar_usuario_e_ator, editar_usuario_e_ator, patch_status_usuario, listar_professores_ativos, listar_responsaveis_ativos, buscar_meu_perfil, listar_usuarios_criados

usuario_bp = Blueprint('usuario_bp', __name__)

usuario_bp.route('/usuario', methods=['POST'])(criar_usuario_e_ator)
usuario_bp.route('/usuario/<string:usuario_id>', methods=['PUT'])(editar_usuario_e_ator)
usuario_bp.route('/usuario/<string:usuario_id>/status', methods=['PATCH'])(patch_status_usuario)
usuario_bp.route('/professores', methods=['GET'])(listar_professores_ativos)
usuario_bp.route('/responsaveis', methods=['GET'])(listar_responsaveis_ativos)
usuario_bp.route('/meuperfil', methods=['GET'])(buscar_meu_perfil)
usuario_bp.route('/atores', methods=['GET'])(listar_usuarios_criados)