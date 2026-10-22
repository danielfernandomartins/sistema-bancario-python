CREATE TABLE IF NOT EXISTS cobranca (
    data_ref DATE NOT NULL,
    contrato_id TEXT NOT NULL,
    cliente_id TEXT NOT NULL,
    vencimento DATE NOT NULL,
    valor_devido NUMERIC(14,2) NOT NULL CHECK (valor_devido >= 0),
    valor_pago_alocado NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (valor_pago_alocado >= 0),
    status TEXT NOT NULL CHECK (status IN ('ABERTO', 'PAGO', 'ACORDO', 'CONTESTADO')),
    canal_preferido TEXT NOT NULL CHECK (canal_preferido IN ('APP', 'EMAIL', 'TELEFONE')),
    tentativas_7d INTEGER NOT NULL DEFAULT 0 CHECK (tentativas_7d >= 0),
    contestado BOOLEAN NOT NULL DEFAULT FALSE,
    acordo_ativo BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (data_ref, contrato_id),
    CHECK (valor_pago_alocado <= valor_devido)
);

-- Importe cobranca_demo.csv na tabela após criar o schema.
