from pathlib import Path


class Config:
    
    CWD = Path.cwd()
    
    # region Endereço
    NOME_TEMPLATE_ENDERECO   = "PETICAO_ENDERECO_TEMPLATE.docx"
    NOME_EXCEL_BASE_ENDERECO = "Planilha endereços.xlsx"
    
    PATH_TEMPLATE_ENDERECO     = CWD / "automations" / "endereco" / "templates" / NOME_TEMPLATE_ENDERECO
    PATH_INPUT_EXCEL_ENDERECOS = fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\BASE\{NOME_EXCEL_BASE_ENDERECO}"
    PATH_OUTPUT_ENDERECOS      = "\\192.168.1.54\desenvolvimentojuridico$\PETICOES\ENDERECO"
    
    
    
    # region Desistências
    NOME_TEMPLATE_DESISTENCIAS   = "DESISTÊNCIA COM BLOQUEIO (MODELO).docx"
    NOME_EXCEL_BASE_DESISTENCIAS = "DESISTENCIAS.xlsx"
    
    PATH_TEMPLATE_DESISTENCIAS    = CWD / "automations" / "desistencia" / "templates" / NOME_TEMPLATE_DESISTENCIAS
    PATH_INPUT_EXCEL_DESISTENCIAS = fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\BASE\{NOME_EXCEL_BASE_DESISTENCIAS}"
    PATH_OUTPUT_DESISTENCIAS      = fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\DESISTENCIA"
    
    
    
    # region Sentença
    NOME_TEMPLATE_SENTENCA   = "PETICAO_SENTENCA_TEMPLATE.docx"
    NOME_EXCEL_BASE_SENTENCA = "CUMPRIMENTO DE SENTENÇA.xlsx"
    
    PATH_TEMPLATE_SENTENCA    = CWD / "automations" / "sentenca" / "templates" / NOME_TEMPLATE_SENTENCA
    PATH_INPUT_EXCEL_SENTENCA = fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\BASE\{NOME_EXCEL_BASE_SENTENCA}"
    PATH_OUTPUT_SENTENCA      = fr"\\192.168.1.54\desenvolvimentojuridico$\PETICOES\SENTENCA"