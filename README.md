# URL-Based CRUD App

A minimalist task management system that operates primarily through URL query parameters. Built with **FastAPI** and **SQLModel**, following architectural patterns and security best practices from the [Official FastAPI Guides](https://fastapi.tiangolo.com/).

## Key Features

- **URL-First Management** - Create, update, and manage tasks directly through your browser's address bar
- **JWT Authentication** - Secure user registration and login using HTTP-only cookies for token storage
- **Dockerized Environment** - Production-ready with Docker Compose, featuring health checks and persistent storage

## Quick Start

1. [Clone & Configure](#installation--configuration)
2. [Choose Your Setup](#3-installation) (Docker/pip/uv)
3. [Register & Login](#authentication)
4. [Start Managing Tasks](#create-tasks)

---

## Installation & Configuration

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (optional, for containerized setup)
- Basic command line knowledge

### 1. Clone the Repository
```bash
git clone https://github.com/Vafth/url-base-crud-app.git
cd url-base-crud-app
```

### 2. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and configure based on your setup:
```env
# Security
SECRET_KEY="your_super_secret_key_here"  # Generate with: openssl rand -hex 32 or python -c "import secrets; print(secrets.token_hex(32))"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
# For Local Development (SQLite):
DATABASE_URL=sqlite:///./app/database.db

# For Docker/Production (PostgreSQL):
# DATABASE_URL=postgresql://user:password@db:5432/dbname
```

> **Note:** Comment/uncomment the appropriate `DATABASE_URL` based on whether you're running locally (SQLite) or via Docker (PostgreSQL).

### 3. Installation

<details>
<summary><b>Using Docker</b></summary>

Docker Compose sets up both the FastAPI application and PostgreSQL database.

**Before starting:**
1. Ensure the PostgreSQL `DATABASE_URL` is **uncommented** in `.env`
2. Comment out the SQLite `DATABASE_URL`

```bash
# Build and start containers
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

The app will be available at **http://localhost:8000**

**Useful commands:**
```bash
# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

</details>

<details>
<summary><b>Using pip</b></summary>

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access the app at **http://localhost:8000**

</details>

<details>
<summary><b>Using uv</b></summary>

```bash
# Sync dependencies
uv sync

# Run the application
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access the app at **http://localhost:8000**

</details>

---

## Usage Guide

### Authentication

The app uses **JWT tokens stored in HTTP-only cookies**. Once you log in via the browser, you can immediately use URL-based endpoints.

**Authentication Endpoints:**

- **Register:** Navigate to `http://localhost:8000/register/`
  - Fill out the registration form
  - Create your account
  
- **Login:** Navigate to `http://localhost:8000/login/`
  - Enter credentials
  - Access token automatically stored in cookie
  
- **Logout:** Navigate to `http://localhost:8000/logout/`
  - Clears session and redirects to login

### URL-Based Task Management

Once authenticated, manage tasks directly through URLs:

#### Create Tasks
```
# Create a single task
http://localhost:8000/post/?task_content=Buy groceries

# Create multiple tasks at once
http://localhost:8000/post/?task_content=Task 1&task_content=Task 2&task_content=Task 3
```

#### List & Filter Tasks
```
# List all tasks
http://localhost:8000/

# Paginated list
http://localhost:8000/?limit=10&page=1

# Show only completed tasks
http://localhost:8000/?only_complete=true

# Show only incomplete tasks
http://localhost:8000/?only_complete=false
```

#### Update Tasks
```
# Mark task as complete
http://localhost:8000/complete/1/?complete_val=true

# Mark task as incomplete
http://localhost:8000/complete/1/?complete_val=false

# Update task content
http://localhost:8000/change/1/?task_content=Updated task content
```

#### Delete Tasks
```
# Delete a specific task
http://localhost:8000/delete/1/
```

---

## Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, high-performance web framework
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - SQL databases in Python with type safety

Full dependencies in `requirements.txt` and `pyproject.toml`

---

## Roadmap

- [ ] **Admin Dashboard** - View and manage all users and their account status
- [ ] **Account Management** - Deactivate users or promote to admin status
- [ ] **Task Statistics** - Display counters for total/completed tasks
- [ ] **Advanced Filters** - Add keyword search and date range filtering
- [ ] **Task Categories** - Organize tasks with tags or categories
- [ ] **Due Dates** - Add deadline tracking for tasks

---

## License

MIT License - see [LICENSE](LICENSE) file for details
