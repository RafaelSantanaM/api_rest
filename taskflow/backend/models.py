# models.py
from database import db
from datetime import datetime

class Tarefa(db.Model):
    __tablename__ = 'tarefas' # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True) # ID auto-incrementável
    titulo = db.Column(db.String(200), nullable=False) # Título obrigatório
    descricao = db.Column(db.Text, default='') # Descrição opcional
    concluida = db.Column(db.Boolean, default=False) # Status de conclusão
    data_criacao = db.Column(db.DateTime, default=datetime.now) # Data de criação
    data_conclusao = db.Column(db.DateTime, nullable=True) # Data de conclusão

    def __repr__(self):
        return f'<Tarefa {self.id} - {self.titulo}>' # Representação da tarefa para facilitar debug e visualização
    
    def to_dict(self):
        """Converte o objeto Tarefa para um dicionário, facilitando a conversão para JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "concluida": self.concluida,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_conclusao": self.data_conclusao.isoformat() if self.data_conclusao else None
        }