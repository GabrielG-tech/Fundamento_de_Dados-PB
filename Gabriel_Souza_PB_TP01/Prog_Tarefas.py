# As tarefas a serem utilizadas poderão ter diferentes metadados: ID da tarefa, descrição, data de criação, status, prazo final, urgência, entre outros atributos... (O seu professor irá disponibilizar uma listagem de tarefas, bem como, as informações que serão manipuladas para cada uma das tarefas.)

# Detalhes da Implementação:

# B - Manipule uma lista para armazenar e gerenciar as tarefas, incluindo adicionar, listar, marcar como concluída e remover tarefas.
# C - Crie funções para cada funcionalidade do sistema (adicionar, listar, marcar como concluída, remover), utilizando argumentos, parâmetros por palavra-chave, parâmetros padrão e retorno de valores.
# D - Documente cada função utilizando DocStrings para descrever seu propósito, uso e parâmetros.

listaTarefas = [["Fazer Pizza", "Pendente"],
                ["Estudar italiano", "Concluida"],
                ["Jogar Uno", "Pendente"], 
                ["TP01 - Projeto", "Pendente"]]

def adicionar():
    tarefa = input("Digite o nome da tarefa: ")
    listaTarefas.append([tarefa, "Pendente"])

def listar():
    numTarefa = 0
    for tarefa in listaTarefas:
        numTarefa += 1
        print("[{}] - {}\t - {}".format(numTarefa, tarefa[0], tarefa[1]))

def concluir():
    tarefa = int(input("Escolha a tarefa concluida: "))
    listaTarefas[tarefa-1][1] = "Concluida"

def remover():
    tarefa = int(input("Digite o índice da tarefa: "))
    listaTarefas.remove(listaTarefas[tarefa-1])

continuar = True
while continuar:
    print("\n" + "="*8 + " Lista de Tarefas " + "="*8)
    print("[1] - Adicionar Tarefa\n[2] - Listar Tarefas\n[3] - Marcar Tarefa como Concluída\n[4] - Remover Tarefa")
    print("="*36 + "\n")
    escolha = input("\nEscolha uma das opções: ")

    if escolha == "1": 
        adicionar()
        # e = input("Deseja continuar? [s/n]: ").lower()
        # if e == "n": 
        #     continuar = False
    elif escolha == "2":
        listar()
        # e = input("Deseja continuar? [s/n]: ").lower()
        # if e == "n": 
        #     continuar = False
    elif escolha == "3":
        concluir()
        # e = input("Deseja continuar? [s/n]: ").lower()
        # if e == "n": 
        #     continuar = False
    elif escolha == "4":
        remover()
        # e = input("Deseja continuar? [s/n]: ").lower()
        # if e == "n": 
        #     continuar = False
    else:
        print("Entrada inválida, tente novamente.\n")
