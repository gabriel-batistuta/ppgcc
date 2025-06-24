# ppgcc

# Credentials
```json
{
    "database": {
        "server":"localhost",
        "database":"DATABASENAME",
        "username":"postgres",
        "password":"PASSWORD",
        "driver":"psqlodbcw.so"
    },
    "telegram": {
        "token":"BOT TOKEN",
        "chatId":"CHANNEL_ID"
    },
    "log": {
        "email-sender":"emailsender@gmail.com",
        "app-password":"APP PASSWORD",
        "email-receiver":[
            "emailreceiver@gmail.com",
            "emailreceiver2@gmail.com"
        ]
    }
}
```

# Database
```bash
# instale as dependências
sudo apt install -y postgresql unixodbc unixodbc-dev odbc-postgresql
```

```SQL
-- no postgress
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE DATABASE "noticias";

\c noticias

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
```

```bash
python migrate.py
```

```json
// config.json:
{
    "server":"localhost",
    "database":"noticias",
    "username":"postgres",
    "password":"YourPassword",
    "driver":"psqlodbcw.so"
}
```