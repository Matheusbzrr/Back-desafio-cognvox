import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def criar_schema_se_nao_existir():
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')

    conexao = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password
    )
    
    with conexao.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    
    conexao.commit()
    conexao.close()