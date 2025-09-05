// Variáveis para contar quantos grupos e locais já foram adicionados.
// Isso nos ajuda a dar um 'name' único para cada campo novo.
let grupoIndex = 0;
let localIndex = 0;

/**
 * Função para adicionar um novo bloco de campos para um Grupo de Alunos.
 */
function adicionarGrupo() {
    grupoIndex++; // Incrementa o contador
    const container = document.getElementById('grupos-container');
    
    // Cria um novo elemento 'div' para ser o container da linha
    const newGroup = document.createElement('div');
    newGroup.className = 'row align-items-center mb-3'; // Classes do Bootstrap para estilizar
    
    // Define o conteúdo HTML do novo bloco de campos
    newGroup.innerHTML = `
        <div class="col-md-6">
            <input type="text" name="grupo_nome_${grupoIndex}" class="form-control" placeholder="Nome do Grupo (Ex: Turma 1)" required>
        </div>
        <div class="col-md-5">
            <input type="number" name="grupo_alunos_${grupoIndex}" class="form-control" placeholder="Nº de Alunos" min="1" required>
        </div>
        <div class="col-md-1">
            <button type="button" class="btn btn-danger btn-sm" onclick="this.parentElement.parentElement.remove()">X</button>
        </div>
    `;
    // Adiciona o novo bloco de campos ao container na página HTML
    container.appendChild(newGroup);
}

/**
 * Função para adicionar um novo bloco de campos para um Local de Estágio.
 */
function adicionarLocal() {
    localIndex++; // Incrementa o contador
    const container = document.getElementById('locais-container');
    
    const newLocal = document.createElement('div');
    newLocal.className = 'card mb-3';
    
    newLocal.innerHTML = `
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <input type="text" name="local_nome_${localIndex}" class="form-control" placeholder="Nome do Local (Ex: Pronto Socorro)" required>
                <button type="button" class="btn btn-danger btn-sm ms-2" onclick="this.closest('.card').remove()">X</button>
            </div>
            <hr>
            <h6>Regras de Vagas (separe os tipos de vaga por vírgula)</h6>
            <div class="row">
                <div class="col-md-6 border-end pe-3">
                    <strong>Dias de Semana (Seg-Sex)</strong>
                    <div class="mt-2">
                        <label class="form-label small">Vagas Diurnas:</label>
                        <input type="text" name="local_semana_diurno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2">
                    </div>
                    <div class="mt-2">
                        <label class="form-label small">Vagas Noturnas:</label>
                        <input type="text" name="local_semana_noturno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2">
                    </div>
                </div>
                <div class="col-md-6 ps-3">
                    <strong>Fins de Semana (Sáb-Dom)</strong>
                    <div class="mt-2">
                        <label class="form-label small">Vagas Diurnas:</label>
                        <input type="text" name="local_fds_diurno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2, P2">
                    </div>
                    <div class="mt-2">
                        <label class="form-label small">Vagas Noturnas:</label>
                        <input type="text" name="local_fds_noturno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2">
                    </div>
                </div>
            </div>
        </div>
    `;
    container.appendChild(newLocal);
}

// Garante que o script só execute depois que a página HTML inteira for carregada.
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona o primeiro grupo e o primeiro local automaticamente para facilitar o uso.
    adicionarGrupo();
    adicionarLocal();
});