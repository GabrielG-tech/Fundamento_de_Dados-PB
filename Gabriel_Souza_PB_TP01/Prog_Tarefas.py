# As tarefas a serem utilizadas poderão ter diferentes metadados: ID da tarefa, descrição, data de criação, status, prazo final, urgência, entre outros atributos... (O seu professor irá disponibilizar uma listagem de tarefas, bem como, as informações que serão manipuladas para cada uma das tarefas.)

"""
Este script implementa um sistema simples de lista de tarefas, permitindo adicionar, listar, marcar como concluída e remover tarefas.
"""
from CRUD import *

def criar_lista_padrao(listaTarefas):
    # Lista de tarefas inicial
    listaTarefas = [["Fazer Pizza", "Pendente"],
                    ["Estudar italiano", "Concluída"],
                    ["Jogar Uno", "Pendente"], 
                    ["TP01 - Projeto", "Pendente"]]
    return listaTarefas

listaTarefas = []
listaTarefas = criar_lista_padrao(listaTarefas)


def adicionar(tarefa: str):
    """
    Adiciona uma nova tarefa à lista de tarefas.

    Parâmetros:
    - tarefa (str): Descrição da tarefa a ser adicionada.

    Retorno:
    Nenhum.
    """
    listaTarefas.append([tarefa, "Pendente"])

def listar():
    """
    Lista todas as tarefas existentes.

    Parâmetros:
    Nenhum.

    Retorno:
    Nenhum.
    """
    numTarefa = 0
    for tarefa in listaTarefas:
        numTarefa += 1
        print("[{}] - {}\t - {}".format(numTarefa, tarefa[0], tarefa[1]))

def concluir(indice: int):
    """
    Marca uma tarefa existente como concluída.

    Parâmetros:
    - indice (int): Índice da tarefa a ser marcada como concluída.

    Retorno:
    Nenhum.
    """
    listaTarefas[indice][1] = "Concluída"

def remover(indice: int):
    """
    Remove uma tarefa da lista.

    Parâmetros:
    - indice (int): Índice da tarefa a ser removida.

    Retorno:
    Nenhum.
    """
    del listaTarefas[indice]

# Loop principal para interação com o usuário
continuar = True
while continuar:
    mostrar_menu()
    escolha = input("Escolha uma das opções: ")

    if escolha == "1": 
        nova_tarefa = input("Digite o nome da tarefa: ")
        adicionar(nova_tarefa)
    elif escolha == "2":
        listar()
    elif escolha == "3":
        indice_concluir = int(input("Escolha o índice da tarefa concluída: ")) - 1
        concluir(indice_concluir)
    elif escolha == "4":
        indice_remover = int(input("Digite o índice da tarefa: ")) - 1
        remover(indice_remover)
    elif escolha.lower() == "5":
        continuar = False
    else:
        print("Entrada inválida, tente novamente.\n")
