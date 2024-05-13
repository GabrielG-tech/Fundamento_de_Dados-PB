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

agenda = {}

adicionar_contato("João", "Rua A, 123", "01/01/1990", ["123456789", "987654321"], ["joao@example.com"])
adicionar_contato("Maria", "Rua B, 456", "15/05/1985", ["987654321"], ["maria@example.com"])

buscar_contato("João")
buscar_contato("Pedro")

excluir_contato("Maria")
buscar_contato("Maria")