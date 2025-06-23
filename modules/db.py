import pyodbc
from datetime import datetime
import os
import json

class DataBase():
    def __init__(self, config:dict) -> None:
        self.__server = config['server']
        self.__database = config['database']
        self.__username = config['username']
        self.__password = config['password']
        self.__driver = config['driver']
        self.cursor = self.connect()

    def get_database_config(self):
        return {
            "server": self.__server,
            "database": self.__database,
            "username": self.__username,
            "password": self.__password,
            "driver": self.__driver
        }
    
    def connect(self):
        db_config = self.get_database_config()
        connection_data = f"SERVER={db_config['server']};DATABASE={db_config['database']};UID={db_config['username']};PWD={db_config['password']};DRIVER={{{db_config['driver']}}};"
        
        conn = pyodbc.connect(connection_data)
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setencoding(encoding='utf-8')

        cursor = conn.cursor()
        return cursor

    def close(self):
        self.cursor.close()
        

    def _drop_table(self, table_name):
        self.cursor.execute(f"""DROP TABLE IF EXISTS {table_name};""")
        self.cursor.commit()

    def _drop_all_tables(self):
        # Primeiro, buscar todos os nomes das tabelas no esquema público
        self.cursor.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public';
        """)
        
        tables = self.cursor.fetchall()
        
        # Apagar cada tabela individualmente
        for table in tables:
            table_name = table[0]
            drop_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
            self.cursor.execute(drop_query)
            print(f"Tabela {table_name} apagada com sucesso.")

        # Confirma as alterações no banco de dados
        self.cursor.commit()

    def _erase_table(self, table_name):
        self.cursor.execute(f"""DELETE FROM {table_name};""")
        self.cursor.commit()

    def select_table(self, table_name):
        self.cursor.execute(f"""SELECT * FROM {table_name};""")
        return self.cursor.fetchall()

    def save_news(self, all_news):
        # Abre conexão e cursor

        insert_sql = """
            INSERT INTO noticias (
                img_url,
                data_publicacao,
                titulo,
                link,
                descricao_parcial,
                descricao_completa
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (link) DO NOTHING
        """

        for item in all_news:
            # Converte data (string) para datetime.date
            data = None
            if item['date']:
                try:
                    data = datetime.strptime(item['date'], '%d/%m/%Y').date()
                except ValueError:
                    # Tente outros formatos ou ignore
                    pass

            params = (
                item.get('img'),
                data,
                item.get('title'),
                item.get('link'),
                item.get('partial_description'),
                item.get('description')
            )

            self.cursor.execute(insert_sql, params)

        # Confirma e fecha
        self.cursor.commit()
        self.cursor.close()
        print(f"[INFO] Inseridas/atualizadas {len(all_news)} notícias.")

# Exemplo de uso:
if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    db = DataBase(config)
    # Supondo que all_news já foi preenchido pelo seu scraper
    all_news = [
        {
            'img': 'https://...',
            'date': '12/06/2025',
            'title': 'Exemplo de notícia',
            'link': 'https://...',
            'partial_description': 'Resumo...',
            'description': 'Conteúdo completo...'
        },
    ]
    # db.save_news(all_news)
    news = db.select_table('noticias')
    print(news)