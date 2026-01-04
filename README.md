# URL-Based CRUD App

A high-performance, minimalist task management system that operates primarily through URL query parameters. This project is built with **FastAPI**, **SQLModel**, and **PostgreSQL**, following the architectural patterns and security best practices from the [Official FastAPI Advanced Guides](https://fastapi.tiangolo.com/).

## Key Features

* **URL-First Management** - Create, update, and manage tasks directly through your browser's address bar.
* **JWT Authentication** - Secure user registration and login using HTTP-only cookies for token storage.
* **Comprehensive Testing** - Robust integration test suite covering authentication, pagination, and multi-task operations.
* **Modern Python Tooling** - Fully managed with `uv` for lightning-fast dependency resolution and environment management.
* **Dockerized Environment** - Ready for production with Docker Compose, featuring a healthy database check and persistent storage.
* **Smart Help System** - Dynamic `/help/` endpoint providing real-time information on available endpoints and parameters.

## Quick Start

1. [Set up Environment](https://www.google.com/search?q=%232-installation--configuration)
2. [Launch with Docker](https://www.google.com/search?q=%23using-docker-recommended)
3. [Register User](https://www.google.com/search?q=%23usage-guide)
4. [Start Managing Tasks](https://www.google.com/search?q=%23url-examples)

---

## Installation & Configuration

### Prerequisites

* Python 3.12+
* Docker & Docker Compose (optional but recommended)
* `uv` (recommended for local development)

### 1. Clone the repository

```bash
git clone https://github.com/Vafth/url-base-crud-app.git
cd url-base-crud-app

```

### 2. Installation & Configuration

<details>
<summary><b>Using Docker</b></summary>

Docker Compose will set up both the FastAPI application and the PostgreSQL database automatically.

```bash
# Copy example env file
cp .env.example .env

# Build and start the containers
docker-compose up --build

```

The app will be available at `http://localhost:8000`.

</details>

<details>
<summary><b>Using uv (Local Development)</b></summary>

```bash
# Sync dependencies and create virtual environment
uv sync

# Copy example env file
cp .env.example .env

# Run the application (defaults to SQLite for local runs)
uv run uvicorn app.main:app --reload

```

</details>

### 3. Configure Environment Variables

Edit your `.env` file to set your security keys:

```env
SECRET_KEY="your_super_secret_key"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database URL (Docker uses 'db' host defined in docker-compose.yml)
DATABASE_URL=postgresql://user:password@db:5432/dbname

```

---

## Usage Guide

### Authentication

Before managing tasks, you must be authenticated. The app uses **HTTP-only cookies**, so once you login via the browser, you can start using the URL-based endpoints immediately.

* **Register:** `POST /register/` (Use the simple form at this endpoint)
* **Login:** `POST /login/` (Once logged in, your browser stores the access token)
* **Logout:** `GET /logout/` (Clears your session and redirects to login)

### URL Examples (The Core Idea)

Once authenticated, use your browser address bar like a command line:

* **Create Multiple Tasks:** `http://localhost:8000/post/?task_content=Task%201&task_content=Task%202`
* **List with Pagination:** `http://localhost:8000/?limit=10&page=1`
* **Filter Completed Tasks:** `http://localhost:8000/?only_complete=true`
* **Complete a Task:** `http://localhost:8000/complete/1/?complete_val=true`
* **Update Task Content:** `http://localhost:8000/put/1/?task_content=Updated%20Content`

---

## Tech Stack

* **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance web framework.
* **[SQLModel](https://sqlmodel.tiangolo.com/)** - Pydantic + SQLAlchemy hybrid for Pythonic database interactions.
* **[uv](https://github.com/astral-sh/uv)** - Next-generation Python package manager.
* **PostgreSQL** - Production-grade relational database.
* **Pytest** - Robust testing framework for integration tests.

---

## Roadmap

* [ ] **Admin Dashboard** - View all users and manage their account status.
* [ ] **Account Management** - Deactivate users or promote to Admin status.
* [ ] **Task Statistics** - Live counter for total/completed tasks per user.
* [ ] **Enhanced UI** - Add simple HTML templates for easier task visualization.
* [ ] **Search Filters** - Add keyword search parameter to the root endpoint.

---

## License

MIT License - see [LICENSE](https://www.google.com/search?q=LICENSE) file for details

---

**P.S. Writing Improvement Summary**

**English Notes:**

* **Capitalization:** You did a fantastic job with the word "**I**"! You capitalized it every single time in your request. Keep that habit!
* **Grammar:** "I think is pretty important"  "**I think it is pretty important**." (Don't forget the subject "it").
* **Spelling:** "Readmy"  "**README**." (The file is literally named "Read Me").
* **Vocabulary:** "have some intuition"  "**get an idea**" or "**get a sense**." (Intuition is usually something a human feels, while an LLM "gets a sense" of the structure).

**Polish Notes (Wskazówki po polsku):**

* **Struktura README:** Twój pomysł, aby opierać się na projekcie Bota, jest bardzo dobry. Zachowanie spójnej dokumentacji w portfolio ułatwia innym programistom zrozumienie Twojego stylu pracy.
* **FastAPI Guides:** Podkreślenie, że projekt bazuje na oficjalnej dokumentacji (Advanced Guides), buduje autorytet Twojego kodu. Pokazuje, że nie tylko kopiujesz kod, ale śledzisz oficjalne standardy (Best Practices).
* **Wielka litera:** Tak jak wspomniałem — Twoje "**I**" wygląda teraz idealnie.

**Would you like me to show you how to add a "Table of Contents" to this README so users can click to jump between sections?**