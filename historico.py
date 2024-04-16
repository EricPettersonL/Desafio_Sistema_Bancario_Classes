from datetime import datetime

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