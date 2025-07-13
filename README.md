# 📒 Projeto: Agenda de Contatos

Aplicação web para cadastro, edição, visualização e gerenciamento de contatos pessoais com autenticação de usuários.

---

## ✅ Funcionalidades

- Cadastro de usuários  
- Login e logout  
- CRUD de contatos  
- Upload de imagem do contato  
- Paginação e busca  
- Templates com Bootstrap  

---

## 💻 Tecnologias Utilizadas

- Python 3.x  
- Django  
- SQLite (banco padrão do Django)  
- Bootstrap (para estilização)  
- Pillow (para upload de imagens)  

---

## 📦 Requisitos

- Python 3.10+  
- Pip  
- Ambiente virtual (recomendado)  

---

## ⚙️ Instalação

```bash
# Clonar o projeto
git clone https://github.com/seuusuario/projeto_agenda_django.git
cd projeto_agenda_django

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (escolha conforme o seu sistema)
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar o banco de dados e aplicar migrações
python manage.py migrate

# Criar usuário admin (opcional)
python manage.py createsuperuser

# Rodar o servidor local
python manage.py runserver
