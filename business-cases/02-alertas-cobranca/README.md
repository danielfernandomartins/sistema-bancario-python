# 02 — Priorização de alertas de cobrança

**Natureza:** projeto de estudo/portfólio. **Dados:** sintéticos. **Tecnologias:** PostgreSQL, SQL, Power BI/DAX.

## Problema e objetivo

A operação precisa visualizar contratos vencidos e revisar contatos de forma organizada. O estudo cria uma fila com saldo aberto, dias de atraso, canal preferido, contestação, acordo e tentativas recentes. A fila apoia decisão humana; não envia mensagens automaticamente.

## História do usuário

Como analista da operação de cobrança, quero uma fila priorizada com valor, atraso, status e canal preferido, para revisar o próximo contato e registrar a tratativa.

## Regras de negócio

1. Saldo aberto = valor devido menos pagamentos alocados, limitado a zero.
2. Itens pagos ou contestados ficam fora da fila.
3. Prioridade ordena maior atraso, depois saldo aberto, depois vencimento mais antigo.
4. Duas ou mais tentativas em sete dias geram sinal de revisão de frequência. É um parâmetro fictício do estudo, não uma regra legal.
5. Preferência do canal, acordos e solicitações de não contato devem ser validados antes de qualquer comunicação real.
6. Evitar dados pessoais desnecessários e não inferir penalidade ou consequência não confirmada.

## Critérios de aceite

- A data de referência determina atrasos e fila reproduzível.
- Pagamentos alocados são abatidos do saldo devido.
- Casos contestados ou pagos não entram na fila.
- Canal preferido e tentativas recentes aparecem para revisão.
- Pagamento, promessa e acordo são tratados como estados diferentes.

## KPIs

Saldo vencido elegível; contratos por faixa de atraso; pagamentos alocados; taxa de recuperação no período; quantidade em contestação/acordo; contratos sinalizados por frequência de contato.

## Consulta SQL

Execute schema.sql e importe cobranca_demo.csv na tabela cobranca.

    WITH base AS (
      SELECT c.*,
        GREATEST(valor_devido - valor_pago_alocado, 0) AS saldo_aberto,
        data_ref - vencimento AS dias_atraso
      FROM cobranca c
    )
    SELECT contrato_id, cliente_id, vencimento, dias_atraso, saldo_aberto,
      canal_preferido, tentativas_7d, acordo_ativo,
      CASE WHEN acordo_ativo THEN 'revisar_acordo'
           WHEN tentativas_7d >= 2 THEN 'revisar_frequencia'
           ELSE 'revisar_contato' END AS acao_sugerida
    FROM base
    WHERE status = 'ABERTO' AND NOT contestado
      AND saldo_aberto > 0 AND vencimento < data_ref
    ORDER BY dias_atraso DESC, saldo_aberto DESC, vencimento ASC;

## Medidas para Power BI

Importe o CSV e renomeie a tabela para Cobranca.

    Saldo vencido elegível =
      SUMX(FILTER(Cobranca, Cobranca[status] = "ABERTO" && Cobranca[contestado] = FALSE() && Cobranca[vencimento] < Cobranca[data_ref]), Cobranca[valor_devido] - Cobranca[valor_pago_alocado])

    Contratos na fila =
      CALCULATE(DISTINCTCOUNT(Cobranca[contrato_id]), Cobranca[status] = "ABERTO", Cobranca[contestado] = FALSE())

    Pagamentos alocados = SUM(Cobranca[valor_pago_alocado])

## Limites

Não há envio automático, consulta de cadastro real, cálculo de juros ou cobrança real. Regras de privacidade, contato e acordo precisam de validação pelas áreas responsáveis.
