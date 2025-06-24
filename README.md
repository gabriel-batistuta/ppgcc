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