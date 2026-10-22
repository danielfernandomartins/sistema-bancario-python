WITH base AS (
  SELECT i.*,
    GREATEST(saldo_medio_30d - saldo_minimo_30d - 500.00, 0) AS saldo_potencial
  FROM investimentos i
)
SELECT data_ref, segmento, cliente_id, saldo_potencial,
  (suitability_validada AND consentimento_contato AND saldo_potencial >= 500) AS elegivel
FROM base
ORDER BY data_ref, segmento, cliente_id;

-- Exposição e aceite. Aceite não significa aplicação liquidada.
SELECT data_ref,
  COUNT(*) FILTER (WHERE oferta_exibida) AS ofertas_exibidas,
  COUNT(*) FILTER (WHERE oferta_aceita) AS ofertas_aceitas,
  ROUND(100.0 * COUNT(*) FILTER (WHERE oferta_aceita)
    / NULLIF(COUNT(*) FILTER (WHERE oferta_exibida), 0), 2) AS taxa_aceite_pct
FROM investimentos
GROUP BY data_ref
ORDER BY data_ref;
