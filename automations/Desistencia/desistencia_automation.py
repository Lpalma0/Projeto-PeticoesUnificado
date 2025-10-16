import logging

import numpy as np
from consulta_tjsp import get_foro_and_comarca
from word import tratamento_word,substituir_marcador_paragrafo,Pt

from docx import Document
import pandas as pd
import queue
import threading
from datetime import datetime
from time import sleep
from teste import LoginTJ

from ..configs import config

EXCEL_BASE_DESISTENCIAS = "DESISTENCIAS.xlsx"
PATH_INPUT_EXCEL_DESISTENCIAS = fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\BASE\{EXCEL_BASE_DESISTENCIAS}"
PATH_OUTPUT_DESISTENCIAS = r"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\DESISTENCIA"

PATH_MODELO_DESISTENCIAS = r"DESISTÊNCIA COM BLOQUEIO (MODELO).docx"


MAX_REQUISICOES_SIMULTANEAS = 10

class GeneratePetAddress:
    
    def __init__(self):
        pass
    
    def rescue_district(self,session,process_number:str,login:str="124.774.618-69",password:str="Grp@Icr2024"):
        self.foro,self.num_vara,self.num_processo,self.classe,self.reqte = get_foro_and_comarca(login,password,process_number,session)
    
    def create_doc_word(self, process_number:str, name:str):
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
            "REQTE":self.reqte,
            "TEXT_FORO": text_foro.upper(),
            "NUM_PROCESSO": process_number,
            "CLASSE1" :self.classe.upper(),
            "NOME" : name,
        }
         
        
        documento = Document(PATH_MODELO_DESISTENCIAS)

        for paragrafo in documento.paragraphs:
            for marcador, substituto in vars_text.items():
                substituir_marcador_paragrafo(paragrafo, marcador, substituto)

                for run in paragrafo.runs:
                    run.font.size = Pt(11)

        name_doc = f'{name} - {process_number}.docx'
        # Salve o novo documento
        documento.save(fr"{PATH_OUTPUT_DESISTENCIAS}\{name_doc}")
     
     
    def generate(self, df:pd.DataFrame, session):

        for idx, row in df.iterrows():

            try:
          
                nome = str(row["NOME"]).strip()
                process_number = str(row["PROCESSO"]).strip()
                logging.info(f'Processando linha: {idx}- Processo: {process_number} - Nome: {nome}')
                self.rescue_district(session, process_number)
                self.create_doc_word(process_number, nome)
                
            except Exception as e:
                logging.error(f"Falha ao processar o processo {process_number}: {e}")


def separar_lista(lista: list, quantidade: int):
    new_list = []
    for index in range(0, len(lista), quantidade):
        new_list.append(lista[index:index+quantidade])
    return new_list


def tjsp_autenticar(login=None, password=None):
    session = LoginTJ().login()
    return session  
            
def start():
    df = pd.read_excel(PATH_INPUT_EXCEL_DESISTENCIAS, dtype=str)
    qtd_linhas = len(df)
    
    if qtd_linhas == 0:
        logging.warning("Nenhuma linha encontrada no arquivo Excel. Nada a fazer.")
        return

    requisicoes_simultaneas = min(MAX_REQUISICOES_SIMULTANEAS, qtd_linhas)
    lista_de_dataframes = np.array_split(df, requisicoes_simultaneas)
    logging.info(f"Total de linhas carregadas: {qtd_linhas}")
    logging.info(f"Total de requisições simultâneas: {requisicoes_simultaneas}")
    
    inicio = datetime.now()
    session = tjsp_autenticar("", "")
    
    threads = []
    for df_lote in lista_de_dataframes:
        if not df_lote.empty:
            sleep(2)
            t = threading.Thread(
                target=GeneratePetAddress().generate,
                kwargs={"lista": df_lote, "session": session}
            )
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    fim = datetime.now()

    tempo = fim - inicio

    print(tempo)

if __name__ == "__main__":
    start()

