def adicionar_contato(nome, endereco, data_nascimento, telefones, emails):
    if nome not in agenda:
        agenda[nome] = {
            'endereco': endereco,
            'data_nascimento': data_nascimento,
            'telefones': telefones,
            'emails': emails
        }
        print(f"Contato {nome} adicionado com sucesso!")
    else:
        print(f"O contato {nome} já existe na agenda.")

def excluir_contato(nome):
    if nome in agenda:
        del agenda[nome]
        print(f"Contato {nome} excluído com sucesso!")
    else:
        print(f"O contato {nome} não existe na agenda.")

def buscar_contato(nome):
    if nome in agenda:
        print(f"Informações do contato {nome}:")
        print("● Nome:", nome)
        print("● Endereço:", agenda[nome]['endereco'])
        print("● Data de Nascimento:", agenda[nome]['data_nascimento'])
        print("● Telefones:", agenda[nome]['telefones'])
        print("● Emails:", agenda[nome]['emails'])
    else:
        print(f"O contato {nome} não foi encontrado na agenda.")

def listar_contatos():
    print("Contatos na agenda:")
    for nome in agenda:
        print("-", nome)

def alterar_contato(nome):
    if nome in agenda:
        print(f"Alterando informações do contato {nome}:")
        endereco = input("Digite o novo endereço: ")
        data_nascimento = input("Digite a nova data de nascimento: ")
        telefones = input("Digite os novos telefones (separados por vírgula): ").split(',')
        emails = input("Digite os novos emails (separados por vírgula): ").split(',')

        agenda[nome]['endereco'] = endereco
        agenda[nome]['data_nascimento'] = data_nascimento
        agenda[nome]['telefones'] = telefones
        agenda[nome]['emails'] = emails
        print(f"Informações do contato {nome} alteradas com sucesso!")
    else:
        print(f"O contato {nome} não existe na agenda.")

def mostrar_menu():
    print("\nMenu:")
    print("1. Adicionar Contato")
    print("2. Buscar Contato")
    print("3. Listar Contatos")
    print("4. Alterar Contato")
    print("5. Excluir Contato")
    print("6. Sair")

agenda = {}

adicionar_contato("João", "Rua A, 123", "01/01/1990", ["123456789", "987654321"], ["joao@example.com"])
adicionar_contato("Maria", "Rua B, 456", "15/05/1985", ["987654321"], ["maria@example.com"])

buscar_contato("João")
buscar_contato("Pedro")

excluir_contato("Maria")
buscar_contato("Maria")

while True:
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        nome = input("Digite o nome do contato: ")
        endereco = input("Digite o endereço: ")
        data_nascimento = input("Digite a data de nascimento: ")
        telefones = input("Digite os telefones (separados por vírgula): ").split(',')
        emails = input("Digite os emails (separados por vírgula): ").split(',')
        adicionar_contato(nome, endereco, data_nascimento, telefones, emails)
    elif opcao == '2':
        nome = input("Digite o nome do contato: ")
        buscar_contato(nome)
    elif opcao == '3':
        listar_contatos()
    elif opcao == '4':
        nome = input("Digite o nome do contato que deseja alterar: ")
        alterar_contato(nome)
    elif opcao == '5':
        nome = input("Digite o nome do contato que deseja excluir: ")
        excluir_contato(nome)
    elif opcao == '6':
        print("Saindo...")
        break
    else:
        print("Opção inválida.")