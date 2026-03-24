# TaskFlow - Gerenciador de Tarefas com API REST

![TaskFlow Screenshot](link-para-screenshot)

Um gerenciador de tarefas completo com autenticação de usuários e API RESTful.

## 🚀 Tecnologias Utilizadas

### Backend
- Python 3.9+
- Flask (Framework web)
- Flask-SQLAlchemy (ORM)
- SQLite (Banco de dados)
- Flask-CORS (Compartilhamento de recursos)

### Frontend
- HTML5
- CSS3 (Flexbox/Grid)
- JavaScript Vanilla (ES6+)
- Fetch API

## 📋 Funcionalidades

- ✅ Cadastro e autenticação de usuários
- ✅ CRUD completo de tarefas
- ✅ Filtros por status (pendente/andamento/concluída)
- ✅ Prioridades (baixa/média/alta)
- ✅ Categorias personalizadas
- ✅ Dashboard com estatísticas
- ✅ Interface responsiva

## 🛠️ Como executar

### Pré-requisitos
- Python 3.9+
- Git

### Passo a passo

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/taskflow.git
cd taskflow
```

2. Instale as dependências do Backend:
```bash
cd backend 
pip install -r requirements.txt
```

3. Execute o servidor:
```bash
python app.py
```

4. Abra o arquivo frontend/index.html no navegador

## 📚 Endpoints da API
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| **POST** | `/api/usuarios` | Criar usuário |
| **POST** | `/api/login` | Login |
| **GET** | `/api/tarefas?usuario_id=X` | Listar tarefas |
| **POST** | `/api/tarefas` | Criar tarefa |
| **PUT** | `/api/tarefas/{id}` | Atualizar tarefa |
| **DELETE** | `/api/tarefas/{id}` | Deletar tarefa |
| **GET** | `/api/tarefas/estatisticas/{id}` | Estatísticas |


## Autor
Rafael Santana - @RafaelSantanaM