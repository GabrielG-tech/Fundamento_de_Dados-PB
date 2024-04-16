from CRUD import *

# Lista de tarefas inicial
listaTarefas = []

# Função para criar uma lista padrão de tarefas (se necessário)
def criar_lista_padrao(listaTarefas):
    listaTarefas = [
        [1, "Fazer Pizza", "Pendente", "20-03-2024", "2024-03-25", "alta"],
        [2, "Estudar italiano", "Concluída", "18-03-2024", "2024-03-22", "média"]
    ]
    return listaTarefas

# Opção para criar uma lista padrão de tarefas (descomente se necessário)
listaTarefas = criar_lista_padrao(listaTarefas)

# Loop principal para interação com o usuário
continuar = True
while continuar:
    mostrar_menu()
    escolha = input("Escolha uma das opções: ")

    if escolha == "1":
        incluir_tarefa(listaTarefas)
    elif escolha == "2":
        exibir_tarefas(listaTarefas)
    elif escolha == "3":
        concluir_tarefa(listaTarefas)
    elif escolha == "4":
        excluir_tarefa(listaTarefas)
    elif escolha == "5":
        continuar = False
    else:
        print("Entrada inválida, tente novamente.\n")
