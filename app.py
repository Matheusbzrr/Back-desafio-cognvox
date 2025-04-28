from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_migrate import upgrade
from dotenv import load_dotenv
from config import Config
from database.db import db
from routes.auth_routes import auth_bp
from routes.usuario_ator_routes import usuario_bp
from routes.referenciais_routes import referenciais_bp
from utils.criar_schema import criar_schema_se_nao_existir
from utils.send_referenciais import send_referenciais
from utils.send_usuario_admin import send_usuario_admin
from flasgger import Swagger
from flask_cors import CORS

load_dotenv()

criar_schema_se_nao_existir()

app = Flask(__name__)
app.config.from_object(Config) 

CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"])

db.init_app(app)
migrate = Migrate(app, db)


jwt = JWTManager(app)

app.config["JWT_HEADER_TYPE"] = "Bearer"
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API COGNVOX",
        "description": "Documentação da API para gestão de usuários e atores. Para utilizar, coloque a palavra Bearer seguida do seu token no campo de Authorize.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Coloque seu token aqui no formato: Bearer <token>"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger = Swagger(app, template=swagger_template)


app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(referenciais_bp, url_prefix='/api')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        upgrade() 
        send_referenciais()
        send_usuario_admin()
    app.run(debug=True, host="0.0.0.0", port=5000)
