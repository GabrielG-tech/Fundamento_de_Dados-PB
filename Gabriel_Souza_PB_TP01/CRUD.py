def mostrar_menu():
    """
    Exibe o menu do programa de lista de tarefas.

    Parâmetros:
    Nenhum.

    Retorno:
    Nenhum.
    """
    print("\n" + "="*9 + " Lista de Tarefas " + "="*9)
    print("[1] - Adicionar Tarefa")
    print("[2] - Listar Tarefas")
    print("[3] - Marcar Tarefa como Concluída")
    print("[4] - Remover Tarefa")
    print("[5] - Sair")
    print("="*36 + "\n")

def exibir_tarefas(tarefas):
    """
    Exibe todas as tarefas existentes.

    Parâmetros:
    - tarefas (list): Lista de tarefas a ser exibida.

    Retorno:
    Nenhum.
    """
    for tarefa in tarefas:
        print(f"{tarefa[0]} -\t{tarefa[1]}")


def pesquisar_tarefa(tarefas, num):
    """
    Pesquisa uma tarefa na lista de tarefas com base no número da tarefa.

    Parâmetros:
    - tarefas (list): Lista de tarefas a ser pesquisada.
    - num (int): Número da tarefa a ser pesquisada.

    Retorno:
    - tarefa_pesquisada (list): Lista contendo os dados da tarefa encontrada.
    """
    tarefa_pesquisada = []
    for tarefa in tarefas:
        if tarefa[0] == num:
            tarefa_pesquisada = tarefa
            break
    return tarefa_pesquisada

def incluir_tarefa(tarefas):
    """
    Inclui uma nova tarefa na lista de tarefas.

    Parâmetros:
    - tarefas (list): Lista de tarefas onde a nova tarefa será incluída.

    Retorno:
    Nenhum.
    """
    while True:
        try:
            num = int(input("Entre com número da tarefa: "))
            break
        except ValueError:
            print("Erro: Por favor, insira um número inteiro para o número da tarefa.")

    tarefa = pesquisar_tarefa(tarefas, num)
    if tarefa:
        print("Erro: tarefa já existe")
        return
    descricao = input("Entre com a descrição: ")
    status = input("Entre com o status: ")
    tarefas.append([num, descricao, status])

def concluir_tarefa(tarefas):
    """
    Marca uma tarefa como concluída.

    Parâmetros:
    - tarefas (list): Lista de tarefas onde a tarefa será marcada como concluída.

    Retorno:
    Nenhum.
    """
    indice = int(input("Escolha o índice da tarefa concluída: ")) - 1
    if indice >= 0 and indice < len(tarefas):
        tarefas[indice][1] = "Concluída"
        print("Tarefa marcada como concluída com sucesso.")
    else:
        print("Erro: Índice da tarefa inválido.")

def excluir_tarefa(tarefas):
    """
    Exclui uma tarefa da lista de tarefas.

    Parâmetros:
    - tarefas (list): Lista de tarefas onde a tarefa será removida.

    Retorno:
    Nenhum.
    """
    try:
        num = int(input("Entre com o número da tarefa: "))
    except ValueError:
        print("Erro: Por favor, insira um número inteiro para o número da tarefa.")
        return
    tarefa = pesquisar_tarefa(tarefas, num)
    if not tarefa:
        print("Erro: tarefa não existe")
        return
    tarefas.remove(tarefa)

# ============================================================

# def exibir_tarefas(tarefas):
#     """
#     Exibe as informações de todas as tarefas.

#     Parâmetros:
#     - tarefas (list): Uma lista contendo as tarefas, cada tarefa é uma lista com os seguintes elementos:
#         - ID (int): O identificador único da tarefa.
#         - Descrição (str): A descrição da tarefa.
#         - Status (str): O status atual da tarefa.
#         - Data de Criação (str): A data em que a tarefa foi criada.
#         - Prazo Final (str): A data de prazo final para a conclusão da tarefa.
#         - Urgência (str): O nível de urgência da tarefa.

#     Retorno:
#     Nenhum.
#     """

# def pesquisar_tarefa(tarefas, num):
#     """
#     Pesquisa uma tarefa pelo seu ID na lista de tarefas.

#     Parâmetros:
#     - tarefas (list): Uma lista contendo as tarefas.
#     - num (int): O ID da tarefa a ser pesquisada.

#     Retorno:
#     - tarefa_pesquisada (list): A tarefa encontrada, ou uma lista vazia se a tarefa não for encontrada.
#     """

# def incluir_tarefa(tarefas):
#     """
#     Inclui uma nova tarefa na lista de tarefas.

#     Parâmetros:
#     - tarefas (list): Uma lista contendo as tarefas.

#     Retorno:
#     Nenhum.
#     """

# def excluir_tarefa(tarefas):
#     """
#     Exclui uma tarefa da lista de tarefas.

#     Parâmetros:
#     - tarefas (list): Uma lista contendo as tarefas.

#     Retorno:
#     Nenhum.
#     """
