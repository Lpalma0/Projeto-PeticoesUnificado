import questionary

choices = ["Endereço", "Desistencia", "Sentença"]

print("Gerar petições de: ")
escolha = questionary.select("Select an option:", choices=choices).ask()

if escolha == "Endereço":
    from Endereco.main import start
    start()
    
elif escolha == "Desistencia":
    from Desistencia.main import start
    start()
    
elif escolha == "Sentença":
    from Sentenca.main import start
    start()