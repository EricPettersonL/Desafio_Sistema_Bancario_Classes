from abc import ABC, abstractmethod
from utils import verificar_cliente
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
