# 🏦 DIO Bank - Sistema Bancário em Python

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Plataforma-DIO-orange.svg)](https://dio.me)
[![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

> Projeto prático desenvolvido durante a formação de tecnologia da [DIO (Digital Innovation One)](https://dio.me), com foco em lógica de programação, estruturas condicionais, laços de repetição e boas práticas com Python.

---

## 📌 Visão Geral

Este projeto simula o funcionamento das operações essenciais de um caixa eletrônico / sistema bancário. O objetivo principal foi criar uma solução robusta em linha de comando (CLI), aplicando validações estritas de regras de negócio financeiras e fornecendo uma experiência amigável e segura para o usuário.

---

## ⚙️ Regras de Negócio e Funcionalidades

O sistema conta com um menu interativo contínuo contendo as seguintes operações:

### 1. 💵 Depósito
- Aceita apenas valores numéricos estritamente positivos.
- Atualiza o saldo em tempo real.
- Todas as transações são registradas no histórico do extrato com data e formatação monetária.

### 2. 💸 Saque
Possui uma camada tripla de validações de segurança:
1. **Verificação de Saldo:** Impede saques superiores ao saldo disponível em conta.
2. **Limite por Transação:** Limite máximo de **R$ 500,00** por operação de saque.
3. **Limite Diário:** Permite no máximo **3 saques diários**.
- Notifica o usuário sobre a quantidade de saques restantes no dia.

### 3. 📄 Extrato
- Exibe a listagem completa de todas as entradas e saídas formatadas em padrão monetário (`R$ XXX.XX`).
- Caso nenhuma movimentação tenha sido realizada, exibe a mensagem amigável: *"Não foram realizadas movimentações."*
- Apresenta o saldo consolidado ao final da consulta.

### 4. 🚪 Sair
- Encerra a aplicação de forma limpa.

---

## 🛠️ Tecnologias e Conceitos Aplicados

- **Linguagem:** Python 3
- **Estruturas de Controle de Fluxo:** `if`, `elif`, `else` para validações lógicas.
- **Laços de Repetição:** `while True` com controle de parada (`break`).
- **Tratamento de Exceções:** Blocos `try / except ValueError` para prevenir travamentos caso o usuário digite caracteres inválidos no lugar de números.
- **Formatação de Dados:** *f-strings* com alinhamento e precisão decimal de duas casas (`:.2f`).
- **Boas Práticas:** Código legível, nomes de variáveis expressivos e aderência aos padrões da **PEP 8**.

---

## 🖥️ Demonstração de Uso

```text
========================================
             DIO BANK - MENU            
========================================
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
========================================
=> Escolha uma operacao: d

--- OPERACAO DE DEPOSITO ---
Informe o valor a depositar: R$ 1000.00
[+] Deposito de R$ 1000.00 realizado com sucesso!

=> Escolha uma operacao: s

--- OPERACAO DE SAQUE ---
Informe o valor a sacar: R$ 200.00
[+] Saque de R$ 200.00 realizado com sucesso! (Saques restantes hoje: 2)

=> Escolha uma operacao: e

================ EXTRATO ================
Deposito: R$    1000.00
Saque:    R$     200.00

Saldo atual: R$ 800.00
=========================================
```

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Ter o **Python 3** instalado em sua máquina.
- Ter o **Git** instalado.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/sistema-bancario-python.git
   ```

2. **Acesse a pasta do projeto:**
   ```bash
   cd sistema-bancario-python
   ```

3. **Execute o script:**
   ```bash
   python sistema_bancario.py
   ```

---

## 📈 Próximas Evoluções (Roadmap)

Conforme a evolução na trilha de aprendizado da DIO:
- [ ] **Fase 2:** Modularização do sistema com funções (`def`), separando regras de saque, depósito e extrato.
- [ ] **Fase 3:** Refatoração completa utilizando **Programação Orientada a Objetos (POO)** com classes para Cliente, Conta Corrente e Histórico.
- [ ] **Fase 4:** Persistência em banco de dados relacional (SQLite / PostgreSQL).

---

## 👨‍💻 Autor

Desenvolvido por **Daniel Fernando Martins**  
- **E-mail:** [dfernandom@outlook.com](mailto:dfernandom@outlook.com)  
- **GitHub:** [@dfernandom](https://github.com/dfernandom)  
- **Perfil DIO:** Estudante em formação na DIO

---
*Gostou do projeto? Deixe uma ⭐️ no repositório!*
