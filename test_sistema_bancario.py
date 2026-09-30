import unittest
from sistema_bancario_poo import PessoaFisica, ContaCorrente, Deposito, Saque


class TestSistemaBancarioPOO(unittest.TestCase):
    def setUp(self):
        self.cliente = PessoaFisica(
            cpf="12345678900",
            nome="Daniel Fernando Martins",
            data_nascimento="01-01-1995",
            endereco="Av. Paulista, 1000 - Bela Vista - Sao Paulo/SP",
        )
        self.conta = ContaCorrente.nova_conta(
            cliente=self.cliente,
            numero=1,
            agencia="0001",
        )
        self.cliente.adicionar_conta(self.conta)

    def test_deposito_com_sucesso(self):
        transacao = Deposito(1000.0)
        sucesso = self.cliente.realizar_transacao(self.conta, transacao)
        self.assertTrue(sucesso)
        self.assertEqual(self.conta.saldo, 1000.0)
        self.assertEqual(len(self.conta.historico.transacoes), 1)

    def test_deposito_valor_invalido(self):
        transacao = Deposito(-50.0)
        sucesso = self.cliente.realizar_transacao(self.conta, transacao)
        self.assertFalse(sucesso)
        self.assertEqual(self.conta.saldo, 0.0)

    def test_saque_com_sucesso(self):
        self.cliente.realizar_transacao(self.conta, Deposito(500.0))
        sucesso = self.cliente.realizar_transacao(self.conta, Saque(200.0))
        self.assertTrue(sucesso)
        self.assertEqual(self.conta.saldo, 300.0)

    def test_saque_saldo_insuficiente(self):
        self.cliente.realizar_transacao(self.conta, Deposito(100.0))
        sucesso = self.cliente.realizar_transacao(self.conta, Saque(250.0))
        self.assertFalse(sucesso)
        self.assertEqual(self.conta.saldo, 100.0)

    def test_saque_limite_por_transacao(self):
        self.cliente.realizar_transacao(self.conta, Deposito(2000.0))
        # O limite padrão é 500.0
        sucesso = self.cliente.realizar_transacao(self.conta, Saque(600.0))
        self.assertFalse(sucesso)
        self.assertEqual(self.conta.saldo, 2000.0)

    def test_saque_limite_diario_atingido(self):
        self.cliente.realizar_transacao(self.conta, Deposito(1000.0))
        # Limite padrão são 3 saques
        self.assertTrue(self.cliente.realizar_transacao(self.conta, Saque(100.0)))
        self.assertTrue(self.cliente.realizar_transacao(self.conta, Saque(100.0)))
        self.assertTrue(self.cliente.realizar_transacao(self.conta, Saque(100.0)))
        
        # 4º saque deve ser bloqueado
        bloqueado = self.cliente.realizar_transacao(self.conta, Saque(100.0))
        self.assertFalse(bloqueado)
        self.assertEqual(self.conta.saldo, 700.0)


if __name__ == "__main__":
    unittest.main()
