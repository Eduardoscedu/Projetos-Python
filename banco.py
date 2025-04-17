import sqlite3

def conectar_banco():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT NOT NULL,
        botao_apertado INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keys_acesso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        nivel_acesso TEXT NOT NULL
    )
    ''')

    keys_validas = [
        ('KEY-123', 'USUARIO'),
        ('KEY-456', 'DEV'),
        ('KEY-789', 'ADM'),
    ]

    for key, nivel in keys_validas:
        cursor.execute("SELECT * FROM keys_acesso WHERE key = ?", (key,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO keys_acesso (key, nivel_acesso) VALUES (?, ?)", (key, nivel))

    conn.commit()
    return conn, cursor
