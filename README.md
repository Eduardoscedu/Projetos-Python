# 💧 Sistema de Login com Controle de Irrigação

Sistema desenvolvido em **Python + Tkinter + SQLite**, com autenticação por níveis de acesso e simulação de irrigação. Ideal para fins educacionais ou como base para projetos de automação.

---

## 🚀 Funcionalidades

- 🔐 Tela de **Login**
- 📝 Tela de **Cadastro** com validação por **chave de acesso**
- 📊 Painel do usuário com:
  - ✅ Controle de irrigação (ligar/desligar)
  - 🔍 Verificação de status (para níveis `DEV` e `ADM`)
  - 🌡️ Indicador visual de status (verde/vermelho)
- 🗂️ Banco de dados SQLite criado automaticamente
- 🔑 Três níveis de acesso:
  - `USUARIO`
  - `DEV`
  - `ADM`

---

## 🖥️ Tecnologias Utilizadas

- 🐍 Python 3
- 🧰 Tkinter (interface gráfica)
- 🗃️ SQLite (banco de dados local)

---

## 📁 Estrutura de Arquivos

```
📦 sistema-irrigacao/
├── main.py          # Inicializa a aplicação
├── gui.py           # Interface e lógica do sistema
├── banco.py         # Conexão e criação do banco de dados
└── sistema.db       # (Gerado automaticamente)
```

---

## 🧠 Como Funciona

### 🔑 Registro

Usuários só podem se registrar se tiverem uma **key válida** (pré-cadastrada no banco):

| Key       | Nível de Acesso |
|-----------|-----------------|
| KEY-123   | USUARIO         |
| KEY-456   | DEV             |
| KEY-789   | ADM             |

---

### 🔐 Login

Após registro, o usuário faz login e acessa o painel conforme seu nível.

---

### 🧪 Painel de Controle

- **Todos os usuários**:
  - Ligar ou desligar irrigação (altera o valor `botao_apertado`)
- **Níveis DEV e ADM**:
  - Verificam status atual (ligado/desligado)
- **Status visual**:
  - 🟢 Verde = Irrigação Ligada
  - 🔴 Vermelho = Irrigação Desligada

---

## 🗄️ Estrutura do Banco de Dados

### Tabela `usuarios`

| Campo          | Tipo     | Descrição                    |
|----------------|----------|------------------------------|
| id             | INTEGER  | Chave primária              |
| nome           | TEXT     | Nome do usuário (único)     |
| senha          | TEXT     | Senha do usuário            |
| nivel_acesso   | TEXT     | USUARIO / DEV / ADM         |
| botao_apertado | INTEGER  | 0 = desligado, 1 = ligado   |

### Tabela `keys_acesso`

| Campo        | Tipo     | Descrição                |
|--------------|----------|--------------------------|
| id           | INTEGER  | Chave primária          |
| key          | TEXT     | Chave única de acesso   |
| nivel_acesso | TEXT     | Nível associado à chave |

---

## ▶️ Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seuusuario/sistema-irrigacao
   cd sistema-irrigacao
   ```

2. **Execute o projeto:**
   ```bash
   python main.py
   ```

3. A aplicação abrirá com a interface gráfica.

---

## ✨ Melhorias Futuras

- ⏱️ Timer de irrigação com duração personalizada
- 🔐 Criptografia de senhas (com `hashlib`)
- 🌎 Integração com dispositivos físicos (como Raspberry Pi)
- 📈 Histórico de ações dos usuários

---

## 🧑‍💻 Autor

Desenvolvido por [Eduardo]  

---

> ⭐ Dê uma estrela ⭐ neste projeto se ele te ajudou ou serviu de inspiração!
