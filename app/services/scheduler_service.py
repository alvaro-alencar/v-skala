import datetime
import random
from collections import defaultdict

# A função parse_form_data permanece inalterada
def parse_form_data(form):
    config = {'grupos': {}, 'locais': {}, 'rodizios': []}
    
    grupo_nomes = {k: v for k, v in form.items() if k.startswith('grupo_nome_')}
    for key, nome in grupo_nomes.items():
        if not nome: continue
        index = key.split('_')[-1]
        num_alunos = int(form.get(f'grupo_alunos_{index}', 0))
        config['grupos'][nome] = {'alunos': num_alunos}

    local_nomes = {k: v for k, v in form.items() if k.startswith('local_nome_')}
    for key, nome in local_nomes.items():
        if not nome: continue
        index = key.split('_')[-1]
        regras = {
            'semana_diurno': [v.strip() for v in form.get(f'local_semana_diurno_{index}', '').split(',') if v.strip()],
            'semana_noturno': [v.strip() for v in form.get(f'local_semana_noturno_{index}', '').split(',') if v.strip()],
            'fds_diurno': [v.strip() for v in form.get(f'local_fds_diurno_{index}', '').split(',') if v.strip()],
            'fds_noturno': [v.strip() for v in form.get(f'local_fds_noturno_{index}', '').split(',') if v.strip()]
        }
        config['locais'][nome] = {'regras': regras}

    rodizio_inicios = {k: v for k, v in form.items() if k.startswith('rodizio_') and k.endswith('_inicio')}
    for key, inicio_str in rodizio_inicios.items():
        index = key.split('_')[1]
        fim_str = form.get(f'rodizio_{index}_fim')
        grupos_no_rodizio = form.getlist(f'rodizio_{index}_grupos')
        locais_no_rodizio = form.getlist(f'rodizio_{index}_locais')
        
        if inicio_str and fim_str and grupos_no_rodizio and locais_no_rodizio:
            config['rodizios'].append({
                'inicio': datetime.date.fromisoformat(inicio_str),
                'fim': datetime.date.fromisoformat(fim_str),
                'grupos': grupos_no_rodizio,
                'locais': locais_no_rodizio
            })
            
    return config

# A função gerar_escala_completa é a que vamos modificar
def gerar_escala_completa(config, feriados_obj, data_inicio_geral, data_fim_geral):
    """
    Atualizado para lidar com o caso de nenhum rodízio ser especificado.
    """
    escala_final_agrupada = {}
    relatorio_final_agrupado = defaultdict(lambda: defaultdict(int))

    # --- LÓGICA DE INTELIGÊNCIA ADICIONADA AQUI ---
    # Verifica se o gestor cadastrou algum período de rodízio.
    if not config['rodizios']:
        # Se não cadastrou, criamos um "rodízio padrão" usando todos os dados.
        todos_grupos = list(config['grupos'].keys())
        todos_locais = list(config['locais'].keys())
        
        # Só prossegue se houver pelo menos um grupo e um local cadastrado
        if todos_grupos and todos_locais:
            config['rodizios'].append({
                'inicio': data_inicio_geral,
                'fim': data_fim_geral,
                'grupos': todos_grupos,
                'locais': todos_locais
            })
    # -------------------------------------------------

    # O resto da lógica continua a mesma, operando sobre a lista de rodízios
    # (seja a que o usuário criou, ou a nossa padrão).
    alunos_por_grupo = {}
    aluno_id_global = 1
    for nome_grupo, info_grupo in config['grupos'].items():
        alunos_por_grupo[nome_grupo] = []
        for _ in range(info_grupo['alunos']):
            alunos_por_grupo[nome_grupo].append(f"{nome_grupo}_Aluno{aluno_id_global}")
            aluno_id_global += 1

    for rodizio in config['rodizios']:
        alunos_do_periodo = []
        for nome_grupo in rodizio['grupos']:
            if nome_grupo in alunos_por_grupo:
                alunos_do_periodo.extend(alunos_por_grupo[nome_grupo])

        locais_do_periodo = []
        for nome_local in rodizio['locais']:
            if nome_local in config['locais']:
                locais_do_periodo.append({'nome': nome_local, **config['locais'][nome_local]})
        
        if not alunos_do_periodo or not locais_do_periodo:
            continue

        vagas_do_periodo = gerar_vagas_de_plantao(rodizio['inicio'], rodizio['fim'], locais_do_periodo, feriados_obj)
        escala_parcial, relatorio_parcial = criar_escala_justa(alunos_do_periodo, vagas_do_periodo)
        
        escala_final_agrupada.update(escala_parcial)
        for aluno, contagens in relatorio_parcial.items():
            for categoria, valor in contagens.items():
                relatorio_final_agrupado[aluno][categoria] += valor
    
    todos_alunos = [aluno for sublist in alunos_por_grupo.values() for aluno in sublist]
    return escala_final_agrupada, relatorio_final_agrupado, todos_alunos


