# FastAPI Pedidos API

Este é um projeto de API para gerenciamento de pedidos, desenvolvido com FastAPI e SQLAlchemy. A aplicação permite o cadastro de usuários, autenticação via JWT e o gerenciamento completo de pedidos e itens de pedido.

## 🚀 Funcionalidades

### Autenticação e Usuários
- **Cadastro de Usuário:** Permite criar novos usuários.
- **Login:** Autenticação por email e senha, retornando tokens de acesso (JWT) e refresh.
- **Refresh Token:** Permite renovar o token de acesso.
- **Autorização:** Controle de acesso baseado em funções (Admin vs Usuário comum).

### Pedidos
- **Criar Pedido:** Usuários autenticados podem iniciar um novo pedido.
- **Listar Pedidos:** 
  - Usuários comuns visualizam apenas seus próprios pedidos.
  - Administradores têm visão global de todos os pedidos no sistema.
- **Adicionar Itens:** Adiciona produtos ao pedido com cálculo automático de subtotal.
- **Remover Itens:** Remove produtos do pedido e atualiza o valor total automaticamente.
- **Cancelar Pedido:** Permite o cancelamento de pedidos pendentes (restrito ao dono ou admin).
- **Cálculo Automático:** O sistema recalcula o valor total do pedido a cada alteração nos itens.

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno e de alto desempenho.
- **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM para interação com o banco de dados.
- **[SQLite](https://www.sqlite.org/):** Banco de dados relacional leve (em arquivo).
- **[Pydantic](https://docs.pydantic.dev/):** Validação de dados e configurações.
- **[Jose (JWT)](https://python-jose.readthedocs.io/):** Gerenciamento de tokens de segurança.
- **[Passlib](https://passlib.readthedocs.io/):** Hashing de senhas com BCrypt.
- **[Alembic](https://alembic.sqlalchemy.org/):** Gerenciamento de migrações de banco de dados.

## 📦 Como Instalar e Rodar

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd FastAPIProjeto
```

### 2. Configurar Ambiente Virtual
```bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/macOS:
source .venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EMPIRE_MINUTES=30
```

### 5. Executar a Aplicação
O projeto está configurado para criar as tabelas automaticamente ao iniciar.
```bash
uvicorn main:app --reload
```
A API estará disponível em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa em `/docs` ou `/redoc`.

## 🧪 Testes
Para rodar os testes de autenticação:
1. Certifique-se de que o servidor está rodando.
2. Execute:
```bash
python test_auth.py
```

---
Desenvolvido como um exemplo prático de FastAPI.
