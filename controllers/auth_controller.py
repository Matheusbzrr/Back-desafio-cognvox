from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.usuario import Usuario

def login():
    """
    Realizar login e obter token JWT
    ---
    tags:
      - Autenticação
    security: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          example:
            login: "admin"
            senha: "Admin@123"
    responses:
      200:
        description: Login realizado com sucesso. Retorna token JWT.
        schema:
          type: object
          properties:
            access_token:
              type: string
      400:
        description: Login ou senha não enviados.
      404:
        description: Usuário não encontrado.
      401:
        description: Senha incorreta.
      500:
        description: Erro interno do servidor.
    """
    dados = request.get_json()

    login = dados.get("login")
    senha = dados.get("senha")

    try:
      if not login or not senha:
        return jsonify({"msg": "Login e senha são obrigatórios."}), 400

      usuario = Usuario.query.filter_by(login=login).first()

      if not usuario:
        return jsonify({"msg": "Usuário não encontrado."}), 404  
    
      if not usuario.verificar_senha(senha):
        return jsonify({"msg": "Senha incorreta."}), 401
    
      access_token = create_access_token(identity=usuario.id)

      return jsonify({
          "access_token": access_token
      }), 200

    except Exception as e:
        return jsonify({"msg": "Erro interno no servidor.", "detalhes": str(e)}), 500


@jwt_required()
def usuarioLogado():
    """
    Buscar informações do usuário logado
    ---
    tags:
      - Usuário
    security:
      - Bearer: []
    responses:
      200:
        description: Dados do usuário logado
        content:
          application/json:
            schema:
              type: object
              properties:
                usuario_id:
                  type: string
                  example: "user_id_simulado"
      401:
        description: Token inválido ou ausente
    """
    try:
        usuario_id = get_jwt_identity()

        usuario = Usuario.query.get(usuario_id)

        if not usuario:
            return jsonify({"msg": "Usuário não encontrado."}), 404

        return jsonify({
            "login": usuario.login,
            "nome": usuario.nome,
            "email": usuario.email
        }), 200
        
    except Exception as e:
        return jsonify({"msg": "Erro ao obter informações do usuário.", "detalhes": str(e)}), 500
    
    



