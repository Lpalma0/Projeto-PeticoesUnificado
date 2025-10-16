
from docx.shared import Pt


def inserir_texto_em_negrito(documento, texto):

    p = documento.add_paragraph()
    p.add_run(texto).bold = True

def substituir_marcador_paragrafo(paragrafo, marcador, substituto):
    for run in paragrafo.runs:
        if marcador in run.text:
            run.text = run.text.replace(marcador, substituto)
            run.font.size = Pt(11)
            return True
    return False


def tratamento_word(num_vara, foro, classe):
    if 'Regional' in foro:
        
        try:
            text_puro = foro.split('-')
            foro_regional = text_puro[1].strip()
        except:
            foro_regional = str(foro.split("de")[1]).strip()
            
        text_foro =  f'DA {num_vara} VARA CÍVEL DO FORO REGIONAL DE {foro_regional} DA COMARCA DE SÃO PAULO/SP'
        
    elif 'Central Cível' in foro:
        
        text_foro = f'DA {num_vara} VARA CÍVEL do foro regional central cível da comarca de são paulo/sp'
        
        
    else:
        
        foro = foro.replace('Foro de','').strip()
        text_foro = f'DA {num_vara} VARA CÍVEL DA COMARCA DE {foro}/SP'
        
        
    return text_foro