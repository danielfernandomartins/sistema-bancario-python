# 01 — Oferta informativa de investimentos no app

**Natureza:** projeto de estudo/portfólio. **Dados:** sintéticos. **Tecnologias:** PostgreSQL, SQL, Power BI/DAX.

## Problema e objetivo

Clientes podem manter valores em conta corrente sem destinação imediata. O estudo propõe estimar saldo potencialmente disponível e apresentar uma opção informativa no app quando suitability e consentimento aplicável estiverem válidos. Nenhum dinheiro é movimentado e nenhuma recomendação é gerada automaticamente.

## História do usuário

Como cliente do aplicativo, quero conhecer uma alternativa de investimento compatível com meu perfil e com a disponibilidade do saldo, para decidir voluntariamente se desejo continuar.

## Regras de negócio

1. Saldo potencial = maior valor entre zero e saldo médio de 30 dias menos saldo mínimo observado e reserva operacional hipotética de R$ 500.
2. No exemplo, o cliente é elegível se saldo potencial for de pelo menos R$ 500, suitability for válida e consentimento aplicável estiver registrado.
3. Se a validação falhar, bloquear a oferta e registrar o motivo.
4. Aceite da oferta registra interesse; não significa aplicação liquidada.
5. Qualquer aplicação futura depende de revisão de produto, informação de risco, liquidez, custos e confirmação explícita.

## Critérios de aceite

- Dado um cliente elegível, ao abrir a área de investimentos, é exibida uma oferta informativa com condições claras.
- Dada suitability inválida ou ausência de consentimento, a oferta não é exibida e o motivo é auditável.
- Um aceite não é contabilizado como aplicação concluída.
- Saldo potencial nunca fica abaixo de zero.
- Consulta SQL e painel reconciliam elegíveis, exposições e aceites.

## KPIs

Clientes elegíveis; ofertas exibidas; taxa de aceite sobre ofertas exibidas; saldo potencial estimado; bloqueios por suitability/consentimento; qualidade e completude da base.

## Modelo e consulta SQL

Execute schema.sql; carregue investimentos_demo.csv na tabela investimentos. Abaixo, consulta para estimar oportunidade e identificar elegibilidade:

    WITH base AS (
      SELECT i.*,
        GREATEST(saldo_medio_30d - saldo_minimo_30d - 500.00, 0) AS saldo_potencial
      FROM investimentos i
    )
    SELECT data_ref, segmento, cliente_id, saldo_potencial,
      (suitability_validada AND consentimento_contato AND saldo_potencial >= 500) AS elegivel
    FROM base
    ORDER BY data_ref, segmento, cliente_id;

## Medidas para Power BI

Importe o CSV e renomeie a tabela para Investimentos.

    Clientes com oferta =
      CALCULATE(DISTINCTCOUNT(Investimentos[cliente_id]), Investimentos[oferta_exibida] = TRUE())

    Ofertas aceitas =
      CALCULATE(COUNTROWS(Investimentos), Investimentos[oferta_aceita] = TRUE())

    Taxa de aceite =
      DIVIDE([Ofertas aceitas], CALCULATE(COUNTROWS(Investimentos), Investimentos[oferta_exibida] = TRUE()))

    Saldo potencial elegível =
      SUMX(FILTER(Investimentos, Investimentos[suitability_validada] = TRUE() && Investimentos[consentimento_contato] = TRUE()),
      MAX(0, Investimentos[saldo_medio_30d] - Investimentos[saldo_minimo_30d] - 500))

## Limites

Saldo potencial é uma estimativa didática, não dinheiro confirmado como disponível. Reserva, elegibilidade e consentimento são hipóteses a validar. O projeto não usa dados reais nem imita política de instituição.
