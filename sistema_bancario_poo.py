from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        pass


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor
        self._data_hora = datetime.now()

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data_hora(self) -> datetime:
        return self._data_hora

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor
        self._data_hora = datetime.now()

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data_hora(self) -> datetime:
        return self._data_hora

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


class Historico:
    def __init__(self) -> None:
        self._transacoes: List[Transacao] = []

    @property
    def transacoes(self) -> List[Transacao]:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append(transacao)

    def gerar_relatorio(self) -> str:
        if not self._transacoes:
            return "Não foram realizadas movimentações."
        
        linhas = []
        for t in self._transacoes:
            tipo = t.__class__.__name__
            linhas.append(f"{tipo:<10}: R$ {t.valor:10.2f}")
        return "\n".join(linhas)


class Conta:
    def __init__(self, numero: int, cliente: "Cliente", agencia: str = "0001") -> None:
        self._saldo: float = 0.0
        self._numero: int = numero
        self._agencia: str = agencia
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: "Cliente", numero: int, agencia: str = "0001") -> "Conta":
        return cls(numero, cliente, agencia)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> "Cliente":
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("[!] Operação falhou: O valor informado para saque deve ser positivo.")
            return False

        if valor > self._saldo:
            print(f"[!] Operação falhou: Saldo insuficiente. Saldo disponível: R$ {self._saldo:.2f}")
            return False

        self._saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("[!] Operação falhou: O valor do depósito deve ser maior que zero.")
            return False

        self._saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(
        self,
        numero: int,
        cliente: "Cliente",
        agencia: str = "0001",
        limite: float = 500.0,
        limite_saques: int = 3,
    ) -> None:
        super().__init__(numero, cliente, agencia)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    def sacar(self, valor: float) -> bool:
        saques_realizados = len(
            [t for t in self.historico.transacoes if isinstance(t, Saque)]
        )

        if valor > self._limite:
            print(f"[!] Operação falhou: O valor excede o limite de R$ {self._limite:.2f} por saque.")
            return False

        if saques_realizados >= self._limite_saques:
            print(f"[!] Operação falhou: Limite máximo diário de {self._limite_saques} saques atingido.")
            return False

        return super().sacar(valor)

    def __str__(self) -> str:
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        Saldo:\t\tR$ {self.saldo:.2f}
        """


class Cliente:
    def __init__(self, endereco: str) -> None:
        self._endereco = endereco
        self._contas: List[Conta] = []

    @property
    def contas(self) -> List[Conta]:
        return self._contas

    def adicionar_conta(self, conta: Conta) -> None:
        self._contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> bool:
        return transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento


def menu():
    return """
========================================
         DIO BANK - VERSÃO POO          
========================================
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova Conta
[lc] Listar Contas
[nu] Novo Usuário
[q]  Sair
========================================
=> Escolha uma opção: """


def main():
    clientes: List[PessoaFisica] = []
    contas: List[ContaCorrente] = []
    numero_conta = 1

    while True:
        opcao = input(menu()).strip().lower()

        if opcao == "d":
            cpf = input("Informe o CPF do titular (somente números): ").strip()
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente or not cliente.contas:
                print("[!] Cliente ou conta não encontrados!")
                continue

            try:
                valor = float(input("Informe o valor do depósito: R$ "))
            except ValueError:
                print("[!] Valor inválido!")
                continue

            transacao = Deposito(valor)
            if cliente.realizar_transacao(cliente.contas[0], transacao):
                print(f"[+] Depósito de R$ {valor:.2f} efetuado com sucesso!")

        elif opcao == "s":
            cpf = input("Informe o CPF do titular: ").strip()
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente or not cliente.contas:
                print("[!] Cliente ou conta não encontrados!")
                continue

            try:
                valor = float(input("Informe o valor do saque: R$ "))
            except ValueError:
                print("[!] Valor inválido!")
                continue

            transacao = Saque(valor)
            if cliente.realizar_transacao(cliente.contas[0], transacao):
                print(f"[+] Saque de R$ {valor:.2f} realizado com sucesso!")

        elif opcao == "e":
            cpf = input("Informe o CPF do titular: ").strip()
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente or not cliente.contas:
                print("[!] Cliente ou conta não encontrados!")
                continue

            conta = cliente.contas[0]
            print("\n================ EXTRATO ================")
            print(conta.historico.gerar_relatorio())
            print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
            print("=========================================")

        elif opcao == "nu":
            cpf = input("Informe o CPF (somente números): ").strip()
            if any(c.cpf == cpf for c in clientes):
                print("[!] Já existe cliente cadastrado com esse CPF.")
                continue

            nome = input("Informe o nome completo: ").strip()
            nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ").strip()

            cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=nascimento, endereco=endereco)
            clientes.append(cliente)
            print("[+] Cliente cadastrado com sucesso!")

        elif opcao == "nc":
            cpf = input("Informe o CPF do titular: ").strip()
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if not cliente:
                print("[!] Cliente não cadastrado! Cadastre o usuário primeiro.")
                continue

            conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
            contas.append(conta)
            cliente.adicionar_conta(conta)
            numero_conta += 1
            print(f"[+] Conta corrente criada com sucesso! Agência: {conta.agencia} | Conta: {conta.numero}")

        elif opcao == "lc":
            if not contas:
                print("[!] Nenhuma conta cadastrada.")
                continue
            for conta in contas:
                print("=" * 40)
                print(str(conta))

        elif opcao == "q":
            print("\nObrigado por utilizar os serviços do DIO Bank! Até breve.\n")
            break

        else:
            print("[!] Opção inválida.")


if __name__ == "__main__":
    main()
