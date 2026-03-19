from flask import Flask, request, jsonify
from datetime import datetime
from database import db, init_app
from models import Tarefa
# - 'request para ler o que o front fala
# - 'jsonify para responder em json para o front

app = Flask(__name__) # cria uma instancia da aplicação web
## '__name__' é uma variável especial do Python que representa o nome do módulo atual.

# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db' # Define o caminho do banco de dados SQLite (será criado na raiz do projeto)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa um recurso que não precisamos e que gera um aviso (warning)

# Inicializa o banco de dados com a aplicação
init_app(app)


@app.route('/')
def home():
    return jsonify({
        'mensagem': 'API TaskFlow com bando de dados!',
        'versao': '2.0',
        'endpoints_disponiveis': [
            'GET /tarefas - Listar todas',
            'GET /tarefas/statistics - Ver estatísticas',
            'POST /tarefas - Criar nova',
            'PUT /tarefas/<id> - Atualizar',
            'DELETE /tarefas/<id> - Deletar'  
        ]
    })

# ------- EXPLICAÇÃO ----------
# '@app.route' -> é um 'decorador' (função especial que modifica outra função)
# '/' -> é a rota raiz da aplicação (home)
# A função home() será chamada quando alguem acessar a raiz
# 'jsonify() -> converte o dicionario Python em JSON válido
# 
# ' 

# Listar - com filtro opcional
@app.route('/tarefas', methods=['GET'])  # -> define a rota para listar tarefas
def listar_tarefas():
    filtrar_concluidas = request.args.get('concluidas') # Pega o parametro 'concluidas' da URL (ex: /tarefas?concluidas=true
    
    query = Tarefa.query # SELECT * FROM tarefas
    
    if filtrar_concluidas is not None: # Se o parametro foi fornecido
        # Convertendo o valor para booleano ( O python entende 'true' como True e 'false' como False)
        if filtrar_concluidas.lower() == 'true':
            query = query.filter_by(concluida=True) # Filtra só as tarefas concluídas
        elif filtrar_concluidas.lower() == 'false':
            query = query.filter_by(concluida=False) # Filtra só as tarefas não concluídas
        else:
            # Se o valor dor inválido, retorna erro ou losta vazia
            return jsonify({'erro': 'Parâmetro concluídas deve ser true ou false'}), 400
        
    tarefas = query.all() # Executa a consulta e pega os resultados filtrados
    return jsonify([tarefa.to_dict() for tarefa in tarefas]) # Retorna a lista filtrada
# - Quando alguem fizer get em /tarefas, retornamos a lista inteira.
# - O jsonify converte a automaticamente a lista Python em JSON

@app.route('/tarefas/statistics', methods=['GET'])
def statistics():
    total = Tarefa.query.count() # Conta o total de tarefas na lista
    concluidas = Tarefa.query.filter_by(concluida=True).count() # Conta quantas tarefas estão marcadas como concluídas
    pendentes = total - concluidas # O resto são pendentes
    return jsonify({
        'total': total,
        'concluidas': concluidas,
        'pendentes': pendentes
    }) # Retorna um JSON com as estatísticas

# Criar tarefa (POST)
@app.route('/tarefas', methods=['POST']) # -> define a rota para criar nova tarefa
def criar_tarefa():
    dados = request.get_json() # request.get_json() pega os dados que o front enviou


    # Validação básica: título é obrigatório
    if not dados or 'titulo' not in dados:
        return jsonify({'erro': 'Título é obrigatório!'}), 400
    # - Se os dados forem nulos ou não tiverem a chave 'titulo', retornamos um erro 400 (Bad Request)
    # - 400 = Bad Request (erro do cliente)

    if len(dados.get('titulo', '')) < 3: # Validação do tamanho minimo de caracteres
        return jsonify({'erro': 'Título deve ter pelo menos 3 caracteres!'}), 400

    # Criar a nova tarefa
    nova_tarefa = Tarefa(
        titulo=dados['titulo'],
        descricao=dados.get('descricao', ''),
        concluida=False,
        data_criacao=datetime.now().utcnow(),
        data_conclusao=None
    )

    db.session.add(nova_tarefa) # Adiciona a nova tarefa na sessão do banco
    db.session.commit() # Salva as mudanças no banco (executa o INSERT)

    return jsonify({
        'id': nova_tarefa.id,
        'titulo': nova_tarefa.titulo,
        'descricao': nova_tarefa.descricao,
        'concluida': nova_tarefa.concluida,
        'data_criacao': nova_tarefa.data_criacao.isoformat() if nova_tarefa.data_criacao else None,
        'data_conclusao': nova_tarefa.data_conclusao.isoformat() if nova_tarefa.data_conclusao else None
    }), 201 # Retorna a tarefa criada com o codigo 201 (Created)



# Atualizar tarefa (PUT)
@app.route('/tarefas/<int:id>', methods=['PUT']) # -> define a rota para atualizar tarefa
def atualizar_tarefa(id):
    # O <int:id> na rota captura o ID da URL
    # Ex: PUT /tarefas/3 -> id = 3

    # Procura a tarefa na lista
    tarefa = Tarefa.query.get(id) # SELECT * FROM tarefas WHERE id = id LIMIT 1 ( busca por chave primaria)


    #Se nao encontrou, retorna 404
    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    # Pega os dados enviados
    dados = request.get_json()

# Atualiza apenas os campos enviados
    if 'titulo' in dados:
        tarefa.titulo = dados['titulo']
    if 'descricao' in dados:
        tarefa.descricao = dados['descricao']
    if 'concluida' in dados:
        tarefa.concluida = dados['concluida']
        # Se a tarefa foi marcada como concluída, atualiza a data de conclusão
        if dados['concluida'] is True:
            tarefa.data_conclusao = datetime.now().utcnow() # Define a data de conclusão como o momento atual
        else:
            tarefa.data_conclusao = None # Se desmarcar como concluída, remove a data de conclusão

    db.session.commit() # Salva as mudanças no banco (executa o UPDATE)

    return jsonify(tarefa.to_dict()) # Retorna a tarefa atualizada 


# Aqui, o PUT é usado para atualizar uma tarefa existente.
# O ID da tarefa a ser atualizada é passado na URL.
# A função procura a tarefa na lista, e se encontrada, 
# atualiza os campos que foram enviados no JSON. Se a tarefa não for encontrada, 
# retorna um erro 404 (Not Found).

# Deletar tarefa (DELETE)
@app.route('/tarefas/<int:id>', methods=['DELETE']) # -> define a rota para deletar tarefa
def deletar_tarefa(id):
    tarefa = Tarefa.query.get(id) # Busca a tarefa pelo ID
    
    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({'mensagem': 'Tarefa deletada com sucesso!'}) # Retorna mensagem de sucesso


# Explicação da magia
# [tarefa for tarefa in tarefas if tarefa['id'] != id] 
# Isso é uma 'list comprehension' - forma compacta de criar listas
# Equivalente a: 
# nova_lista = []
# for tarefa in tarefas:
#     if tarefa['id'] != id:
#         nova_lista.append(tarefa)
# tarefas = nova_lista


if __name__ == '__main__':
    app.run(debug=True, port=5000) # Inicia a aplicação Flask em modo debug (recarrega

    # if __name__ == '__main__' significa:
    # Se este arquivo foi executado diretamente (não importado, faça isso)
    # app.run(debug=True) -> debug=True faz o servidor reiniciar automaticamente quando mudamos o codigo
    # port=5000 -> roda na porta 5000 (Padrao do Flask)