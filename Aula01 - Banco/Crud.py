def exibir_contas2(contas):
    for i in range(len(contas)):
        for j in range(len(contas[i])):
            print(contas[i][j], end=" ")
        print()

def exibir_contas(contas):
    for conta in contas:
        print(conta[0], conta[1], conta[2])

def pesquisar_conta1(contas, num):
    achou = False
    for conta in contas:
        if (conta[0] == num):
            achou = True
            break
    return achou

def pesquisar_conta2(contas, num):
    pos = -1
    for i in range(len(contas)):
        if (contas[i][0] == num):
            pos = i
            break
    return pos

def pesquisar_conta(contas, num):
    conta_pesquisada = []
    for conta in contas:
        if (conta[0] == num):
            conta_pesquisada = conta
            break
    return conta_pesquisada

def incluir_conta(contas):
    num = int(input("Entre com número da conta: "))
    conta = pesquisar_conta(contas, num)
    if (conta):
        print("Erro: conta já existe")
        return
    nome = input("Entre com o nome: ")
    saldo = float(input("Entre com o saldo: "))
    contas.append([num, nome, saldo])

def excluir_conta(contas):
    num = int(input("Entre com o número da conta: "))
    conta = pesquisar_conta(contas, num)
    if (not conta): # (conta == [])
        print("Erro: conta não existe")
        return
    contas.remove(conta)