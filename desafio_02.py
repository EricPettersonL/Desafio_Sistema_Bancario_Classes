from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta(ABC):
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @abstractmethod
    def sacar(self, valor):
        pass
    
    @abstractmethod
    def depositar(self, valor):
        pass

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = sum(1 for transacao in self.historico._transacoes if transacao['tipo'] == 'Saque')
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("\nLimite de valor de saque excedido.\n")
        elif excedeu_saques:
            print("\nLimite total de saques excedido.\n")
        elif self._saldo < valor:  
            print("\nSaldo insuficiente.\n")
        else:
            self._saldo -= valor
            print(f"\nSaque de R${valor:.2f} realizado com sucesso.\n")

            return True
            
        return False
    
    def depositar(self, valor):
        self._saldo += valor
        print(f"\nDepósito de R${valor:.2f} realizado com sucesso.\n")

        
    def __str__(self):
        return f"""\
            Agência:\t\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t\t{self.cliente.nome}
            Saldo:\t\tR$ {self.saldo:.2f}
        """

class Historico:
    def __init__(self):
        self._transacoes = []
        

    
    def adicionar_transacao(self, transacao):

        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        })
        
    def __str__(self):
        extrato = ""
        if not self._transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in self._transacoes:
                extrato += f"\n{transacao['tipo']}: \t\t{transacao['data']}  \n\tR$ {transacao['valor']:.2f}"
        return extrato
class Transacao(ABC):
    @property
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        conta.depositar(self._valor)
        conta.historico.adicionar_transacao(self)

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

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta! ")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def verificar_cliente(clientes, operacao):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return None, None

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return None, None

    return cliente, conta


def depositar(clientes):
    cliente, conta = verificar_cliente(clientes, "Depósito")
    if not cliente or not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cliente, conta = verificar_cliente(clientes, "Saque")
    if not cliente or not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cliente, conta = verificar_cliente(clientes, "Exibir Extrato")
    if not cliente or not conta:
        return

    print("\n================ EXTRATO ================")
    print(conta.historico)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n Cliente criado com sucesso! ")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado! ")
        return

    conta = ContaCorrente(numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n Conta criada com sucesso!")

def listar_contas(contas):
    if contas:
        for conta in contas:
            print("=" * 100)
            print(conta)
    else:
        print("\n Nenhuma conta cadastrada! ")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        else:
            break


main()
