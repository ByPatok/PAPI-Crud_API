import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from pathlib import Path

# Configuração direta do banco PostgreSQL

env_path = Path(__file__).parent.parent / "db.env"
load_dotenv(env_path)

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.environ["DB_NAME"], 
            user=os.environ["DB_USER"],   
            password=os.environ["DB_PASSWORD"], 
            host=os.environ["DB_HOST"],   
            port=os.environ["DB_PORT"],    
            cursor_factory=RealDictCursor
        )
        self.cur = self.conn.cursor()

    def select_all(self):
        self.cur.execute("SELECT * FROM minha_tabela")
        return self.cur.fetchall()

    def select_by_id(self, id):
        """Get a single record by ID"""
        self.cur.execute("SELECT * FROM minha_tabela WHERE id = %s", (id,))
        return self.cur.fetchone()

    def insert_data(self, nome, idade):
        self.cur.execute("INSERT INTO minha_tabela (nome, idade) VALUES (%s, %s)", (nome, idade))
        self.conn.commit()

    def update_data(self, id, nome, idade):
        self.cur.execute("UPDATE minha_tabela SET nome = %s, idade = %s WHERE id = %s", (nome, idade, id))
        self.conn.commit()

    def delete_data(self, id):
        self.cur.execute("DELETE FROM minha_tabela WHERE id = %s", (id,))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
