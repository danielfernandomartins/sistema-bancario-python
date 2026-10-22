# 03 — Rotina operacional de financiamento de veículos

**Natureza:** projeto de estudo/portfólio. **Dados:** sintéticos. **Tecnologias:** PostgreSQL, SQL, Power BI/DAX.

## Problema e objetivo

Pendências documentais e tarefas espalhadas podem dificultar a visibilidade do andamento. A proposta organiza conferência documental, validação dos dados do veículo, solicitação de correção, preparação contratual e acompanhamento de assinatura em uma fila rastreável. O estudo não avalia crédito nem decide aprovação.

## História do usuário

Como analista de operações, quero acompanhar tarefas por contrato, etapa, responsável e prazo, para resolver pendências na ordem correta e dar visibilidade ao processo.

## Novas tarefas propostas

- Conferir completude e legibilidade dos documentos recebidos.
- Validar consistência dos dados do veículo e da proposta contra fonte autorizada.
- Registrar pendência e indicar origem e responsável pela correção.
- Confirmar recebimento de correção e reprocessar validação.
- Preparar pacote contratual para revisão.
- Acompanhar assinatura, devolução ou exceção.
- Encerrar cada tarefa com status, data e motivo auditáveis.

## Regras e critérios de aceite

- Estados válidos: ABERTA, EM_ANDAMENTO, BLOQUEADA e CONCLUIDA.
- Tarefa bloqueada exige motivo; fila mostra próxima ação e área responsável.
- SLA é parâmetro acordado por tipo de tarefa, não constante universal.
- Retrabalho é registrado quando tarefa concluída retorna para correção.
- Tarefa vencida sinaliza exceção operacional; não altera crédito, preço ou aprovação.
- Geração de tarefas obrigatórias deve ser idempotente por contrato e etapa.

## KPIs

Tempo de ciclo; percentual de conclusão no prazo; tarefas vencidas; bloqueios por etapa e área; retrabalho por tipo de tarefa; backlog por responsável.

## Consulta SQL

Execute schema.sql e importe tarefas_demo.csv na tabela tarefas_financiamento.

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
    GROUP BY tipo_tarefa;

## Medidas para Power BI

Importe o CSV e renomeie a tabela para TarefasFinanciamento.

    Tarefas abertas vencidas =
      CALCULATE(COUNTROWS(TarefasFinanciamento), TarefasFinanciamento[status] <> "CONCLUIDA", TarefasFinanciamento[prazo_em] < TarefasFinanciamento[data_ref])

    Tarefas concluídas =
      CALCULATE(COUNTROWS(TarefasFinanciamento), TarefasFinanciamento[status] = "CONCLUIDA")

    Concluídas no prazo =
      CALCULATE(COUNTROWS(TarefasFinanciamento), TarefasFinanciamento[status] = "CONCLUIDA", TarefasFinanciamento[concluida_em] <= TarefasFinanciamento[prazo_em])

    SLA de conclusão = DIVIDE([Concluídas no prazo], [Tarefas concluídas])

    Tarefas com retrabalho =
      CALCULATE(COUNTROWS(TarefasFinanciamento), TarefasFinanciamento[retrabalho] = TRUE())

## Limites

SLA, catálogo de tarefas e responsabilidades são hipóteses a validar. Qualquer implementação real exigiria aprovação da operação, crédito, privacidade, segurança e arquitetura. O exemplo usa identificadores fictícios e não altera decisões de crédito.
