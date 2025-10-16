import questionary

choices = ["Endereço", "Desistencia", "Sentença"]

print("Gerar petições de: ")
escolha = questionary.select("Escolha uma opção:", choices=choices).ask()

if escolha == "Endereço":
    #from Endereco.main import start
    start()
    
elif escolha == "Desistencia":
    from automations.desistencia.desistencia_automation import start
    start()
    
elif escolha == "Sentença":
    #from Sentenca.main import start
    start()