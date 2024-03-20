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
    print("="*21 + " Tarefas " + "="*21)
    for index, tarefa in enumerate(tarefas):
        num, descricao, status, data_criacao, prazo_final, urgencia = tarefa
        if index < len(tarefas) - 1:  # Verifica se não é o último item
            print(f"{num} - {descricao} - {status} - Urgência: {urgencia}\nCriada em: {data_criacao} - Prazo Final: {prazo_final}\n")
        else:
            print(f"{num} - {descricao} - {status} - Urgência: {urgencia}\nCriada em: {data_criacao} - Prazo Final: {prazo_final}")
    print("="*51)

def pesquisar_tarefa(tarefas, num):
    """
    Pesquisa uma tarefa na lista de tarefas com base no número da tarefa.

    Parâmetros:
    - tarefas (list): Lista de tarefas a ser pesquisada.
    - num (int): Número da tarefa a ser pesquisada.

    Retorno:
    - tarefa_pesquisada (list): Lista contendo os dados da tarefa encontrada.
    """
    for tarefa in tarefas:
        if tarefa[0] == num:
            return tarefa
    return None

def incluir_tarefa(tarefas):
    """
    Inclui uma nova tarefa na lista de tarefas.

    Parâmetros:
    - tarefas (list): Lista de tarefas onde a nova tarefa será incluída.

    Retorno:
    Nenhum.
    """
    # Calcula o próximo ID disponível
    if tarefas:
        proximo_id = max(tarefa[0] for tarefa in tarefas) + 1
    else:
        proximo_id = 1

    descricao = input("Entre com a descrição: ")
    status = "Pendente"
    
    while True:
        try:
            data_criacao = input("Entre com a data de criação (formato: DD-MM-AAAA): ")
            break
        except ValueError:
            print("Erro: Por favor, insira uma data no formato DD-MM-AAAA de criação da tarefa.")
    while True:
        try:
            prazo_final = input("Entre com o prazo final (formato: DD-MM-AAAA): ")
            break
        except ValueError:
            print("Erro: Por favor, insira uma data no formato DD-MM-AAAA de prazo final da tarefa.")

    urgencia = input("Informe a urgência da tarefa ([1] alta, [2] média, [3] baixa): ")
    if urgencia == "1": urgencia = "alta"
    elif urgencia == "2": urgencia = "média"
    elif urgencia == "3": urgencia = "baixa"

    tarefas.append([proximo_id, descricao, status, data_criacao, prazo_final, urgencia])

def concluir_tarefa(tarefas):
    """
    Marca uma tarefa como concluída.

    Parâmetros:
    - tarefas (list): Lista de tarefas onde a tarefa será marcada como concluída.

    Retorno:
    Nenhum.
    """
    num = int(input("Entre com o número da tarefa concluída: "))
    tarefa = pesquisar_tarefa(tarefas, num)
    if not tarefa:
        print("Erro: Tarefa não encontrada.")
        return

    tarefa[2] = "Concluída"
    print("Tarefa marcada como concluída com sucesso.")

def excluir_tarefa(tarefas):
    """
    Exclui uma tarefa da lista de tarefas.

    Parâmetros:
    - tarefas (list): Lista de tarefas onde a tarefa será removida.

    Retorno:
    Nenhum.
    """
    num = int(input("Entre com o número da tarefa: "))
    tarefa = pesquisar_tarefa(tarefas, num)
    if not tarefa:
        print("Erro: Tarefa não encontrada.")
        return

    tarefas.remove(tarefa)

    # Se houver tarefas restantes, atualize os IDs para preencher lacunas
    if tarefas:
        for i, tarefa in enumerate(tarefas):
            tarefa[0] = i + 1