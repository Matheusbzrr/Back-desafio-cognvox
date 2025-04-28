from models.usuario import Usuario
from models.ator import Ator
from database.db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from dtos.usuario_ator_dto import UsuarioAtorDTO
from dtos.update_usuario_ator_dto import UsuarioAtorUpdateDTO
from pydantic import ValidationError

@jwt_required()
def criar_usuario_e_ator():
    """
    Criar novo usuário e ator
    ---
    tags:
      - Usuário
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          example:
            login: "admin2"
            senha: "Admin@123"
            nome: "Administrador do Sistema"
            email: "admin2@email.com"
            cod_empresa: 1
            cod_grupo_usuario: 2
            data_nascimento: "2000-01-01"
            data_inicio_intervencao: "2025-01-01"
            reg_profissional: "ADM-000"
            unidade: 1
            idioma_id: 1
            profissao_id: 13
            modalidade_ensino_id: 180
            endereco: "Rua Exemplo, 123"
            cidade: "Recife"
            estado: "PE"
            pais: "Brasil"
            foto: null
            ano_sessao: 2025
    responses:
      201:
        description: Usuário e ator criados com sucesso.
      422:
        description: Erro de validação dos dados enviados.
      500:
        description: Erro interno inesperado.
    """
    try:
        usuario_id = get_jwt_identity()

        usuario_logado = Usuario.query.get(usuario_id)

        if not usuario_logado:
            return jsonify({"erro": "Usuário não encontrado."}), 404

        permissoes_permitidas = [2, 3, 15, 17, 18]

        if usuario_logado.cod_grupo_usuario not in permissoes_permitidas:
            return jsonify({"erro": "Você não tem permissão para criar novos usuários."}), 403
        dto = UsuarioAtorDTO(**request.get_json())

        novo_usuario = Usuario(
            login=dto.login,
            senha=dto.senha,
            nome=dto.nome,
            email=dto.email,
            cod_empresa=dto.cod_empresa,
            cod_grupo_usuario=dto.cod_grupo_usuario,
            criado_por=usuario_logado.id if dto.cod_grupo_usuario == 4 else None
        )

        db.session.add(novo_usuario)
        db.session.flush()  
        novo_ator = Ator(
            nome=dto.nome,
            data_nascimento=dto.data_nascimento,
            inicio_intervencao=dto.data_inicio_intervencao,
            reg_profissional=dto.reg_profissional,
            email=dto.email,
            telefone_celular=dto.telefone_celular,
            telefone_fixo=dto.telefone_fixo,
            unidade=dto.cod_empresa, 
            idioma_id=dto.idioma_id,
            profissao_id=dto.profissao_id,
            modalidade_ensino_id=dto.modalidade_ensino_id,
            endereco=dto.endereco,
            cidade=dto.cidade,
            estado=dto.estado,
            pais=dto.pais,
            foto=dto.foto,
            ano_sessao=dto.ano_sessao,
            usuario_id=novo_usuario.id
        )

        db.session.add(novo_ator)

        db.session.commit()

        return {
            "mensagem": "Usuário criado com sucesso."
        }, 201

    except ValidationError as ve:
        erros = {error['loc'][0]: error['msg'] for error in ve.errors()}
        return jsonify({
            "erro": "Erro de validação dos dados enviados.",
            "detalhes": erros
        }), 422

    except SQLAlchemyError as se:
        db.session.rollback()
        return jsonify({
            "erro": "Erro ao salvar no banco de dados.",
            "detalhes": str(se.__dict__.get('orig', se))
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "erro": "Erro interno inesperado.",
            "detalhes": str(e)
        }), 500


def atualizar_campos(objeto, dto, campos):
    for campo_modelo, campo_dto in campos.items():
        valor = getattr(dto, campo_dto, None)
        if valor is not None:
            setattr(objeto, campo_modelo, valor)

