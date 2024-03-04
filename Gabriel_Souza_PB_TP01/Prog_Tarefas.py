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

# Loop principal para interação com o usuário
continuar = True
while continuar:
    mostrar_menu()
    escolha = input("Escolha uma das opções: ")

    match escolha:
        case "1": 
            nova_tarefa = input("Digite o nome da tarefa: ")
            incluir_tarefa(listaTarefas, nova_tarefa)
        case "2":
            exibir_tarefas(listaTarefas)
        case "3":
            indice_concluir = int(input("Escolha o índice da tarefa concluída: ")) - 1
            concluir_tarefa(listaTarefas, indice_concluir)
        case "4":
            indice_remover = int(input("Digite o índice da tarefa: ")) - 1
            excluir_tarefa(listaTarefas, indice_remover)
        case "5":
            continuar = False
        case _:
            print("Entrada inválida, tente novamente.\n")