from abc import ABC, abstractmethod
from historico import Historico
from utils import filtrar_cliente


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
