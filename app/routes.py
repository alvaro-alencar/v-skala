from flask import (
    render_template, request, session, Response, 
    redirect, url_for, Blueprint
)
import datetime
import holidays
import io
import csv
from app.services import scheduler_service

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/gerar_escala', methods=['GET', 'POST'])
def gerar_escala():
    if request.method == 'POST':
        form_data = request.form
        session['form_data'] = dict(form_data)

        # Pegamos as datas gerais aqui
        data_inicio_geral = datetime.date.fromisoformat(form_data['data_inicio'])
        data_fim_geral = datetime.date.fromisoformat(form_data['data_fim'])

        config = scheduler_service.parse_form_data(form_data)
        feriados_obj = holidays.country_holidays('BR', subdiv='MG')
        
        # E passamos as datas para a função principal
        escala_bruta, relatorio, todos_alunos = scheduler_service.gerar_escala_completa(
            config, feriados_obj, data_inicio_geral, data_fim_geral
        )
        
        escala_ordenada = sorted(escala_bruta.items())
        
        return render_template('resultado.html', 
                               escala=escala_ordenada, 
                               relatorio=relatorio,
                               alunos_ordenados=sorted(todos_alunos))
    
    return redirect(url_for('main.index'))

@main.route('/exportar')
def exportar_csv():
    form_data = session.get('form_data')
    if not form_data:
        return redirect(url_for('main.index'))

    # Também pegamos as datas aqui para a exportação
    data_inicio_geral = datetime.date.fromisoformat(form_data['data_inicio'])
    data_fim_geral = datetime.date.fromisoformat(form_data['data_fim'])

    config = scheduler_service.parse_form_data(form_data)
    feriados_obj = holidays.country_holidays('BR', subdiv='MG')
    
    # E passamos para a função principal na exportação também
    escala_bruta, _, _ = scheduler_service.gerar_escala_completa(
        config, feriados_obj, data_inicio_geral, data_fim_geral
    )

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['Data', 'Dia da Semana', 'Turno', 'Local', 'Tipo de Vaga', 'Academico'])
    for (data, turno, local), vagas_dict in sorted(escala_bruta.items()):
        dia_semana = data.strftime('%A')
        for tipo, academicos in vagas_dict.items():
            for academico in academicos:
                writer.writerow([data.strftime('%d/%m/%Y'), dia_semana, turno, local, tipo, academico])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=escala_medica.csv"}
    )