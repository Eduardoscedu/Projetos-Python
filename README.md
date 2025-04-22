Bom dia!
Bom  man fiz esta alteração no códgo main ve oque acha

Imagem para colocar como avatar.png este é o link https://sdmntprsouthcentralus.oaiusercontent.com/files/00000000-1f78-61f7-953f-771a33c946b7/raw?se=2025-04-22T12%3A41%3A03Z&sp=r&sv=2024-08-04&sr=b&scid=ab0c2063-fb2d-570f-ac80-9fccd3587ad3&skoid=ae70be19-8043-4428-a990-27c58b478304&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-22T04%3A31%3A12Z&ske=2025-04-23T04%3A31%3A12Z&sks=b&skv=2024-08-04&sig=GYkmO7kd044xJzzNWkb3htiIiuVfPZluySPA3LU0o6I%3D
Joguei no gpt para ele comentar oque eu alterei porém ele é meio burro e fez merda kkkkk mas acho que esta funcional testa ai
-------------------------------------------Main.py-------------------------------------
import tkinter as tk
from gui import SistemaGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    root.resizable(False, False)
    app = SistemaGUI(root)
    root.mainloop()
---------------------------------------------Banco.py----------------------------------
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

-------------------------------------------Gui.py-------------------------------
import tkinter as tk
from tkinter import messagebox
from banco import conectar_banco

class SistemaGUI:
    def __init__(self, master):
        self.status_label = None
        self.master = master
        master.title("Login System")

        self.conn, self.cursor = conectar_banco()
        self.tela_login()

    def limpar_tela(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def estilo_basico(self):
        self.master.configure(bg='#b0c4de')  # azul acinzentado

    def tela_login(self):
        self.limpar_tela()
        self.estilo_basico()

        container = tk.Frame(self.master, bg='#2a4d69', bd=0)
        container.place(relx=0.5, rely=0.5, anchor='center', width=320, height=420)

        # Avatar
        avatar = tk.Canvas(container, width=80, height=80, bg='#2a4d69', highlightthickness=0)
        avatar.create_oval(10, 10, 70, 70, outline='white', width=2)
        avatar.place(relx=0.5, rely=0.1, anchor='center')

        # Campos
        def campo(placeholder, show=None):
            entry = tk.Entry(container, font=('Arial', 12), fg='white', bg='#4b6584', insertbackground='white', relief='flat', show=show)
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == placeholder else None)
            entry.bind("<FocusOut>", lambda e: entry.insert(0, placeholder) if entry.get() == '' else None)
            entry.pack(pady=10, ipady=6, ipadx=10, fill='x', padx=30)
            return entry

        usuario_entry = campo("Email ID")
        senha_entry = campo("Password", show="*")

        lembrar_var = tk.IntVar()
        tk.Checkbutton(container, text="Remember me", variable=lembrar_var, bg='#2a4d69', fg='white').pack(pady=(10, 5))

        def tentar_login():
            nome = usuario_entry.get()
            senha = senha_entry.get()
            self.cursor.execute("SELECT nivel_acesso FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
            resultado = self.cursor.fetchone()
            if resultado:
                self.tela_painel(nome, resultado[0])
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")

        tk.Button(container, text="LOGIN", command=tentar_login, font=('Arial', 12, 'bold'),
                  bg='#1e3799', fg='white', activebackground='#3c6382', relief='flat',
                  height=2, width=20).pack(pady=(20, 10))

        tk.Button(container, text="Registrar", command=self.tela_registro, bg='#2a4d69',
                  fg='white', relief='flat').pack()

    def tela_registro(self):
        self.limpar_tela()
        self.estilo_basico()

        container = tk.Frame(self.master, bg='#2a4d69', bd=0)
        container.place(relx=0.5, rely=0.5, anchor='center', width=320, height=450)

        tk.Label(container, text="Registrar", font=('Arial', 16, 'bold'), bg='#2a4d69', fg='white').pack(pady=10)

        usuario_entry = self.criar_campo(container, "Usuário")
        senha_entry = self.criar_campo(container, "Senha", show="*")
        key_entry = self.criar_campo(container, "Key de Acesso")

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
                    self.tela_login()
                except:
                    messagebox.showerror("Erro", "Nome de usuário já existe.")
            else:
                messagebox.showerror("Erro", "Key inválida.")

        tk.Button(container, text="Registrar", command=tentar_registro, font=('Arial', 12),
                  bg='#1e3799', fg='white', relief='flat', height=2).pack(pady=15)
        tk.Button(container, text="Voltar", command=self.tela_login, bg='#2a4d69', fg='white',
                  relief='flat').pack()

    def criar_campo(self, parent, placeholder, show=None):
        entry = tk.Entry(parent, font=('Arial', 12), fg='white', bg='#4b6584',
                         insertbackground='white', relief='flat', show=show)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == placeholder else None)
        entry.bind("<FocusOut>", lambda e: entry.insert(0, placeholder) if entry.get() == '' else None)
        entry.pack(pady=10, ipady=6, ipadx=10, fill='x', padx=30)
        return entry

    def tela_painel(self, nome, nivel):
        self.limpar_tela()
        self.master.configure(bg='#34495e')

        tk.Label(self.master, text=f"Bem-vindo, {nome}!", font=('Arial', 16), bg='#34495e', fg='white').pack(pady=10)
        tk.Label(self.master, text=f"Acesso: {nivel}", font=('Arial', 12), bg='#34495e', fg='white').pack(pady=5)

        tk.Button(self.master, text="Ligar/Desligar", command=self.irrigar,
                  font=('Arial', 12), bg='#1abc9c', fg='white').pack(pady=10)

        if nivel in ['DEV', 'ADM']:
            tk.Button(self.master, text="Verificação", command=self.verificacao,
                      font=('Arial', 12), bg='#3498db', fg='white').pack(pady=10)

        tk.Button(self.master, text="Sair", command=self.tela_login,
                  font=('Arial', 12), bg='#e74c3c', fg='white').pack(pady=10)

        self.status_label = tk.Label(self.master, text="Status: Desconhecido",
                                     font=("Arial", 12), bg='#34495e', fg='white')
        self.status_label.pack(pady=10)

        self.verificacao_cor()

    def irrigar(self):
        self.cursor.execute("SELECT * FROM usuarios WHERE botao_apertado = 1")
        if self.cursor.fetchone():
            self.cursor.execute("UPDATE usuarios SET botao_apertado = 0 WHERE botao_apertado = 1")
            messagebox.showinfo("Desligando", "❌❌ Irrigação Parada!! ❌❌")
        else:
            self.cursor.execute("UPDATE usuarios SET botao_apertado = 1 WHERE botao_apertado = 0")
            messagebox.showinfo("Irrigando", "🚿🚿 Irrigação Iniciada!! 🚿🚿")
        self.verificacao_cor()
        self.conn.commit()

    def verificacao(self):
        self.cursor.execute("SELECT * FROM usuarios WHERE botao_apertado = 1")
        if self.cursor.fetchone():
            messagebox.showinfo("Irrigando", "🚿🚿 A Irrigação está em funcionamento!! 🚿🚿")
        else:
            messagebox.showinfo("Desligada", "❌❌ A Irrigação está desligada!! ❌❌")

    def verificacao_cor(self):
        self.cursor.execute("SELECT * FROM usuarios WHERE botao_apertado = 1")
        resultado = self.cursor.fetchone()
        if resultado:
            self.status_label.config(text="Status: Ligado", bg="#2ecc71")
        else:
            self.status_label.config(text="Status: Desligado", bg="#e74c3c")