# As outras funções (gerar_vagas_de_plantao, criar_escala_justa) permanecem inalteradas
def gerar_vagas_de_plantao(data_inicio, data_fim, locais, feriados_obj):
    vagas_a_preencher = []
    data_atual = data_inicio
    while data_atual <= data_fim:
        dia_da_semana = data_atual.weekday()
        eh_fds_ou_feriado = dia_da_semana >= 5 or data_atual in feriados_obj
        for local in locais:
            regras = local['regras']
            regras_dia = regras['fds_diurno'] if eh_fds_ou_feriado else regras['semana_diurno']
            regras_noite = regras['fds_noturno'] if eh_fds_ou_feriado else regras['semana_noturno']
            for tipo_vaga in regras_dia:
                categoria = f"DIURNO_{'FDS' if eh_fds_ou_feriado else 'SEMANA'}_{local['nome']}_{tipo_vaga}"
                vagas_a_preencher.append({'data': data_atual, 'turno': 'Diurno', 'local': local['nome'], 'tipo_vaga': tipo_vaga, 'categoria': categoria})
            for tipo_vaga in regras_noite:
                categoria = f"NOTURNO_{'FDS' if eh_fds_ou_feriado else 'SEMANA'}_{local['nome']}_{tipo_vaga}"
                vagas_a_preencher.append({'data': data_atual, 'turno': 'Noturno', 'local': local['nome'], 'tipo_vaga': tipo_vaga, 'categoria': categoria})
        data_atual += datetime.timedelta(days=1)
    return vagas_a_preencher

def criar_escala_justa(alunos, vagas):
    if not alunos or not vagas: return {}, {}
    vagas_por_categoria = defaultdict(list)
    for vaga in vagas: vagas_por_categoria[vaga['categoria']].append(vaga)
    escala_final = defaultdict(lambda: defaultdict(list))
    conflitos = defaultdict(set)
    contagem_por_aluno = {aluno: defaultdict(int) for aluno in alunos}
    alunos_ciclicos = {cat: random.sample(alunos, len(alunos)) for cat in vagas_por_categoria}
    indice_aluno = defaultdict(int)
    for categoria, lista_vagas in vagas_por_categoria.items():
        for vaga in lista_vagas:
            alocado = False
            for _ in range(len(alunos)):
                idx_atual = indice_aluno[categoria]
                aluno_candidato = alunos_ciclicos[categoria][idx_atual % len(alunos)]
                indice_aluno[categoria] += 1
                chave_escala = (vaga['data'], vaga['turno'], vaga['local'])
                chave_conflito = (vaga['data'], vaga['turno'])
                if aluno_candidato not in conflitos[chave_conflito]:
                    escala_final[chave_escala][vaga['tipo_vaga']].append(aluno_candidato)
                    conflitos[chave_conflito].add(aluno_candidato)
                    contagem_por_aluno[aluno_candidato][categoria] += 1
                    alocado = True
                    break
            if not alocado:
                chave_escala = (vaga['data'], vaga['turno'], vaga['local'])
                escala_final[chave_escala][vaga['tipo_vaga']].append("VAGA_NAO_PREENCHIDA")
    return escala_final, contagem_por_aluno