# TaskFlow

Aplicação de gestão de tarefas construída com Django e Tailwind CSS. Suporta múltiplos utilizadores, modo escuro/claro e dois idiomas (Português e English).

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=flat&logo=django&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-CDN-38B2AC?style=flat&logo=tailwind-css&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Render-4169E1?style=flat&logo=postgresql&logoColor=white)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?style=flat&logo=vercel&logoColor=white)

---

## Funcionalidades

- **Autenticação** — registo, login e logout de utilizadores
- **CRUD completo de tarefas** — criar, editar, eliminar e marcar como concluída
- **Prioridades** — Alta, Média e Baixa com indicadores visuais
- **Status** — Pendente, Em Andamento e Concluída
- **Quadro Kanban** — arrastar tarefas entre colunas com drag & drop
- **Dashboard** — estatísticas, gráfico semanal, tarefas para hoje e progresso por categoria
- **Categorias** — organizar tarefas com cores personalizadas
- **Filtros e pesquisa** — filtrar por status, prioridade, categoria e texto
- **Perfil do utilizador** — editar nome, e-mail, bio e cor do avatar
- **Modo escuro / claro** — alternado pelo utilizador, guardado no browser
- **Múltiplos idiomas** — Português (PT) e English (EN)
- **Admin Django** — painel de administração com badges coloridos

---

## Stack

| Camada               | Tecnologia          |
| -------------------- | ------------------- |
| Backend              | Django 5.0          |
| Frontend             | Tailwind CSS (CDN)  |
| Base de dados (dev)  | SQLite              |
| Base de dados (prod) | PostgreSQL — Render |
| Ficheiros estáticos  | WhiteNoise          |
| Hospedagem           | Vercel              |
| Autenticação         | Django Auth         |
| i18n                 | Django i18n         |

---

## Estrutura do Projeto

```
todo_app/
├── config/
│   ├── settings.py        # Configurações (dev + prod)
│   ├── urls.py            # Rotas raiz
│   └── wsgi.py            # Ponto de entrada WSGI
├── tasks/
│   ├── models.py          # Task, Category, UserProfile
│   ├── views.py           # Dashboard, Kanban, CRUD
│   ├── forms.py           # TaskForm, CategoryForm
│   ├── admin.py           # Admin customizado
│   ├── urls.py            # Rotas da app
│   ├── signals.py         # Auto-cria perfil no registo
│   └── context_processors.py
├── accounts/
│   ├── views.py           # Login, Registo, Logout
│   ├── forms.py           # LoginForm, RegisterForm
│   └── urls.py
├── templates/
│   ├── base.html          # Layout principal com sidebar
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── tasks/
│       ├── dashboard.html
│       ├── list.html
│       ├── kanban.html
│       ├── edit.html
│       ├── categories.html
│       └── profile.html
├── locale/
│   ├── pt_BR/             # Traduções Português
│   └── en/                # Traduções English
├── vercel.json            # Configuração Vercel
├── build_files.sh         # Script de build
├── requirements.txt       # Dependências Python
└── .env.example           # Modelo de variáveis de ambiente
```

---

## Instalação Local

### Pré-requisitos

- Python 3.12+
- pip

### Passos

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/taskflow.git
cd taskflow/todo_app

# 2. Criar e activar ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Copiar e configurar variáveis de ambiente
cp .env.example .env
# Editar .env e definir pelo menos DEBUG=True

# 5. Aplicar migrações
python manage.py migrate

# 6. Criar superutilizador
python manage.py createsuperuser

# 7. Compilar traduções
python manage.py compilemessages

# 8. Iniciar servidor
python manage.py runserver
```

Abrir em [http://localhost:8000](http://localhost:8000)

---

## Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha os valores:

```bash
# Django
SECRET_KEY=gere-uma-chave-secreta-forte-aqui
DEBUG=True                          # False em produção
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de dados (deixar vazio para usar SQLite em dev)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Vercel (só necessário em produção)
VERCEL_URL=seuapp.vercel.app
DJANGO_SETTINGS_MODULE=config.settings
```

Para gerar uma `SECRET_KEY` segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Deploy

A aplicação está configurada para deploy automático na **Vercel** com base de dados **PostgreSQL** no **Render**.

### 1. Base de dados — Render

1. Criar conta em [render.com](https://render.com)
2. Novo → PostgreSQL → preencher nome e região
3. Copiar a **External Database URL**

### 2. Código — GitHub

```bash
git init
git add .
git commit -m "chore: initial commit"
git remote add origin https://github.com/SEU_USUARIO/taskflow.git
git push -u origin main
```

### 3. Aplicação — Vercel

1. Importar repositório em [vercel.com](https://vercel.com)
2. **Build Command:** `./build_files.sh`
3. Adicionar as variáveis de ambiente:

| Variável                 | Valor               |
| ------------------------ | ------------------- |
| `SECRET_KEY`             | chave gerada acima  |
| `DEBUG`                  | `False`             |
| `DATABASE_URL`           | URL do Render       |
| `ALLOWED_HOSTS`          | `seuapp.vercel.app` |
| `VERCEL_URL`             | `seuapp.vercel.app` |
| `DJANGO_SETTINGS_MODULE` | `config.settings`   |

4. Clicar **Deploy**

### 4. Criar admin em produção

```bash
# Localmente, apontando para o banco do Render
export DATABASE_URL="postgresql://..."
export SECRET_KEY="..."
export DEBUG="False"

python manage.py createsuperuser
```

---

## Rotas Principais

| Método   | URL                   | Descrição                  |
| -------- | --------------------- | -------------------------- |
| GET      | `/`                   | Redireciona para dashboard |
| GET      | `/dashboard/`         | Painel com estatísticas    |
| GET      | `/tasks/`             | Lista de tarefas           |
| POST     | `/tasks/create/`      | Criar tarefa               |
| GET/POST | `/tasks/<id>/edit/`   | Editar tarefa              |
| POST     | `/tasks/<id>/delete/` | Eliminar tarefa            |
| POST     | `/tasks/<id>/toggle/` | Marcar como concluída      |
| GET      | `/kanban/`            | Quadro Kanban              |
| GET      | `/categories/`        | Gerir categorias           |
| GET/POST | `/profile/`           | Perfil do utilizador       |
| GET      | `/admin/`             | Painel de administração    |
| GET      | `/accounts/login/`    | Login                      |
| GET      | `/accounts/register/` | Registo                    |

---

## Modelos de Dados

```
User (Django Auth)
 └── UserProfile        avatar_color, bio, notify_overdue
 └── Category           name, color
 └── Task               title, description, priority, status,
                        category, due_date, order
```

---

## Licença

MIT License — use livremente para projectos pessoais e comerciais.
