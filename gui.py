import tkinter as tk
from tkinter import messagebox
from banco import conectar_banco



class SistemaGUI:
    def __init__(self, master):
        self.status_label = None
        self.master = master
        master.title("Sistema de Login com SQLite")

        self.conn, self.cursor = conectar_banco()
        self.tela_principal()

    def limpar_tela(self):
        for widget in self.master.winfo_children():
            widget.destroy()

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
            self.status_label.config(text="Status: Ligado", bg="green")
        else:
            self.status_label.config(text="Status: Desligado", bg="red")

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
                self.tela_painel(nome, resultado[0])
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
                    self.cursor.execute(
                        "INSERT INTO usuarios (nome, senha, nivel_acesso) VALUES (?, ?, ?)",
                        (nome, senha, nivel)
                    )
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", f"Registrado com acesso: {nivel}")
                    self.tela_principal()
                except:
                    messagebox.showerror("Erro", "Nome de usuário já existe.")
            else:
                messagebox.showerror("Erro", "Key inválida.")

        tk.Button(self.master, text="Registrar", command=tentar_registro).pack(pady=10)
        tk.Button(self.master, text="Voltar", command=self.tela_principal).pack()

    def tela_painel(self, nome, nivel):
        self.limpar_tela()
        tk.Label(self.master, text=f"Bem-vindo, {nome}!", font=('Arial', 14)).pack(pady=10)
        tk.Label(self.master, text=f"Acesso: {nivel}", font=('Arial', 12)).pack(pady=5)
        tk.Button(self.master, text="Ligar/Desligar", command=self.irrigar).pack(pady=10)
        if nivel in ['DEV', 'ADM']:
            tk.Button(self.master, text="Verificação", command=self.verificacao).pack(pady=10)
        tk.Button(self.master, text="Sair", command=self.tela_principal).pack(pady=10)
        self.status_label = tk.Label(self.master, text="Status: Desconhecido", font=("Arial", 12), width=20)
        self.status_label.pack(pady=10)
        #Fazer o Timer de irrigação
        self.timer_label = tk.Label(self.master, text="")

        self.verificacao_cor()

        

