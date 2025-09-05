# Imports necessários: session, Response, redirect, url_for e o módulo io
from flask import render_template, request, session, Response, redirect, url_for
import datetime
import holidays
import io
import csv
from app.services import scheduler_service

def index():
    """Rota principal, renderiza o formulário."""
    return render_template('index.html')

def gerar_escala():
    """
    Recebe os dados do formulário, gera a escala e salva os dados na sessão.
    """
    if request.method == 'POST':
        form_data = request.form
        
        # --- MUDANÇA IMPORTANTE AQUI ---
        # Guardamos uma cópia dos dados do formulário na sessão do usuário.
        # Isso nos permite acessá-los em outras rotas, como a de exportação.
        session['form_data'] = dict(form_data)

        data_inicio = datetime.date.fromisoformat(form_data['data_inicio'])
        data_fim = datetime.date.fromisoformat(form_data['data_fim'])

        config = scheduler_service.parse_form_data(form_data)

        todos_alunos = []
        id_aluno = 1
        for grupo in config['grupos']:
            for _ in range(grupo['alunos']):
                todos_alunos.append(f"{grupo['nome']}_Aluno{id_aluno}")
                id_aluno += 1
        
        feriados_obj = holidays.country_holidays('BR', subdiv='MG')
        vagas = scheduler_service.gerar_vagas_de_plantao(data_inicio, data_fim, config['locais'], feriados_obj)

        escala_bruta, relatorio = scheduler_service.criar_escala_justa(todos_alunos, vagas)
        escala_ordenada = sorted(escala_bruta.items())
        
        return render_template('resultado.html', 
                               escala=escala_ordenada, 
                               relatorio=relatorio,
                               alunos_ordenados=sorted(todos_alunos))
    
    return redirect(url_for('index'))

def exportar_csv():
    """
    Nova rota para gerar e baixar a escala em formato CSV.
    """
    # 1. Pega os dados que guardamos na sessão. Se não houver, volta para a home.
    form_data = session.get('form_data')
    if not form_data:
        return redirect(url_for('index'))

    # 2. Roda a mesma lógica de geração de escala novamente
    data_inicio = datetime.date.fromisoformat(form_data['data_inicio'])
    data_fim = datetime.date.fromisoformat(form_data['data_fim'])
    config = scheduler_service.parse_form_data(form_data)
    todos_alunos = [f"{g['nome']}_Aluno{i+1}" for g in config['grupos'] for i in range(g['alunos'])]
    feriados_obj = holidays.country_holidays('BR', subdiv='MG')
    vagas = scheduler_service.gerar_vagas_de_plantao(data_inicio, data_fim, config['locais'], feriados_obj)
    escala_bruta, _ = scheduler_service.criar_escala_justa(todos_alunos, vagas)

    # 3. Cria o arquivo CSV na memória
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';') # Usando ';' para melhor compatibilidade com Excel no Brasil
    
    # Escreve o cabeçalho
    writer.writerow(['Data', 'Dia da Semana', 'Turno', 'Local', 'Tipo de Vaga', 'Academico'])

    # Escreve os dados da escala
    for (data, turno, local), vagas_dict in sorted(escala_bruta.items()):
        dia_semana = data.strftime('%A') # Nome do dia da semana por extenso
        for tipo, academicos in vagas_dict.items():
            for academico in academicos:
                writer.writerow([data.strftime('%d/%m/%Y'), dia_semana, turno, local, tipo, academico])

    # 4. Prepara a resposta para forçar o download no navegador
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=escala_medica.csv"}
    )

def init_app(app):
    """Registra todas as rotas na aplicação."""
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/gerar_escala', 'gerar_escala', gerar_escala, methods=['GET', 'POST'])
    # --- REGISTRA A NOVA ROTA ---
    app.add_url_rule('/exportar', 'exportar_csv', exportar_csv)