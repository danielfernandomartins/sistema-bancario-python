# Estudos de caso — Análise de Negócios Bancários

Projetos independentes de portfólio para demonstrar análise de negócios em serviços financeiros. Cada caso combina problema, requisitos, regras, critérios de aceite, SQL para PostgreSQL, dados sintéticos e medidas para Power BI.

| Caso | Desafio |
|---|---|
| Investimentos no aplicativo | Identificar saldo potencialmente ocioso e apresentar uma opção informativa, mediante suitability e consentimento válidos. |
| Alertas de cobrança | Priorizar revisão de contratos vencidos, considerando pagamentos, contestação e preferência de canal. |
| Financiamento de veículos | Organizar tarefas operacionais, pendências, prazos e retrabalho por contrato. |

Todos os registros são fictícios. Os estudos não representam sistemas, políticas, dados, resultados ou trabalho realizado no Bradesco ou em qualquer instituição real. SQL/PostgreSQL e Power BI/DAX são tecnologias demonstradas no portfólio; o repositório não afirma que sejam a stack interna de uma empresa.

## Como reproduzir

Em cada pasta, consulte README.md, execute sql/schema.sql e depois sql/consultas.sql. Importe o CSV de data/ no Power BI Desktop, renomeie a tabela conforme comentário no arquivo powerbi/medidas.dax e crie as medidas.

Os exemplos apoiam discussão e validação de requisitos. Não executam investimentos, não enviam cobranças e não aprovam crédito.
