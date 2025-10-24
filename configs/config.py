from pathlib import Path


class Config:
    
    CWD = Path.cwd()
    
    # region Desistencias
    NOME_TEMPLATE_DESISTENCIAS   = "DESISTÊNCIA COM BLOQUEIO (MODELO).docx"
    NOME_EXCEL_BASE_DESISTENCIAS = "DESISTENCIAS.xlsx"
    
    PATH_TEMPLATE_DESISTENCIAS    = CWD / "automations" / "desistencia" / "templates" / NOME_TEMPLATE_DESISTENCIAS
    PATH_INPUT_EXCEL_DESISTENCIAS = fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\BASE\{NOME_EXCEL_BASE_DESISTENCIAS}"
    PATH_OUTPUT_DESISTENCIAS      = r"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\DESISTENCIA"
    
    
    