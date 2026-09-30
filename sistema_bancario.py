"""
DIO Bank - Sistema Bancario em Python
Desenvolvido por Daniel Fernando Martins

Projeto desenvolvido como parte da Formacao / Trilha Python da DIO.
Objetivo: Simular as operacoes basicas de um sistema bancario (deposito, saque e extrato)
aplicando boas praticas de programacao e regras de negocio.
"""

def main():
    saldo = 0.0
    limite_por_saque = 500.0
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES_DIARIOS = 3

    menu = """
========================================
             DIO BANK - MENU            
========================================
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
========================================
=> Escolha uma operacao: """

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            print("\n--- OPERACAO DE DEPOSITO ---")
            try:
                valor = float(input("Informe o valor a depositar: R$ "))
            except ValueError:
                print("[!] Valor invalido. Digite apenas numeros.")
                continue

            if valor > 0:
                saldo += valor
                extrato += f"Deposito: R$ {valor:10.2f}\n"
                print(f"[+] Deposito de R$ {valor:.2f} realizado com sucesso!")
            else:
                print("[!] Operacao falhou: O valor informado deve ser maior que zero.")

        elif opcao == "s":
            print("\n--- OPERACAO DE SAQUE ---")
            try:
                valor = float(input("Informe o valor a sacar: R$ "))
            except ValueError:
                print("[!] Valor invalido. Digite apenas numeros.")
                continue

            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite_por_saque
            excedeu_saques = numero_saques >= LIMITE_SAQUES_DIARIOS

            if excedeu_saldo:
                print(f"[!] Operacao falhou: Saldo insuficiente. Saldo atual: R$ {saldo:.2f}")

            elif excedeu_limite:
                print(f"[!] Operacao falhou: O valor do saque excede o limite de R$ {limite_por_saque:.2f} por operacao.")

            elif excedeu_saques:
                print(f"[!] Operacao falhou: Limite diario de {LIMITE_SAQUES_DIARIOS} saques atingido.")

            elif valor > 0:
                saldo -= valor
                extrato += f"Saque:    R$ {valor:10.2f}\n"
                numero_saques += 1
                print(f"[+] Saque de R$ {valor:.2f} realizado com sucesso! (Saques restantes hoje: {LIMITE_SAQUES_DIARIOS - numero_saques})")

            else:
                print("[!] Operacao falhou: O valor informado deve ser positivo.")

        elif opcao == "e":
            print("\n================ EXTRATO ================")
            if not extrato:
                print("Nao foram realizadas movimentacoes.")
            else:
                print(extrato, end="")
            print(f"\nSaldo atual: R$ {saldo:.2f}")
            print("=========================================")

        elif opcao == "q":
            print("\nObrigado por utilizar os servicos do DIO Bank! Tenha um excelente dia.\n")
            break

        else:
            print("\n[!] Opcao invalida. Por favor, selecione uma opcao valida do menu.")

if __name__ == "__main__":
    main()
