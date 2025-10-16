import logging
from bs4 import BeautifulSoup
import requests
import re
import time
import urllib.parse


     

def tjsp_pegar_processo_url(processo_id):
   
    if ".8.26." not in processo_id:
        logging.warning(f"Processo {processo_id} não é de SP. Será ignorado.")
        return None


    url = None
    try:
        
        unificado = re.search(".+?(?=\\.8\\.26)", processo_id).group()
        numero_foro = re.search("\\d{4}$", processo_id).group() 
        request_url = f'https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={unificado}&foroNumeroUnificado={numero_foro}&dadosConsulta.valorConsultaNuUnificado={processo_id}&dadosConsulta.valorConsultaNuUnificado=UNIFICADO&dadosConsulta.valorConsulta=&dadosConsulta.tipoNuProcesso=UNIFICADO'
        url = requests.get(request_url).url
        
        
        if  str(url) == str(request_url):

            contador_vezes = 0

            MAX_TENTATIVAS = 10
            for tentativa in range(MAX_TENTATIVAS + 1):
                time.sleep(tentativa)
                url = requests.get(request_url).url
                logging.info(f"Processo: {processo_id} - Tentando novamente ({tentativa + 1}X)")

                if url != request_url:
                    break
                
                if tentativa < MAX_TENTATIVAS:
                    logging.warning(f"Processo: {processo_id} - Tentativas excedidas ({tentativa + 1}X)")
                    break

        
        codigo_processo = url.split("processo.codigo=")[1].split("&")[0] 
        
        
    except Exception as error_1:
        
        print(error_1)
        
        teste = requests.get(url)
        soup = BeautifulSoup(teste.text,"html.parser")
        link_element = soup.find('a', class_='linkProcesso')
        link = link_element['href']
        codigo_processo = link.split("processo.codigo=")[1].split("&")[0]


    return codigo_processo
    
def pegar_dados_process(codigo_processo):
    processo_url = f'https://esaj.tjsp.jus.br/cpopg/show.do?processo.codigo={codigo_processo}&gateway=true'
    response = session.get(processo_url)
    tratar_dados_boa_sorte = response.content.decode('utf-8')

    return tratar_dados_boa_sorte
    
    
def check_login():
    response = session.get(
        "https://esaj.tjsp.jus.br/sajcas/verificarLogin.js")
    return "true" in response.text

def get_foro_and_comarca(login, senha, processo, session2):
    
    

    try:
        global session
        session = session2
       
        codigo_processo = tjsp_pegar_processo_url(processo)
        if codigo_processo == None:
            print("Retornou None aqui")
        
        tratar = pegar_dados_process(codigo_processo)

        soup = BeautifulSoup(tratar, 'html.parser')
        textos = [texto.strip() for texto in soup.stripped_strings]
        
        
        foro, num_vara, classe, reqte = None, None, None, None
        for posicao, item in enumerate(textos):
            
            if 'Classe' in item or 'Execução de Sentença' in item:
                if item == 'Execução de Sentença':
                    classe = 'Execução de Sentença'
                else:
                    classe = textos[posicao + 1]
            
            
            if item == 'Foro':
                foro = textos[posicao+1]
            
            if item == 'Reqte':
                reqte = textos[posicao+1]
                if reqte[-1] == '.':
                    reqte = reqte.replace(reqte[-1],"")
                break
            
            if 'Vara Cível' in item or 'Vara' in item:
                if 'Vara' in item and 'Vara Cível' not in item:
                    num_vara = textos[posicao+1].replace('Vara','').strip()
                    if 'Cível' in num_vara:
                        num_vara = num_vara.replace('Cível','').strip()
                    
                else:
                    num_vara = item.replace('Vara Cível', '').strip()
              
        #if all([foro, num_vara, processo, classe, reqte]):
        return foro, num_vara, processo, classe, reqte
        
    
    except Exception as e:
        print(e)
        
        return 'Não foi possivel'


        
          

    
base = "https://esaj.tjsp.jus.br/"
login_url = base + "sajcas/login?service=" + \
    urllib.parse.quote(base + "esaj/j_spring_cas_security_check", safe="")

    
