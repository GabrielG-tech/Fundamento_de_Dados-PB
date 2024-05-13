class Agenda:
    def __init__(self):
        # Inicializa a agenda como um dicionário vazio
        self.contatos = {}

    def adicionar_contato(self, nome, endereco, data_nascimento, telefones, emails):
        # Verifica se o contato já existe na agenda
        if nome in self.contatos:
            print("Este contato já existe na agenda.")
        else:
            # Adiciona o contato à agenda
            self.contatos[nome] = {
                'endereco': endereco,
                'data_nascimento': data_nascimento,
                'telefones': telefones,
                'emails': emails
            }
            print("Contato adicionado com sucesso!")

    def excluir_contato(self, nome):
        # Verifica se o contato existe na agenda
        if nome in self.contatos:
            del self.contatos[nome]
            print("Contato excluído com sucesso!")
        else:
            print("Este contato não existe na agenda.")

    def buscar_contato(self, nome):
        # Verifica se o contato existe na agenda
        if nome in self.contatos:
            # Mostra as informações do contato
            print("Informações do contato:")
            print("Nome:", nome)
            print("Endereço:", self.contatos[nome]['endereco'])
            print("Data de Nascimento:", self.contatos[nome]['data_nascimento'])
            print("Telefones:", self.contatos[nome]['telefones'])
            print("Emails:", self.contatos[nome]['emails'])
        else:
            print("Este contato não foi encontrado na agenda.")

# Criando uma instância da agenda
agenda = Agenda()

# Adicionando contatos
agenda.adicionar_contato("João", "Rua A, 123", "01/01/1990", ["123456789", "987654321"], ["joao@example.com"])
agenda.adicionar_contato("Maria", "Rua B, 456", "15/05/1985", ["987654321"], ["maria@example.com"])

# Buscando contatos
agenda.buscar_contato("João")
agenda.buscar_contato("Pedro")  # Pedro não está na agenda

# Excluindo um contato
agenda.excluir_contato("Maria")
agenda.buscar_contato("Maria")  # Maria foi excluída


'''
agenda = {}

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
        print("Nome:", nome)
        print("Endereço:", agenda[nome]['endereco'])
        print("Data de Nascimento:", agenda[nome]['data_nascimento'])
        print("Telefones:", agenda[nome]['telefones'])
        print("Emails:", agenda[nome]['emails'])
    else:
        print(f"O contato {nome} não foi encontrado na agenda.")

# Exemplo de uso:
adicionar_contato("João", "Rua A, 123", "01/01/1990", ["123456789", "987654321"], ["joao@example.com"])
adicionar_contato("Maria", "Rua B, 456", "15/05/1985", ["987654321"], ["maria@example.com"])

buscar_contato("João")
buscar_contato("Pedro")

excluir_contato("Maria")
buscar_contato("Maria")

'''