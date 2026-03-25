// CONFIGURAÇÃO INICIAL

// URL da API
const API_URL = 'http://localhost:5000';

// Elementos do DOM
const tasksList = documents.getElementById('tasksList');
const createBtn = document.getElementById('createBtn');
const taskTitle = document.getElementById('taskTitle');
const taskDesc = document.getElementById('taskDesc');
const statusFilter = document.getElementById('statusFilter');

// Elemenos das estatísticas
const totalEl = document.getElementById('totalTasks');
const completedEl = document.getElementById('completedTasks');
const pendingEl = document.getElementById('pendingTasks');

// Estado atual do filtro
let currentFilter = 'all';


// FUNÇÕES AUXILIARES


// Função para formatar a data
function formatDate(dateString) {
    if (!dateString) return 'Não definida';
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}

// Converte objeto de tarefa para HTML
function renderTaskCard(tarefa) {
    const statusText = tarefa.concluida ? 'Concluída' : 'Pendente';
    const statusClass = tarefa.concluida ? 'completed' : 'pending';
    return `
        <div class="task-card" data-id="${tarefa.id}">
            <div class="task-header">
                <span class="task-title">${escapeHtml(tarefa.titulo)}</span>
                <span class="task-status ${statusClass}">${statusText}</span>
                </div>
                ${tarefa.descricao ? `<p class="task-description">${escapeHtml(tarefa.descricao)}</p>` : ''}
                <div class="task-meta">
                    <span>📅 Criada em: ${formatDate(tarefa.data_criacao)}</span>
                    ${tarefa.data_conclusao ? `<span>✅ Concluída em: ${formatDate(tarefa.data_conclusao)}</span>` : ''}
                    </div>
                    <div class="task-actions>
                        <button class="btn-status" onclick="toggleTaskStatus(${tarefa.id}, ${!tarefa.concluida})">
                            ${tarefa.concluida ? 'Reabrir' : 'Concluir'}
                            </button>
                            <button class="btn-delete" onclick="deleteTask(${tarefa.id})">Excluir</button>
                            </div>
                    </div>
    `; 

}

// Função simples para evitar injeção de HTML (XSS)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// CARREGAR TAREFAS E ESTATÍSTICAS


//Carrega a lista de tarefas conforme o filtro atual
async function loadTask() {  
    tasksList.innerHTML = '<p class="loading">Carregando tarefas...</p>';
    try {
        let url = `${API_BASE}/tarefas`;
        if(currentFilter !== 'all') {
            url += `?concluidas=${currentFilter}`;
        }
        const response = await fetch(url);
        if (!response.ok) throw new Error('Erro ao carregar tarefas');
        const tarefas = await response.json();

        if (tarefas.length === 0) {
            tasksList.innerHTML = '<p class="loading">Nenhuma tarefa encontrada.</p>';
            return;
        }

        tasksList.innerHTML = tarefas.map(renderTaskCard).join('');
    } catch (error) {
        console.error(error);
        tasksList.innerHTML = '<p class="loading">Erro ao carregar tarefas. Verifique se o backend está rodando.</p>';
    }
}

// Carrega as estatísticas
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/tarefas/statistics`);
        if (!response.ok) throw new Error('Erro ao carregar estatísticas');
        const stats = await response.json();
        totalEl.textContent = stats.total;
        completedEl.textContent = stats.concluidas;
        pendingEl.textContent = stats.pendentes;
    } catch (error) {
        console.error(error);
        totalEl.textContent = '?';
        completedEl.textContent = '?';
        pendingEl.textContent = '?';
    }
}


// OPERAÇÕES CRUD


// Criar nova tarefa
async function createTask() {
    const titulo = taskTitle.value.trim();
    const descricao = taskDesc.value.trim();
    
    if (!titulo) {
        alert('O título é obrigatório.');
        return;
    }
    if (titulo.length < 3) {
        alert('O título deve ter pelo menos 3 caracteres.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/tarefas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titulo, descricao })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro ao criar tarefa');
        }
        
        // Limpa formulário
        taskTitle.value = '';
        taskDesc.value = '';
        
        // Recarrega dados
        await loadTasks();
        await loadStats();
    } catch (error) {
        alert(error.message);
    }
}

// Alternar status (concluir/reabrir)
window.toggleTaskStatus = async function(id, concluida) {
    try {
        const response = await fetch(`${API_BASE}/tarefas/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ concluida })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro ao atualizar status');
        }
        
        // Recarrega dados
        await loadTasks();
        await loadStats();
    } catch (error) {
        alert(error.message);
    }
};

// Deletar tarefa
window.deleteTask = async function(id) {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/tarefas/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro ao deletar tarefa');
        }
        
        // Recarrega dados
        await loadTasks();
        await loadStats();
    } catch (error) {
        alert(error.message);
    }
};


// CONFIGURAR FILTRO E CARREGAMENTO INICIAL


// Atualiza o filtro e recarrega
function handleFilterChange() {
    currentFilter = statusFilter.value;
    loadTasks();
}

// Event listeners
createBtn.addEventListener('click', createTask);
statusFilter.addEventListener('change', handleFilterChange);

// Carrega dados iniciais
loadTasks();
loadStats();