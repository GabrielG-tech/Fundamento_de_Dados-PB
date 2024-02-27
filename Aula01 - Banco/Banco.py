from Crud import *

def criar_contas(contas):
    contas = [[1, "Anna", 1000], 
            [2, "Gabriel", 2000], 
            [3, "Leilane", 3000], 
            [4, "Lucas", 4000]]
    return contas

contas = []
contas = criar_contas(contas)
exibir_contas(contas)
excluir_conta(contas)
#incluir_conta(contas)
exibir_contas(contas)