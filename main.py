import logging

import questionary

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        #logging.FileHandler("<caminho log>"),
        logging.StreamHandler(),
    ],
)

choices = ["Endereço", "Desistencia", "Sentença"]

print("Gerar petições de: ")
escolha = questionary.select("Escolha uma opção: ", choices=choices).ask()

if escolha == "Endereço":
    from automations.Endereco.endereco_automation import start as endereco_start
    endereco_start()
    
elif escolha == "Desistencia":
    from automations.desistencia.desistencia_automation import start as desistencia_start
    desistencia_start()
    
elif escolha == "Sentença":
    from automations.Sentenca.sentenca_automation import start as sentenca_start
    sentenca_start()