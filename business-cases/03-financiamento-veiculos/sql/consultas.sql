SELECT responsavel_area, etapa, COUNT(*) AS tarefas_vencidas
FROM tarefas_financiamento
WHERE status <> 'CONCLUIDA' AND prazo_em < data_ref
GROUP BY responsavel_area, etapa
ORDER BY tarefas_vencidas DESC;

SELECT tipo_tarefa,
  COUNT(*) FILTER (WHERE status = 'CONCLUIDA') AS concluidas,
  COUNT(*) FILTER (WHERE status = 'CONCLUIDA' AND concluida_em <= prazo_em) AS concluidas_no_prazo,
  ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'CONCLUIDA' AND concluida_em <= prazo_em)
    / NULLIF(COUNT(*) FILTER (WHERE status = 'CONCLUIDA'), 0), 2) AS sla_pct
FROM tarefas_financiamento
GROUP BY tipo_tarefa
ORDER BY tipo_tarefa;

SELECT tipo_tarefa, etapa, COUNT(*) AS retrabalhos
FROM tarefas_financiamento
WHERE retrabalho
GROUP BY tipo_tarefa, etapa
ORDER BY retrabalhos DESC;
