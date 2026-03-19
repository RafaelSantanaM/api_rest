# database.py
from flask_sqlalchemy import SQLAlchemy

# Instância do SQLAlchemy (sem app ainda)
db = SQLAlchemy()

# Função para iniciar o banco com o app (será chamada no app.py)
def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all() # Cria as tabelas no banco (se ainda não existirem)