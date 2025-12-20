# WhatUSaidWhatWeDone
This platform is combined with any ideas come from you. So write down your lovely idea please.

我现在打算做一个网页应用，但由于我想不到主题，所以我打算做一个大杂烩平台，里面可以包含任意的功能。目前网页暂时展示一个酷炫的todo list，大家可以在上面写下自己的想法和需求。然后我逐一去实现并加在我的这个平台中。我的后端打算用python+flask+poetry，前端用vue.js来写，搭配一些主流好用的UI库去实现一个简洁且美观的前端UI。不能太丑陋没有美感。目前你先给我实现一个基础的前后端，先把todo list这个功能实现了，允许用户输入自己的想法和需求等。还有就是要写dockerfile使这个项目可以直接docker build，方便后期CICD。你先实现基础的框架和功能，记住，前端UI界面要符合当今审美潮流
# Fullstack Project Template

This repository is a **project-level template** with:

- `backend/` – Flask backend (Poetry + virtualenv + MySQL)
- `frontend/` – empty directory (reserved for future frontend)

---

## Project Structure

```text
project-template/
├── backend/
│   ├── app/
│   │   ├── commands/     # Flask CLI commands (db_init)
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── routes/       # HTTP routes / APIs
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── __init__.py
│   ├── pyproject.toml    # Poetry dependency & virtualenv config
│   ├── .env.example
│   ├── wsgi.py
│   └── README.md
│
└── frontend/             # empty (intentionally)
```

---

## Backend Overview

The backend uses:

- **Flask** – Web framework
- **SQLAlchemy** – ORM
- **Flask-Migrate** – Database migration support
- **MySQL** – Running in Docker (host port `13306`)
- **Poetry** – Dependency management + virtual environment

---

## Prerequisites

Make sure the following are installed on your machine / server:

- Python **3.10+**
- Docker (for MySQL)
- Poetry

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

### 1. Enter backend directory

```bash
cd backend
```

---

### 2. Install dependencies (creates virtual environment automatically)

```bash
poetry install
```

Poetry will automatically create and manage a virtual environment.

---

### 3. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DB_HOST=127.0.0.1
DB_PORT=13306
DB_NAME=demo_db
DB_USER=root
DB_PASSWORD=root
```

> `.env` **must not** be committed to Git.

---

### 4. Verify MySQL is reachable

```bash
mysql -h 127.0.0.1 -P 13306 -u root -p
```

If you can log in, the database connection is correct.

---

### 5. Initialize database and tables

Run the custom Flask CLI command:

```bash
poetry run flask db_init
```

This will:

1. Create database `demo_db` if it does not exist
2. Create tables based on SQLAlchemy models

---

### 6. Run backend server

```bash
poetry run python wsgi.py
```

Server will start on:

```
http://localhost:5000
```

Test health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{"status": "ok"}
```

---

## Virtual Environment Notes (Important)

- **Do NOT use `pip install` directly**
- Always use:
  ```bash
  poetry install
  poetry run <command>
  ```
- Poetry automatically isolates dependencies per project
- No need to manually create `.venv`

---

## Frontend

The `frontend/` directory is intentionally empty.

You can later add:

- Vue / React
- Vite
- Next.js
- Any frontend stack

---

## Recommended Next Steps

- Add CRUD APIs (User, Auth, etc.)
- Enable Flask-Migrate workflows
- Add JWT authentication
- Dockerize backend
- Add CI/CD

---

## License

MIT
