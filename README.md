# WhatUSaidWhatWeDone
This platform is combined with any ideas come from you. So write down your lovely idea please.

This repository is a **project-level template** with:

- `Backend/` - Flask backend (Poetry + virtualenv + MySQL)
- `Frontend/` - Vue 3 + Vite frontend (Tailwind CDN, Apple-inspired UI)

---

## Authors

- Kevin Shen
- Jimmy Cai

## Project Structure

```text
WhatUSaidWhatWeDone/
- Backend/
  - app/
    - commands/         # Flask CLI commands (db_init)
    - models/           # SQLAlchemy ORM models
    - routes/           # HTTP routes / APIs (health)
    - config.py
    - extensions.py
    - __init__.py
  - .env.example
  - pyproject.toml       # Poetry dependency & virtualenv config
  - wsgi.py

- Frontend/
  - App.vue              # Root shell (Header + router view)
  - main.ts              # Vue entry
  - router.ts            # Routes: / (home), /board
  - components/          # Header, Hero, TodoBoard
  - views/               # Home.vue, Board.vue
  - composables/         # useTodos shared state (add/vote)
  - data/                # Seed todos
  - types.ts             # Shared types/enums
  - index.html           # Tailwind CDN + root mount
  - package.json         # Vite/Vue scripts & deps
  - tsconfig.json
  - vite.config.ts
```

---

## Backend Overview

The backend uses:

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Migrate** - Database migration support
- **MySQL** - Running in Docker (host port `13306`)
- **Poetry** - Dependency management + virtual environment

---

## Prerequisites

Make sure the following are installed on your machine / server:

- Python **3.10+**
- Docker (for MySQL)
- Poetry (or install deps with pip)

Install Poetry (once):

```bash
pip install poetry
```

Verify:

```bash
poetry --version
```

---

## Backend Setup (Step by Step)

1) Enter backend directory
```bash
cd Backend
```

2) Install dependencies (creates virtual environment automatically)
```bash
poetry install
```

3) Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` with your MySQL settings.

4) Verify MySQL is reachable
```bash
mysql -h 127.0.0.1 -P 13306 -u root -p
```

5) Initialize database and tables
```bash
poetry run flask db_init
```

6) Run backend server
```bash
poetry run python wsgi.py
```
Server: `http://localhost:5000` (health check at `/health`)

---

## Frontend

Vue 3 + Vite SPA styled with Tailwind CDN (Apple-inspired UI).
- Routes: `/` (Hero + top-3 hottest todos), `/board` (full board with add form, voting toggle, detail modal)

Quickstart:
```bash
cd Frontend
npm install
npm run dev   # http://localhost:3000
```

---

## Recommended Next Steps

- Add CRUD APIs (User, Auth, etc.)
- Enable Flask-Migrate workflows
- Add JWT authentication
- Dockerize backend
- Add CI/CD

---

## Prompt
我现在打算做一个网页应用，但由于我想不到主题，所以我打算做一个大杂烩平台，里面可以包含任何的功能。目前网页暂时展示一个炫酷的todo list，大家可以在上面写下自己的想法和需求等。然后我逐一去实现并加在我的这个平台中。我的后端打算用python+flask+poetry，前端用vue.js来写，搭配一些主流好用的UI库去实现一个简洁且美观的前端UI。不能太休闲没有美感。目前你先给我实现一个基礎的前后端，先把todo list这个功能实现了，允许用户输入自己的想法和需求等。还有就是要写dockerfile使这个项目可以直接docker build，方便后期CICD。你先实现基础的框架和功能，记住，前端UI界面要符合当今审美潮流?

## License

MIT

---

