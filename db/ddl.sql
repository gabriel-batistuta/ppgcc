-- Primeiro crie a extensão OID para usar UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE DATABASE "noticias";

-- Tabela de notícias
CREATE TABLE noticias (
    id                  UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
    img_url             TEXT      NULL,
    data_publicacao     DATE      NULL,
    titulo              TEXT      NOT NULL,
    link                TEXT      NOT NULL UNIQUE,
    descricao_parcial   TEXT      NULL,
    descricao_completa  TEXT      NULL,
    criado_em           TIMESTAMP NOT NULL DEFAULT NOW()
);