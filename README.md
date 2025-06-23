# ppgcc

# Database
```bash
# instale as dependências
sudo apt install -y postgresql unixodbc unixodbc-dev odbc-postgresql
```

```SQL
-- no postgress
CREATE DATABASE "noticias";
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