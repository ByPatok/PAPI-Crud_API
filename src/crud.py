import psycopg2
from psycopg2.extras import RealDictCursor

# Configuração direta do banco PostgreSQL
DB_NAME = "learningbase"
DB_USER = "postgres"
DB_PASSWORD = "quack"
DB_HOST = "localhost"
DB_PORT = "5432"

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
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