@jwt_required()
def editar_usuario_e_ator(usuario_id):
    """
    Editar usuário e ator vinculados
    ---
    tags:
      - Usuário
    security:
      - Bearer: []
    parameters:
      - name: usuario_id
        in: path
        required: true
        type: string
        description: ID do usuário a ser editado
      - in: body
        name: body
        required: true
        description: Campos que deseja atualizar
        schema:
          type: object
          example:
            email: "novoeemail@email.com"
            telefone_celular: "81988888888"
    responses:
      200:
        description: Usuário e Ator atualizados com sucesso.
      404:
        description: Usuário ou Ator não encontrado.
      422:
        description: Erro de validação dos dados enviados.
      500:
        description: Erro interno inesperado.
    """
    try:
      
        dto = UsuarioAtorUpdateDTO(**request.get_json())
       
        usuario = Usuario.query.filter_by(id=usuario_id).first()
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado."}), 404

        ator = Ator.query.filter_by(usuario_id=usuario.id).first()
        if not ator:
            return jsonify({"erro": "Ator vinculado ao usuário não encontrado."}), 404

        atualizar_campos(usuario, dto, {
            "login": "login",
            "nome": "nome",
            "email": "email",
            "cod_empresa": "cod_empresa",
            "cod_grupo_usuario": "cod_grupo_usuario"
        })

        if dto.senha:
            usuario.senha = dto.senha

        atualizar_campos(ator, dto, {
            "nome": "nome",
            "data_nascimento": "data_nascimento",
            "inicio_intervencao": "data_inicio_intervencao",
            "reg_profissional": "reg_profissional",
            "email": "email",
            "telefone_celular": "telefone_celular",
            "telefone_fixo": "telefone_fixo",
            "unidade": "cod_empresa",
            "idioma_id": "idioma_id",
            "profissao_id": "profissao_id",
            "modalidade_ensino_id": "modalidade_ensino_id",
            "endereco": "endereco",
            "cidade": "cidade",
            "estado": "estado",
            "pais": "pais",
            "foto": "foto",
            "status": "status",
            "ano_sessao": "ano_sessao"
        })

        db.session.commit()

        return jsonify({
            "mensagem": "Usuário e Ator atualizados com sucesso."
        }), 200

    except ValidationError as ve:
        erros = {error['loc'][0]: error['msg'] for error in ve.errors()}
        return jsonify({
            "erro": "Erro de validação dos dados enviados.",
            "detalhes": erros
        }), 422

    except SQLAlchemyError as se:
        db.session.rollback()
        return jsonify({
            "erro": "Erro ao atualizar no banco de dados.",
            "detalhes": str(se.__dict__.get('orig', se))
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "erro": "Erro interno inesperado.",
            "detalhes": str(e)
        }), 500


@jwt_required()
def patch_status_usuario(usuario_id):
    """
    Inativar usuário e ator vinculados
    ---
    tags:
      - Usuário
    security:
      - Bearer: []
    parameters:
      - name: usuario_id
        in: path
        required: true
        type: string
        description: ID do usuário a ser inativado
    responses:
      204:
        description: Usuário e Ator inativados com sucesso.
      404:
        description: Usuário não encontrado.
      500:
        description: Erro interno inesperado.
    """
    try:
        usuario = Usuario.query.filter_by(id=usuario_id).first()

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado."}), 404

        usuario.cod_status = 2

        ator = Ator.query.filter_by(usuario_id=usuario.id).first()
        if ator:
            ator.status = 2 
        db.session.commit()

        return '', 204

    except SQLAlchemyError as se:
        db.session.rollback()
        return jsonify({
            "erro": "Erro ao atualizar no banco de dados.",
            "detalhes": str(se.__dict__.get('orig', se))
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "erro": "Erro interno inesperado.",
            "detalhes": str(e)
        }), 500
    

@jwt_required()
def listar_professores_ativos():
    try:
        professores = Ator.query.filter(
            Ator.profissao_id == 17,    # profissão professor
            Ator.status != 2            
        ).order_by(Ator.nome).all()

        if not professores:
            return jsonify({"mensagem": "Nenhum professor encontrado."}), 404
        
        resposta = [
            {
                "nome": professor.nome,
                "email": professor.email,
                "telefone_celular": professor.telefone_celular,
                "telefone_fixo": professor.telefone_fixo,
                "unidade": professor.unidade,
                "idioma_id": professor.idioma_id,
                "profissao_id": professor.profissao_id,
                "modalidade_ensino_id": professor.modalidade_ensino_id,
                "endereco": professor.endereco,
                "cidade": professor.cidade,
                "estado": professor.estado,
                "pais": professor.pais,
                "foto": professor.foto
            } for professor in professores
        ]
        
        return jsonify(resposta), 200

    except SQLAlchemyError as se:
        return jsonify({
            "erro": "Erro ao buscar professores.",
            "detalhes": str(se.__dict__.get('orig', se))
        }), 500

    except Exception as e:
        return jsonify({
            "erro": "Erro interno inesperado.",
            "detalhes": str(e)
        }), 500


@jwt_required()
def listar_responsaveis_ativos():
    try:
        responsaveis = Ator.query.filter(
            Ator.profissao_id.notin_([15, 16, 18, 3]),
            Ator.status != 2
        ).order_by(Ator.nome).all()

        if not responsaveis:
            return jsonify({"mensagem": "Nenhum responsável encontrado."}), 404

        resposta = [
            {
                "nome": responsavel.nome,
                "email": responsavel.email,
                "telefone_celular": responsavel.telefone_celular,
                "telefone_fixo": responsavel.telefone_fixo,
                "unidade": responsavel.unidade,
                "idioma_id": responsavel.idioma_id,
                "profissao_id": responsavel.profissao_id,
                "modalidade_ensino_id": responsavel.modalidade_ensino_id,
                "endereco": responsavel.endereco,
                "cidade": responsavel.cidade,
                "estado": responsavel.estado,
                "pais": responsavel.pais,
                "foto": responsavel.foto
            } for responsavel in responsaveis
        ]

        return jsonify(resposta), 200

    except SQLAlchemyError as se:
        return jsonify({
            "erro": "Erro ao buscar responsáveis.",
            "detalhes": str(se.__dict__.get('orig', se))
        }), 500

    except Exception as e:
        return jsonify({
            "erro": "Erro interno inesperado.",
            "detalhes": str(e)
        }), 500
    
