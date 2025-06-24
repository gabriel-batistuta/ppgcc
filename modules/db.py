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

    def _create_table(self):
        """Cria a tabela 'noticias' no banco PostgreSQL, com UUID e extensão uuid-ossp."""
        # Habilita extensão para UUID
        self.cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        # Criação da tabela
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
        self.cursor.execute(create_sql)
        self.cursor.commit()
        print("[INFO] Tabela 'noticias' criada com sucesso.")

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

    def link_exists(self, link: str) -> bool:
        """Verifica se já existe uma notícia com o mesmo link."""
        self.cursor.execute("SELECT 1 FROM noticias WHERE link = ?", (link,))
        return self.cursor.fetchone() is not None

    def save_news(self, all_news):

        new_news = [

        ]

        """Insere uma lista de notícias, pulando links já existentes."
        """
        # Novo insert: adiciona data_publicacao (hoje) e original_date (string)
        insert_sql = """
            INSERT INTO noticias (
                img_url,
                data_publicacao,
                original_date,
                titulo,
                link,
                descricao_parcial,
                descricao_completa
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        inserted_count = 0
        today = datetime.today().date()

        for item in all_news:
            link = item.get('link')
            if not link:
                print("[WARNING] Link ausente. Ignorando item.")
                continue
            if self.link_exists(link):
                print(f"[INFO] Link já existe: {link}. Pulando...")
                continue

            new_news.append(item)
            
            # original date string
            original_date = item.get('date')

            # converte para data_publicacao: hoje
            data_pub = today

            params = (
                item.get('img'),
                data_pub,
                original_date,
                item.get('title'),
                link,
                item.get('partial_description'),
                item.get('description')
            )
            self.cursor.execute(insert_sql, params)
            inserted_count += 1

        self.cursor.commit()
        print(f"[INFO] Inseridas {inserted_count} novas notícias (duplicados ignorados).")
        
        return new_news


# Exemplo de uso:
if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    db = DataBase(config['database'])

    """ SELECT -> """
    
    # noticias = db.select_table('noticias')
    # print(f"[INFO] Total de notícias ({len(noticias)}) na tabela: {noticias}")


    """ INSERT-> """
    
    # all_news = [
    #     {
    #         'img': 'https://...',
    #         'date': '12/06/2025',
    #         'title': 'Exemplo de notícia',
    #         'link': 'https://...',
    #         'partial_description': 'Resumo...',
    #         'description': 'Conteúdo completo...'
    #     },
    # ]
    # # db.save_news(all_news)
    # news = db.select_table('noticias')
    # print(news)