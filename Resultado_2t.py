import requests
import json
import time
import os
import pandas as pd
from datetime import datetime

#Variaveis globais
pct_urnasApuradas = ''
t=5
current_time = datetime.now().strftime("%H:%M:%S")
while(True):
    try:
        #endpoint site tse com resultado das apuracoes    
        url = 'https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r.json'
        response = requests.get(url)
        jsonObj = json.loads(response.content)
        os.system('cls')
        #verifica se a resposta é igual a anterior
        if (pct_urnasApuradas != jsonObj['psi']):
            print('Porcentagem de urnas apuradas: '+jsonObj['psi']+'%'+' ATUALIZOU')
            pct_urnasApuradas = jsonObj['psi']
            current_time = datetime.now().strftime("%H:%M:%S")
        else:
            print('Porcentagem de urnas apuradas: '+pct_urnasApuradas+'%')
        #filtra somente os dados dos candidatos
        cand = jsonObj['cand']
        #transforma o objeto em dataframe
        df = pd.DataFrame(cand)
        #filtra as colunas importantes
        df.drop(columns=['seq', 'sqcand', 'n', 'cc', 'nv', 'e', 'st', 'dvt'], axis=1, inplace=True)
        df.rename(columns={'nm':'Candidato', 'vap':'Votos Apurados', 'pvap':'Porcentagem'}, inplace=True)
        #centraliza o texto das colunas
        pd.options.display.colheader_justify = 'center'  
        #colunas com o calculo das diferencas relativas ao mais votado
        df['Diferenca'] =  int(df['Votos Apurados'][0]) - pd.to_numeric(df['Votos Apurados']) 
        df['Porcentagem'] = df['Porcentagem'].str.replace(',', '.')
        df['Diferenca Pct'] =  float(df['Porcentagem'][0]) - pd.to_numeric(df['Porcentagem']) 
        #imprime o dataframe      
        print(df.to_string(index=False))
        print('Ultima atualizacao em: '+ current_time)
        time.sleep(t)
    except :
        print('Erro ao atualizar. Tentando novamente...')
        os.system('cls')
        time.sleep(1)
    