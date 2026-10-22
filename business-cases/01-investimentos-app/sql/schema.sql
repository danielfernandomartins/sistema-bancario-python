CREATE TABLE IF NOT EXISTS investimentos (
    data_ref DATE NOT NULL,
    cliente_id TEXT NOT NULL,
    segmento TEXT NOT NULL,
    saldo_medio_30d NUMERIC(14,2) NOT NULL CHECK (saldo_medio_30d >= 0),
    saldo_minimo_30d NUMERIC(14,2) NOT NULL CHECK (saldo_minimo_30d >= 0),
    valor_aplicado NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (valor_aplicado >= 0),
    oferta_exibida BOOLEAN NOT NULL DEFAULT FALSE,
    oferta_aceita BOOLEAN NOT NULL DEFAULT FALSE,
    suitability_validada BOOLEAN NOT NULL DEFAULT FALSE,
    consentimento_contato BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (data_ref, cliente_id),
    CHECK (saldo_minimo_30d <= saldo_medio_30d),
    CHECK (NOT oferta_aceita OR oferta_exibida)
);

-- Importe investimentos_demo.csv na tabela após criar o schema.
