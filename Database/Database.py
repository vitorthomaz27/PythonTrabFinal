import sqlite3

def connect_to_database():
    conn = sqlite3.connect(r'Dados.db') 
    return conn

def create_users_table():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Criação da tabela users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_users_table()