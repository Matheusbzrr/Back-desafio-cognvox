"""Criação do log de usuários com triggers

Revision ID: f5e8e1bb0e11
Revises: 
Create Date: 2025-04-26 18:35:53.691463
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = 'f5e8e1bb0e11'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('senha_hash',
               existing_type=mysql.TINYBLOB(),
               type_=sa.LargeBinary(length=60),
               existing_nullable=False)
    op.create_table(
        'usuario_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('usuario_id', sa.String(36), nullable=False),
        sa.Column('login', sa.String(50), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('cod_status', sa.Integer, nullable=True),   
        sa.Column('acao', sa.String(20), nullable=False), 
        sa.Column('data_evento', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    op.execute("""
    CREATE TRIGGER trg_usuario_insert
    AFTER INSERT ON usuarios
    FOR EACH ROW
    INSERT INTO usuario_log (usuario_id, login, email, cod_status, acao)
    VALUES (NEW.id, NEW.login, NEW.email, NEW.cod_status, 'INSERT');
    """)
    
    op.execute("""
    CREATE TRIGGER trg_usuario_update
    AFTER UPDATE ON usuarios
    FOR EACH ROW
    BEGIN
        IF OLD.cod_status <> NEW.cod_status THEN
            INSERT INTO usuario_log (usuario_id, login, email, cod_status, acao)
            VALUES (NEW.id, NEW.login, NEW.email, NEW.cod_status, 'STATUS_CHANGE');
        ELSE
            INSERT INTO usuario_log (usuario_id, login, email, cod_status, acao)
            VALUES (NEW.id, NEW.login, NEW.email, NEW.cod_status, 'UPDATE');
        END IF;
    END;
    """)

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_usuario_insert;")
    op.execute("DROP TRIGGER IF EXISTS trg_usuario_update;")
    op.drop_table('usuario_log')

    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('senha_hash',
               existing_type=sa.LargeBinary(length=60),
               type_=mysql.TINYBLOB(),
               existing_nullable=False)
