import json
import pyodbc

# 1) Carrega configuração
with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)['database']

DRIVER   = cfg['driver']      # ex: "PostgreSQL Unicode"
SERVER   = cfg['server']      # ex: "localhost"
USER     = cfg['username']
PASSWORD = cfg['password']
PORT     = cfg.get('port', 5432)

# String de conexão genérica
def conn_str(db):
    return (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"PORT={PORT};"
        f"DATABASE={db};"
        f"UID={USER};"
        f"PWD={PASSWORD};"
    )

# 2) Conecta em 'postgres' e cria o database 'noticias'
cnxn = pyodbc.connect(conn_str('postgres'))
cnxn.autocommit = True   # necessário para CREATE DATABASE fora de transação
csr = cnxn.cursor()
try:
    csr.execute('CREATE DATABASE noticias;')
    print("[INFO] Banco 'noticias' criado com sucesso.")
except Exception as e:
    # se já existir, ignora
    print(f"[INFO] Ao criar DB: {e}")
finally:
    csr.close()
    cnxn.close()

# 3) Conecta em 'noticias' e cria extensão + tabela
cnxn = pyodbc.connect(conn_str('noticias'))
cnxn.autocommit = False
csr = cnxn.cursor()

# cria extensão uuid-ossp
csr.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

# DDL da tabela
create_sql = '''
CREATE TABLE IF NOT EXISTS noticias (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    img_url TEXT,
    data_publicacao DATE,
    original_date TEXT,
    titulo TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,
    descricao_parcial TEXT,
    descricao_completa TEXT,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);
'''

csr.execute(create_sql)
cnxn.commit()
print("[INFO] Tabela 'noticias' criada com sucesso em DB 'noticias'.")

csr.close()
cnxn.close()