@jwt_required()
def buscar_meu_perfil():
    try:
        usuario_id = get_jwt_identity()  

        usuario = Usuario.query.filter_by(id=usuario_id).first()

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado."}), 404

        ator = Ator.query.filter_by(usuario_id=usuario_id).first()

        if not ator:
            return jsonify({"erro": "Ator associado não encontrado."}), 404

        resposta = {
            "login": usuario.login,
            "nome": usuario.nome,
            "email": usuario.email,
            "cod_empresa": usuario.cod_empresa,
            "cod_status": usuario.cod_status,
            "cod_grupo_usuario": usuario.cod_grupo_usuario,
            "id_ator": ator.id,
            "nome_ator": ator.nome,
            "ano_sessao": ator.ano_sessao,
            "data_nascimento": ator.data_nascimento,
            "inicio_intervencao": ator.inicio_intervencao,
            "reg_profissional": ator.reg_profissional,
            "telefone_celular": ator.telefone_celular,
            "telefone_fixo": ator.telefone_fixo,
            "idioma_id": ator.idioma_id,
            "unidade": ator.unidade,
            "profissao_id": ator.profissao_id,
            "modalidade_ensino_id": ator.modalidade_ensino_id,
            "endereco": ator.endereco,
            "cidade": ator.cidade,
            "estado": ator.estado,
            "pais": ator.pais,
            "foto": ator.foto,
            "status_ator": ator.status
        }
        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({"erro": "Erro interno.", "detalhes": str(e)}), 500


@jwt_required()
def listar_usuarios_criados():
    """
    Listar todos os usuários criados pelo usuário logado, incluindo dados de ator
    ---
    tags:
      - Usuário
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de usuários e seus respectivos atores criada com sucesso.
      404:
        description: Nenhum usuário criado encontrado.
      500:
        description: Erro interno inesperado.
    """
    try:
        usuario_id = get_jwt_identity()

        usuarios_criados = Usuario.query.filter_by(criado_por=usuario_id).all()

        if not usuarios_criados:
            return jsonify({"mensagem": "Nenhum usuário criado encontrado."}), 404

        resultado = []
        for usuario in usuarios_criados:
            ator = Ator.query.filter_by(usuario_id=usuario.id).first()

            if ator:
                
                unidade_nome = None
                idioma_nome = None
                profissao_nome = None
                modalidade_nome = None

                if ator.unidade:
                    from models.referenciais import Instituicao
                    unidade = Instituicao.query.get(ator.unidade)
                    unidade_nome = unidade.nome if unidade else None

                if ator.idioma_id:
                    from models.referenciais import Idioma
                    idioma = Idioma.query.get(ator.idioma_id)
                    idioma_nome = idioma.nome if idioma else None

                if ator.profissao_id:
                    from models.referenciais import TipoOuProfissao
                    profissao = TipoOuProfissao.query.get(ator.profissao_id)
                    profissao_nome = profissao.nome if profissao else None

                if ator.modalidade_ensino_id:
                    from models.referenciais import ModalidadeEnsino
                    modalidade = ModalidadeEnsino.query.get(ator.modalidade_ensino_id)
                    modalidade_nome = modalidade.nome if modalidade else None
            else:
                unidade_nome = idioma_nome = profissao_nome = modalidade_nome = None

            resultado.append({
                "usuario": {
                    "id": usuario.id,
                    "login": usuario.login,
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "cod_empresa": usuario.cod_empresa,
                    "cod_grupo_usuario": usuario.cod_grupo_usuario
                },
                "ator": {
                    "id": ator.id if ator else None,
                    "nome": ator.nome if ator else None,
                    "data_nascimento": ator.data_nascimento if ator else None,
                    "reg_profissional": ator.reg_profissional if ator else None,
                    "unidade": unidade_nome,
                    "idioma": idioma_nome,
                    "profissao": profissao_nome,
                    "modalidade_ensino": modalidade_nome,
                    "endereco": ator.endereco if ator else None,
                    "cidade": ator.cidade if ator else None,
                    "estado": ator.estado if ator else None,
                    "pais": ator.pais if ator else None,
                    "foto": ator.foto if ator else None,
                    "ano_sessao": ator.ano_sessao if ator else None,
                    "status": ator.status if ator else None
                }
            })

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro interno inesperado.",
            "detalhes": str(e)
        }), 500