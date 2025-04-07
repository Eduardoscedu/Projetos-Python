import sqlite3
import tkinter as tk
import time
from tkinter import messagebox
import os

# Conectar ou criar banco
def conectar_banco():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()

    # Cria tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT NOT NULL
    )
    ''')

    # Cria tabela de keys
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keys_acesso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        nivel_acesso TEXT NOT NULL
    )
    ''')

    # Insere as keys válidas se ainda não existirem
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


class SistemaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Login com SQLite")

        # Conecta e inicializa o banco
        self.conn, self.cursor = conectar_banco()

        self.tela_principal()

    def limpar_tela(self):
        for widget in self.master.winfo_children():
            widget.destroy()
      
    def irrigar(self):
        self.cursor.execute("SELECT * FROM usuarios WHERE botao_apertado = 1")
        resultado = self.cursor.fetchone()

        if resultado:
            self.cursor.execute("UPDATE usuarios SET botao_apertado = 0 WHERE botao_apertado = 1")
            messagebox.showinfo("Desligando", "Irrigação Parada!")
        else:
            self.cursor.execute("UPDATE usuarios SET botao_apertado = 1 WHERE botao_apertado = 0")
            messagebox.showinfo("Irrigando", "Irrigação Iniciada!")

    def verificacao(self):
        self.cursor.execute("SELECT * FROM usuarios WHERE botao_apertado = 1")
        resultado_verific = self.cursor.fetchone()
    
        if resultado_verific:
            messagebox.showinfo("Irrigando", "A Irrigação esta em Funcionamento!!")
        else:
             messagebox.showinfo("Desligada", "A Irrigação esta Desligada!!")

           

    def tela_principal(self):
        self.limpar_tela()
        tk.Label(self.master, text="Bem-vindo!", font=('Arial', 16)).pack(pady=10)
        tk.Button(self.master, text="Login", width=20, command=self.tela_login).pack(pady=5)
        tk.Button(self.master, text="Registrar", width=20, command=self.tela_registro).pack(pady=5)
        tk.Button(self.master, text="Sair", width=20, command=self.master.quit).pack(pady=5)

    def tela_login(self):
        self.limpar_tela()
        tk.Label(self.master, text="Login", font=('Arial', 14)).pack(pady=10)
        tk.Label(self.master, text="Usuário").pack()
        usuario_entry = tk.Entry(self.master)
        usuario_entry.pack()

        tk.Label(self.master, text="Senha").pack()
        senha_entry = tk.Entry(self.master, show="*")
        senha_entry.pack()

        def tentar_login():
            nome = usuario_entry.get()
            senha = senha_entry.get()

            self.cursor.execute("SELECT nivel_acesso FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
            resultado = self.cursor.fetchone()

            if resultado:
                nivel = resultado[0]
                self.tela_painel(nome, nivel)
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")

        tk.Button(self.master, text="Entrar", command=tentar_login).pack(pady=10)
        tk.Button(self.master, text="Voltar", command=self.tela_principal).pack()

    def tela_registro(self):
        self.limpar_tela()
        tk.Label(self.master, text="Registrar", font=('Arial', 14)).pack(pady=10)

        tk.Label(self.master, text="Usuário").pack()
        usuario_entry = tk.Entry(self.master)
        usuario_entry.pack()

        tk.Label(self.master, text="Senha").pack()
        senha_entry = tk.Entry(self.master, show="*")
        senha_entry.pack()

        tk.Label(self.master, text="Key de Acesso").pack()
        key_entry = tk.Entry(self.master)
        key_entry.pack()

        def tentar_registro():
            nome = usuario_entry.get()
            senha = senha_entry.get()
            key = key_entry.get()

            self.cursor.execute("SELECT nivel_acesso FROM keys_acesso WHERE key = ?", (key,))
            resultado = self.cursor.fetchone()

            if resultado:
                nivel = resultado[0]
                try:
                    self.cursor.execute("INSERT INTO usuarios (nome, senha, nivel_acesso) VALUES (?, ?, ?)",
                                        (nome, senha, nivel))
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", f"Registrado com acesso: {nivel}")
                    self.tela_principal()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Erro", "Nome de usuário já existe.")
            else:
                messagebox.showerror("Erro", "Key inválida.")

        tk.Button(self.master, text="Registrar", command=tentar_registro).pack(pady=10)
        tk.Button(self.master, text="Voltar", command=self.tela_principal).pack()

    def tela_painel(self, nome, nivel):
        self.limpar_tela()
        tk.Label(self.master, text=f"Bem-vindo, {nome}!", font=('Arial', 14)).pack(pady=10)
        tk.Label(self.master, text=f"Acesso: {nivel}", font=('Arial', 12)).pack(pady=5)

        if nivel == 'USUARIO':
            tk.Label(self.master, text="Painel de USUÁRIO").pack(pady=5)
        elif nivel == 'DEV':
            tk.Label(self.master, text="Painel de DEV - em desenvolvimento").pack(pady=5)
        elif nivel == 'ADM':
            tk.Label(self.master, text="Painel de ADMINISTRADOR 👑").pack(pady=5)

        tk.Button(self.master, text=f"Ligar/Desligar", command=self.irrigar).pack(pady=10)
        tk.Button(self.master, text=f"Verificação", command=self.verificacao).pack(pady=10)
        tk.Button(self.master, text="Sair", command=self.tela_principal).pack(pady=10)



# Execução principal
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x350")
    app = SistemaGUI(root)
    root.mainloop()
