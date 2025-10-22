from docx import Document
import pandas as pd
import queue
import threading
from datetime import datetime
from time import sleep
from teste import LoginTJ

from consulta_tjsp import get_foro_and_comarca
from word import tratamento_word,substituir_marcador_paragrafo,Pt

from utils.data_processing import split_dataframe_into_chunks


class GeneratePetAddress:
    
    def __init__(self):
        pass
    
    def rescue_district(self,session,process_number:str,login:str="124.774.618-69",password:str="Grp@Icr2024"):
        self.foro,self.num_vara,self.num_processo,self.classe,self.reqte = get_foro_and_comarca(login,password,process_number,session)
        
    
    def create_doc_word(self,process_number:str,name:str,address:str):
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
            "ENDERECO_EXCEL" : address+"."
        }
         
        documento = Document(r"Modelo2.docx")

        for paragrafo in documento.paragraphs:
            for marcador, substituto in vars_text.items():
                substituir_marcador_paragrafo(paragrafo, marcador, substituto)

                for run in paragrafo.runs:
                    run.font.size = Pt(11)

        name_doc = f'{name} - {process_number}.docx'
        # Salve o novo documento
        documento.save(fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\ENDERECO\{name_doc}")
     
    
    
    def generate(self, df:pd.DataFrame, session):

        for index, row in df.iterrows():
       
            try:
          
                name = str(row["NOME/BANCO"]).strip()
                print(index)
                print(name)
                process_number = str(row["PROCESSO"]).strip()
                address = str(row["ENDEREÇO/LOCALIZAÇÃO"]).strip()
                
                self.rescue_district(session,process_number)
                self.create_doc_word(process_number,name,address)
            except:
                with open("teste.txt","a+") as f:
                    f.write(process_number+"\n")
            
            
def separar_lista(lista: list, quantidade: int):
    new_list = []
    for index in range(0, len(lista), quantidade):
        new_list.append(lista[index:index+quantidade])
    return new_list  


def tjsp_autenticar(login=None, password=None):
    session = LoginTJ().login()
    return session 
            
def start():
    df = pd.read_excel(r"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\BASE\Planilha endereços.xlsx", dtype=str)

    lista_de_dataframes = split_dataframe_into_chunks(df)
    
    inicio = datetime.now()
    
    session = tjsp_autenticar("", "")
    
    threads = []
    for idx, df_lote in enumerate(lista_de_dataframes):
        if not df_lote.empty:
            sleep(2)
            t = threading.Thread(
                target=GeneratePetAddress().generate,
                kwargs={"df" : df_lote, "session" : session}
            )
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    fim = datetime.now()

    tempo = fim - inicio

    print(tempo)
    
start()

