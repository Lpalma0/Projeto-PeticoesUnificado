import logging
import threading
from datetime import datetime
from time import sleep

import numpy as np
import pandas as pd
from docx import Document

from configs.config import Config
from utils.consulta_tjsp import get_foro_and_comarca
from utils.data_processing import split_dataframe_into_chunks
from utils.login_tjsp import LoginTJ

from .word import Pt, substituir_marcador_paragrafo, tratamento_word

NOME_EXCEL_BASE_DESISTENCIAS = Config.NOME_EXCEL_BASE_DESISTENCIAS
PATH_INPUT_EXCEL_DESISTENCIAS = Config.PATH_INPUT_EXCEL_DESISTENCIAS
PATH_OUTPUT_DESISTENCIAS = Config.PATH_OUTPUT_DESISTENCIAS
PATH_TEMPLATE_DESISTENCIAS = Config.PATH_TEMPLATE_DESISTENCIAS


class GeneratePetDesistencia:
    
    def __init__(self):
        pass

    def rescue_district(
        self,
        session,
        process_number: str,
        login: str = "124.774.618-69",
        password: str = "Grp@Icr2024"
    ) -> bool:
        """
        Resgata informações da comarca do processo.
        Returns:
            bool: Retorna True se achar todas as informações. Caso contrário, False.
        """
        
        self.foro, self.num_vara, self.num_processo, self.classe, self.reqte = get_foro_and_comarca(login, password, process_number, session)

        if all([self.foro, self.num_vara, self.num_processo, self.classe, self.reqte]):
            return True
        return False

    def create_doc_word(self, process_number: str, name: str):
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
        
        
        documento = Document(PATH_TEMPLATE_DESISTENCIAS)

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

                if not self.rescue_district(session, process_number):
                    logging.warning(f"Não foi possível resgatar a comarca para o processo {process_number}")
                    continue

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
    lista_de_dataframes = split_dataframe_into_chunks(df)

    inicio = datetime.now()
    session = tjsp_autenticar("", "")
    
    threads = []
    for df_lote in lista_de_dataframes:
        if not df_lote.empty:
            sleep(2)
            t = threading.Thread(
                target=GeneratePetDesistencia().generate,
                kwargs={"df": df_lote, "session": session}
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

