import datetime
import random
from collections import defaultdict
import holidays

def parse_form_data(form):
    config = {'grupos': [], 'locais': []}
    
    grupo_nomes = {k: v for k, v in form.items() if k.startswith('grupo_nome_')}
    for key, nome in grupo_nomes.items():
        if not nome: continue
        index = key.split('_')[-1]
        num_alunos = int(form.get(f'grupo_alunos_{index}', 0))
        config['grupos'].append({'nome': nome, 'alunos': num_alunos})

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
        config['locais'].append({'nome': nome, 'regras': regras})
        
    return config

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
                categoria = f"DIURNO_{'FDS_FERIADO' if eh_fds_ou_feriado else 'SEMANA'}_{local['nome']}_{tipo_vaga}"
                vagas_a_preencher.append({'data': data_atual, 'turno': 'Diurno', 'local': local['nome'], 'tipo_vaga': tipo_vaga, 'categoria': categoria})
            
            for tipo_vaga in regras_noite:
                categoria = f"NOTURNO_{'FDS_FERIADO' if eh_fds_ou_feriado else 'SEMANA'}_{local['nome']}_{tipo_vaga}"
                vagas_a_preencher.append({'data': data_atual, 'turno': 'Noturno', 'local': local['nome'], 'tipo_vaga': tipo_vaga, 'categoria': categoria})

        data_atual += datetime.timedelta(days=1)
    return vagas_a_preencher

def criar_escala_justa(alunos, vagas):
    if not alunos or not vagas:
        return {}, {}

    vagas_por_categoria = defaultdict(list)
    for vaga in vagas:
        vagas_por_categoria[vaga['categoria']].append(vaga)

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

                # --- MUDANÇA PRINCIPAL AQUI ---
                # A chave agora inclui o local, para ser única e para o template funcionar
                chave_escala = (vaga['data'], vaga['turno'], vaga['local'])
                chave_conflito = (vaga['data'], vaga['turno']) # Conflito é por data/turno, independente do local

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