import logging
import os
import queue
import threading
from datetime import datetime
from decimal import Decimal
from time import sleep

import pandas as pd
from docx import Document

from utils.consulta_tjsp import get_foro_and_comarca
from utils.login_tjsp import LoginTJ

from .word import Pt, substituir_marcador_paragrafo, tratamento_word

from dotenv import load_dotenv; load_dotenv() 



INPUT_EXCEL = "CUMPRIMENTO DE SENTENÇA.xlsx"
PATH_INPUT_EXCEL = f"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\BASE\{INPUT_EXCEL}"

PATH_OUTPUT_SENTENCA = r"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\SENTENCA"

class GeneratePetSentenca:
    
    def __init__(self):
        pass
    
    def rescue_district(self,session,process_number:str,login:str="124.774.618-69",password:str="Grp@Icr2024"):
        self.foro,self.num_vara,self.num_processo,self.classe,self.reqte = get_foro_and_comarca(login,password,process_number,session)
        
    
    def create_doc_word(self, process_number:str, name:str,valor:str):
        text_foro = tratamento_word(
            self.num_vara,
            self.foro,
            self.classe
        )
        if self.classe == 'Execução de Sentença':
            classe1 = 'Execução de Sentença'
            self.classe = 'BUSCA E APREENSÃO EM ALIENAÇÃO FIDUCIÁRIA'
          
        else:
            self.classe = 'AÇÃO DE BUSCA E APREENSÃO EM ALIENAÇÃO FIDUCIÁRIA'
            
        vars_text = {
            "TEXT_FORO": text_foro.upper(),
            "NUM_PROCESSO": process_number,
            "CLASSE1" :self.classe.upper(),
            "NOME" : name,
            "VALOR_EXCEL":valor

        }
        
        documento = Document() #TODO

        for paragrafo in documento.paragraphs:
            for marcador, substituto in vars_text.items():
                substituir_marcador_paragrafo(paragrafo, marcador, substituto)

                for run in paragrafo.runs:
                    run.font.size = Pt(11)

        name_doc = f'{name} - {process_number}.docx'
        # Salve o novo documento
        documento.save(fr"{PATH_OUTPUT_SENTENCA}\{name_doc}")
        print("ok")
    

    def generate(self, lista:list, session):
        df = pd.DataFrame(lista)
        
        
        for index, row in df.iterrows():
       
            try:
          
                name = str(row["NOME"]).strip()
                print(index)
                print(name)
                process_number = str(row["Nº PROCESSO"]).strip()
                value = str(row["VALOR DA CAUSA"]).strip()
                value = Decimal(value)
                value = f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
                value = str(value).replace("R$","").strip()
                contract = str(row["CONTRATO"]).strip()
                
                self.rescue_district(session, process_number)
                self.create_doc_word(process_number, name, value)
                
                
            except Exception as e:
                logging.error(f"Erro ao gerar petição de senteça: {e}")
            
            
def separar_lista(lista: list, quantidade: int):
    new_list = []
    for index in range(0, len(lista), quantidade):
        new_list.append(lista[index:index+quantidade])
    return new_list  

def tjsp_autenticar(login=None, password=None):
    session = LoginTJ().login()
    return session
  

def start():
    
    data_queue = queue.Queue() 
    requisicoes_simultaneas = int(input('Quantas requisições simultaneas deseja fazer?' ))
    
    df = pd.read_excel(rf"{INPUT_EXCEL}", dtype=str)
    
    numero_raw = len(df)  / requisicoes_simultaneas # < Número que deve ser trocado para divisão < 
    lista_separada = separar_lista(df,int(numero_raw))
    inicio = datetime.now()

        
    session = tjsp_autenticar("", "")
    
    threads = []
    for index,lista in enumerate(lista_separada):
        sleep(2)
        t = threading.Thread(target=GeneratePetSentenca().generate,kwargs={"lista" :lista,"session":session})
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    fim = datetime.now()

    tempo = fim - inicio

    print(tempo)
    
start()
