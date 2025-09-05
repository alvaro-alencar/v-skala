let grupoIndex = 0;
let localIndex = 0;
let rodizioIndex = 0;

// Funções adicionarGrupo e adicionarLocal (sem alterações)
function adicionarGrupo() {
    grupoIndex++;
    const container = document.getElementById('grupos-container');
    const newGroup = document.createElement('div');
    newGroup.className = 'row align-items-center mb-3';
    newGroup.innerHTML = `
        <div class="col-md-6"><input type="text" name="grupo_nome_${grupoIndex}" class="form-control" placeholder="Nome do Grupo (Ex: Turma 1)" required></div>
        <div class="col-md-5"><input type="number" name="grupo_alunos_${grupoIndex}" class="form-control" placeholder="Nº de Alunos" min="1" required></div>
        <div class="col-md-1"><button type="button" class="btn btn-danger btn-sm" onclick="this.parentElement.parentElement.remove()">X</button></div>
    `;
    container.appendChild(newGroup);
}

function adicionarLocal() {
    localIndex++;
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
            <h6>Regras de Vagas (separe os tipos por vírgula)</h6>
            <div class="row">
                <div class="col-md-6 border-end pe-3"><strong>Dias de Semana</strong><div class="mt-2"><label class="form-label small">Vagas Diurnas:</label><input type="text" name="local_semana_diurno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2"></div><div class="mt-2"><label class="form-label small">Vagas Noturnas:</label><input type="text" name="local_semana_noturno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2"></div></div>
                <div class="col-md-6 ps-3"><strong>Fins de Semana</strong><div class="mt-2"><label class="form-label small">Vagas Diurnas:</label><input type="text" name="local_fds_diurno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2, P2"></div><div class="mt-2"><label class="form-label small">Vagas Noturnas:</label><input type="text" name="local_fds_noturno_${localIndex}" class="form-control form-control-sm" placeholder="Ex: P1, P2"></div></div>
            </div>
        </div>
    `;
    container.appendChild(newLocal);
}


/**
 * NOVA FUNÇÃO PARA ADICIONAR UM PERÍODO DE RODÍZIO
 */
function adicionarRodizio() {
    rodizioIndex++;
    const container = document.getElementById('rodizio-container');
    
    // 1. Coleta os nomes dos grupos e locais já cadastrados
    const gruposInputs = document.querySelectorAll('#grupos-container input[name^="grupo_nome_"]');
    const locaisInputs = document.querySelectorAll('#locais-container input[name^="local_nome_"]');

    let gruposOptions = '';
    gruposInputs.forEach(input => {
        if (input.value) {
            gruposOptions += `<div class="form-check"><input class="form-check-input" type="checkbox" name="rodizio_${rodizioIndex}_grupos" value="${input.value}" id="g-${rodizioIndex}-${input.value}"><label class="form-check-label" for="g-${rodizioIndex}-${input.value}">${input.value}</label></div>`;
        }
    });

    let locaisOptions = '';
    locaisInputs.forEach(input => {
        if (input.value) {
            locaisOptions += `<div class="form-check"><input class="form-check-input" type="checkbox" name="rodizio_${rodizioIndex}_locais" value="${input.value}" id="l-${rodizioIndex}-${input.value}"><label class="form-check-label" for="l-${rodizioIndex}-${input.value}">${input.value}</label></div>`;
        }
    });

    if (!gruposOptions || !locaisOptions) {
        alert("Por favor, cadastre pelo menos um Grupo e um Local antes de adicionar um período de rodízio.");
        return;
    }

    // 2. Cria o HTML para o novo período de rodízio
    const newRodizio = document.createElement('div');
    newRodizio.className = 'card mb-3 bg-light';
    newRodizio.innerHTML = `
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="mb-0">Período de Rodízio ${rodizioIndex}</h6>
                <button type="button" class="btn btn-danger btn-sm" onclick="this.closest('.card').remove()">X</button>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Início do Período:</label>
                    <input type="date" name="rodizio_${rodizioIndex}_inicio" class="form-control" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Fim do Período:</label>
                    <input type="date" name="rodizio_${rodizioIndex}_fim" class="form-control" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label fw-bold">Grupos neste período:</label>
                    ${gruposOptions}
                </div>
                <div class="col-md-6">
                    <label class="form-label fw-bold">Locais neste período:</label>
                    ${locaisOptions}
                </div>
            </div>
        </div>
    `;
    container.appendChild(newRodizio);
}


document.addEventListener('DOMContentLoaded', function() {
    // Adiciona os primeiros campos para facilitar
    adicionarGrupo();
    adicionarLocal();
});