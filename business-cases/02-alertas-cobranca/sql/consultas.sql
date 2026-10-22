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

SELECT CASE
  WHEN data_ref - vencimento BETWEEN 1 AND 7 THEN '01-07'
  WHEN data_ref - vencimento BETWEEN 8 AND 30 THEN '08-30'
  WHEN data_ref - vencimento BETWEEN 31 AND 60 THEN '31-60'
  ELSE '61+'
  END AS faixa_atraso,
  COUNT(*) AS contratos,
  SUM(GREATEST(valor_devido - valor_pago_alocado, 0)) AS saldo_aberto
FROM cobranca
WHERE status = 'ABERTO' AND NOT contestado AND vencimento < data_ref
GROUP BY 1
ORDER BY 1;
