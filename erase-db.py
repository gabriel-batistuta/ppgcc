import modules as md
import json

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    db = md.DataBase(config['database'])
    db._drop_all_tables()
    db._create_table()
    
    print("Banco de dados apagado com sucesso!")