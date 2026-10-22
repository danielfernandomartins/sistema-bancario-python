CREATE TABLE IF NOT EXISTS tarefas_financiamento (
    data_ref DATE NOT NULL,
    contrato_id TEXT NOT NULL,
    tarefa_id TEXT NOT NULL,
    tipo_tarefa TEXT NOT NULL,
    etapa TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ABERTA', 'EM_ANDAMENTO', 'BLOQUEADA', 'CONCLUIDA')),
    responsavel_area TEXT NOT NULL,
    criada_em DATE NOT NULL,
    prazo_em DATE NOT NULL,
    concluida_em DATE,
    bloqueio_motivo TEXT,
    retrabalho BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (data_ref, tarefa_id),
    CHECK (prazo_em >= criada_em),
    CHECK (concluida_em IS NULL OR concluida_em >= criada_em),
    CHECK (status <> 'BLOQUEADA' OR NULLIF(bloqueio_motivo, '') IS NOT NULL)
);

-- Importe tarefas_demo.csv na tabela após criar o schema.
