from flask import Flask, request, jsonify
# - 'request para ler o que o front fala
# - 'jsonify para responder em json para o front

app = Flask(__name__) # cria uma instancia da aplicação web
## '__name__' é uma variável especial do Python que representa o nome do módulo atual.


tarefas = [] # lista para armazenar as tarefas
contador_id = 1 # Para gerar IDs unicos
## Refatorar mais tarde para adicionar SQLite

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'mensagem': 'API TaskFlow funcionando!',
        'versao': '1.0 MVP',
        'endpoints_disponiveis': [
            'GET /tarefas - Listar todas',
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

@app.route('/tarefas', methods=['GET'])  # -> define a rota para listar tarefas
def listar_tarefas():
    return jsonify(tarefas) # retorna a lista de tarefas em formato JSON
# - Quando alguem fizer get em /tarefas, retornamos a lista inteira.
# - O jsonify converte a automaticamente a lista Python em JSON

@app.route('/tarefas', methods=['POST']) # -> define a rota para criar nova tarefa
def criar_tarefa():
    global contador_id # precisamos dizer que vamos modificar a variável global contador_id
    dados = request.get_json() # request.get_json() pega os dados que o front enviou

    # Validação básica: título é obrigatório
    if not dados or 'titulo' not in dados:
        return jsonify({'erro': 'Título é obrigatório!'}), 400
    # - Se os dados forem nulos ou não tiverem a chave 'titulo', retornamos um erro 400 (Bad Request)
    # - 400 = Bad Request (erro do cliente)

    # Criar a nova tarefa
    nova_tarefa = {
        'id': contador_id, # Atribui o ID atual
        'titulo': dados['titulo'], # Pega o título do JSON enviado
        'descricao': dados.get('descricao', ''), # Se nao tiver descriçai, string vazia
        'concluida': False, # Tarefa nova começa nçao concluída
        'data_criacao': '2026-01-01' # Drpois usaremos data real 
    }

    tarefas.append(nova_tarefa) # Adiciona a nova tarefa na lista 
    contador_id += 1 # Incrementa o contador para a próxima taref
    return jsonify(nova_tarefa), 201 # Retorna a tarefa criada com o codigo 201 (Created)



# Atualizar tarefa (PUT)
@app.route('/tarefas/<int:id>', methods=['PUT']) # -> define a rota para atualizar tarefa
def atualizar_tarefa(id):
    # O <int:id> na rota captura o ID da URL
    # Ex: PUT /tarefas/3 -> id = 3

    # Procura a tarefa na lista
    tarefa_encontrada = None
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefa_encontrada = tarefa
            break

    #Se nao encontrou, retorna 404
    if not tarefa_encontrada:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    # Pega os dados enviados
    dados = request.get_json()

# Atualiza apenas os campos enviados
    if 'titulo' in dados:
        tarefa_encontrada['titulo'] = dados['titulo']
    if 'descricao' in dados:
        tarefa_encontrada['descricao'] = dados['descricao']
    if 'concluida' in dados:
        tarefa_encontrada['concluida'] = dados['concluida']

    return jsonify(tarefa_encontrada) # Retorna a tarefa atualizada 


# Aqui, o PUT é usado para atualizar uma tarefa existente.
# O ID da tarefa a ser atualizada é passado na URL.
# A função procura a tarefa na lista, e se encontrada, 
# atualiza os campos que foram enviados no JSON. Se a tarefa não for encontrada, 
# retorna um erro 404 (Not Found).

# Deletar tarefa (DELETE)
@app.route('/tarefas/<int:id>', methods=['DELETE']) # -> define a rota para deletar tarefa
def deletar_tarefa(id):
    global tarefas # Vamos modificar a lista

    # Filtra a lista mantendo só as tarefas com ID diferente
    tarefas_originais = len(tarefas) # Guarda o tamanho original para verificar se deletou algo
    tarefas = [tarefa for tarefa in tarefas if tarefa['id'] != id] # - Cria uma nova lista com todas as tarefas exceto a que tem o ID que queremos deletar

    # Se o tamanho não mudou, é porque não encontrou
    if len(tarefas) == tarefas_originais:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    
    return jsonify({'mensagem': 'Tarefa deletada com sucesso!'}) # Retorna mensagem de sucesso


# Explicação da magia
# [tarefa for tarefa in tarefas id tarefa['id'] != id] 
# Isso é uma 'list comprehension' - forma compacta de criar listas
# Equivalente a: 
# nova_lista = []
# for tarefa in tarefas:
#     if tarefa['id'] != id:
#         nova_lista.append(tarefa)
# tarefas = nova_lista


if __name__ == '__main__':
    print("=" * 50)
    print("     TaskFlow API - Modo Desenvolvimento")
    print("     Endpoints disponíveis:")
    print("     GET      /")
    print("     GET      /tarefas")
    print("     POST     /tarefas")
    print("     PUT      /tarefas/<int:id>")
    print("     DELETE   /tarefas/<int:id>")
    print("=" * 50)
    app.run(debug=True, port=5000) # Inicia a aplicação Flask em modo debug (recarrega

    # if __name__ == '__main__' significa:
    # Se este arquivo foi executado diretamente (não importado, faça isso)
    # app.run(debug=True) -> debug=True faz o servidor reiniciar automaticamente quando mudamos o codigo
    # port=5000 -> roda na porta 5000 (Padrao do Flask)