# AQUI ESTÁ A MUDANÇA: adicionamos redirect e url_for
from flask import render_template, request, redirect, url_for
import datetime
import holidays
from app.services import scheduler_service

def index():
    """
    Rota principal. Apenas renderiza a página com o formulário de configuração.
    """
    return render_template('index.html')

def gerar_escala():
    """
    Rota que recebe os dados do formulário (método POST).
    Ela coordena o trabalho: chama os serviços para processar os dados
    e gerar a escala, e depois renderiza a página de resultado.
    """
    if request.method == 'POST':
        form_data = request.form
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
    
    # Se o usuário tentar acessar /gerar_escala diretamente, redireciona para a home
    return redirect(url_for('index'))

def init_app(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/gerar_escala', 'gerar_escala', gerar_escala, methods=['GET', 'POST']) # Adicionado GET para o redirecionamento funcionar