import re
import pandas as pd
import numpy as np

def ponto_df_creator(file):

    raw_df = pd.read_excel('dados\\'+ file,header = [8], usecols='A:D')
    text = raw_df.to_string()

    full_pattern = re.compile(r'([A-Z][a-z]{2}[ ]{2}\d{2}:\d{2} \d{2}:\d{2} \d{2}:\d{2} \d{2}:\d{2}|[A-Z][a-z]{2}[ ]{2}\d{2}:\d{2} \d{2}:\d{2} [ ]{5} [ ]{5}|[A-Z][a-z]{2}[ ]{2}[ ]{5} [ ]{5} \d{2}:\d{2} \d{2}:\d{2}|[A-Z][a-z]{2}[ ]{22}NaN)')
    name_pattern = re.compile(r'\w+ \w+ \w+ \w* \w*')
    code_pattern = re.compile(r'\d{6}')
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    time_pattern = re.compile(r'(\d{2}:\d{2} \d{2}:\d{2} \d{2}:\d{2} \d{2}:\d{2}|\d{2}:\d{2} \d{2}:\d{2} [ ]{5} [ ]{5}|[ ]{5} [ ]{5} \d{2}:\d{2} \d{2}:\d{2})')

    data = []

    full_matches = full_pattern.finditer(text)
    for full_match in full_matches:
        match = full_match.group()
        index = full_match.span()[0]
        name_matches = name_pattern.findall(text[:index])
        code_matches = code_pattern.findall(text[:index])
        date_matches = date_pattern.findall(text[:index])
        time_matches = time_pattern.search(match)

        i = len(match.split())

        if i == 5:
            (open_1, close_1, open_2, close_2) = time_matches.group().split()
        elif i == 3 and time_matches.group().endswith(' '):
            (open_1, close_1) = (time_matches.group().split())
            (open_2, close_2) = ('00:00','00:00')
        elif i == 3 and time_matches.group().startswith(' '):
            (open_1, close_1) = ('00:00','00:00')
            (open_2, close_2) = (time_matches.group().split())
        else:
            (open_1, close_1, open_2, close_2) = ('00:00','00:00','00:00','00:00')

        time = '{} {} {} {}'.format(open_1, close_1, open_2, close_2)

        date_matches[-1] = date_matches[-1].replace('1901', '2022')
        open_1 = date_matches[-1] + ' ' + open_1 +':00'
        close_1 = date_matches[-1] + ' ' + close_1 + ':00'
        open_2 = date_matches[-1] + ' ' + open_2 + ':00'
        close_2 = date_matches[-1] + ' ' + close_2 + ':00'

        operador = '{} - {}'.format(code_matches[-1], name_matches[-1])


        user_info = (code_matches[-1], operador, date_matches[-1], time, open_1,close_1,open_2,close_2)
        data.append(user_info)

    df = pd.DataFrame(data, columns=['matricula', 'Operador' , 'Data', 'Entrada/Saída', 'entrada_1','saida_1','entrada_2','saida_2'])
    df['matricula'] = pd.to_numeric(df['matricula'])

    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')

    df[['entrada_1', 'saida_1', 'entrada_2', 'saida_2']] = df[['entrada_1', 'saida_1', 'entrada_2', 'saida_2']].apply(pd.to_datetime, format = '%Y-%m-%d %H:%M:%S')

    df['saida_1'] = np.where(df['saida_1'] < df['entrada_1'], df['saida_1'] + pd.Timedelta(days=1),df['saida_1'])
    df['saida_2'] = np.where(df['saida_2'] < df['entrada_2'], df['saida_2'] + pd.Timedelta(days=1),df['saida_2'])

    df['Expediente Total'] = df['saida_1'] - df['entrada_1'] + df['saida_2'] - df['entrada_2']
    # df.to_excel('ponto_df.xlsx')
    return df

def solinftec_df_creator(solinftec_file):
    df = pd.read_excel('dados\\' + solinftec_file)
    df = df[['Data', 'Operador', 'Estado', 'Duração (h)']]
    df = df.fillna(0)
    i = df.index[(df['Data'] == 'Total')].tolist()
    ii = df.index[df['Operador'] == '-1 - * não definido *'].tolist()

    df.drop(df.index[i[0]:], inplace=True)
    df.drop(df.index[ii], inplace=True)

    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d %H:%M:%S')
    df[['matricula', 'nome']] = df['Operador'].str.split('-', expand=True)
    df['matricula'] = df['matricula'].astype(int)

    df_pivot = df.pivot_table(values='Duração (h)', columns='Estado', index=['Operador', 'matricula', 'Data'], aggfunc=np.sum)
    df_pivot.drop(['DESCARREGANDO', 'DESLOC P/ DESC'], axis=1, inplace=True)
    df_pivot.fillna(0, inplace=True)
    df_pivot['Total Geral'] = df_pivot['DESLOCAMENTO'] + df_pivot['MANOBRA'] + df_pivot['PARADA'] + df_pivot['TRABALHANDO']
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns= {'Operador': 'operador'}, inplace=True)
    # df.to_excel('solinftec_df.xlsx')
    return df_pivot

def merge_data(p_df, s_df):
    final_df = pd.merge(p_df, s_df, on = ['matricula', 'Data'], how = 'left')
    final_df = final_df[['Operador', 'Data', 'Entrada/Saída', 'Expediente Total', 'DESLOCAMENTO', 'MANOBRA', 'PARADA', 'TRABALHANDO', 'Total Geral']]
    columns = ['DESLOCAMENTO', 'MANOBRA', 'PARADA', 'TRABALHANDO', 'Total Geral']
    final_df[columns] = final_df[columns].apply(pd.to_timedelta, unit = 'h')
    final_df.set_index(['Operador', 'Data'], inplace=True)
    final_df.to_excel('final.xlsx')
    return final_df

solinftec_file = 'solinftec.xlsx'
ponto_file = 'ponto.xlsx'

if __name__ == '__main__':
    try:
        p_df = ponto_df_creator(ponto_file)
        print(f'\nOK >>> Arquivo {ponto_file} processado com sucesso')
    except:
        print(f'\nErro no processamento de {ponto_file}')

    try:
        s_df = solinftec_df_creator(solinftec_file)
        print(f'\nOK >>> Arquivo {solinftec_file} processado com sucesso')
    except:
        print(f'\nErro no processamento de {solinftec_file}')

    try:
        merge_data(p_df, s_df)
        print('\nOK >>> Cruzamento dos dados realizado com sucesso')
    except PermissionError:
        print('\nErro no cruzamento dos dados\nPlanilha final.xlsx está aberta')
