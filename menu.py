def menu():
    '''
    Função menu
    
    Para a interação com o usuário
    
    '''
    
    print("\n1 - Depositar")
    print("2 - Saque")
    print("3 - Extrato")
    print("4 - Criar usuário")
    print("5 - Criar conta")
    print("6 - Listar contas")
    print("7 - Sair\n")
    
    while True:
        op = input("Escolha uma opção: ")
        if op in {'1', '2', '3', '4', '5', '6', '7'}:
            return op
        else:
            print("Opção inválida. Por favor, escolha novamente.")