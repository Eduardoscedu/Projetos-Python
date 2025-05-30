🌱 Sistema de Login com Controle de Irrigação - Tkinter + SQLite
Este projeto é uma aplicação gráfica (GUI) em Python que simula um Sistema de Login com Controle de Irrigação, utilizando Tkinter para a interface e SQLite para armazenamento dos dados. É ideal para fins educacionais, projetos de IoT simulados ou como base para sistemas com controle por acesso.

🧩 Funcionalidades
✅ Tela de login com autenticação
✅ Tela de registro com validação por key de acesso
✅ Painel principal com:

✅ Ligar / Desligar o sistema de irrigação

✅ Verificação de status da irrigação

✅ Identificação de nível de acesso do usuário
✅ Interface amigável com status visual
✅ Banco de dados criado e alimentado automaticamente

📋 Tecnologias Utilizadas
Python 3

Tkinter (GUI)

SQLite3 (banco de dados local)

📁 Estrutura do Projeto
bash
Copiar
Editar
├── main.py              # Inicia a aplicação Tkinter
├── gui.py               # Interface e lógica de controle do sistema
├── banco.py             # Conexão e criação do banco de dados
└── sistema.db           # Arquivo gerado automaticamente com as tabelas
🧠 Lógica de Funcionamento
Acesso de Usuários
Registro: o usuário precisa de uma key válida:

KEY-123 → acesso USUARIO

KEY-456 → acesso DEV

KEY-789 → acesso ADM

Login: após se registrar, o usuário pode fazer login e será redirecionado a um painel personalizado conforme seu nível de acesso.

Painel de Irrigação
Todos os usuários podem ativar/desativar a irrigação.

Níveis DEV e ADM têm acesso ao botão Verificação, que mostra o estado atual da irrigação.

O status da irrigação é exibido em tempo real com cores:

Verde: Irrigação Ligada

Vermelho: Irrigação Desligada

🧪 Banco de Dados
Tabela usuarios
Campo	Tipo	Descrição
id	INTEGER	Chave primária
nome	TEXT	Nome de usuário (único)
senha	TEXT	Senha do usuário
nivel_acesso	TEXT	Nível de acesso (USUARIO/DEV/ADM)
botao_apertado	INTEGER	Estado do botão de irrigação

Tabela keys_acesso
Campo	Tipo	Descrição
id	INTEGER	Chave primária
key	TEXT	Chave de acesso única
nivel_acesso	TEXT	Nível vinculado à key

🚀 Como Executar o Projeto
Clonar o repositório

bash
Copiar
Editar
git clone https://github.com/seuusuario/sistema-irrigacao
cd sistema-irrigacao
Executar o projeto

bash
Copiar
Editar
python main.py
Pronto! O sistema será aberto com a interface gráfica.


