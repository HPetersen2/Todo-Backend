# Django Todo Application

## Description

This project is a Django-based Todo application that provides:

* Classic **Django views with templates** for direct usage in the browser
* A **REST API** built with **Django Rest Framework (DRF)**
* Authentication using **JWT (Simple JWT)**
* Styled templates using **Django Crispy Forms**
* Cross-origin support via **Django Cors Headers**

The application can be used both as a traditional web app and as a backend API for external clients.

---

## Quickstart

Follow the steps below to get the project running locally.

### 1. Clone the project from GitHub

```bash
git clone https://github.com/HPetersen2/Todo-Backend.git
```

### 2. Change into the project directory

```bash
cd Todo-Backend
```

### 3. Create and activate a virtual environment

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
```

---

### 4. Copy the environment template

#### macOS / Linux

```bash
cp .env.template .env
```

#### Windows (PowerShell)

```powershell
copy .env.template .env
```

---

### 5. Fill in the `.env` file

Open the `.env` file and configure all required environment variables (e.g. secret key, database settings, JWT settings, etc.).

---

### 6. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 7. Apply database migrations

```bash
python manage.py migrate
```

---

### 8. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

---

## Usage

### Web Views (Templates)

The application includes classic Django views rendered with templates.
You can access the login page at:

```
http://<host>/login/
```

These views are intended for direct interaction within the browser.

---

### REST API (Django Rest Framework)

In addition to the template-based views, the project provides a RESTful API built with **Django Rest Framework**.

#### Available Endpoints

| Method | Endpoint       | Description            |
| ------ | -------------- | ---------------------- |
| GET    | `/api/todos/`      | List all todos         |
| POST   | `/api/todos/`      | Create a new todo      |
| GET    | `/api/todos/<id>/` | Retrieve a single todo |
| PUT    | `/api/todos/<id>/` | Update a todo          |
| DELETE | `/api/todos/<id>/` | Delete a todo          |

The endpoints are defined as:

```python
urlpatterns = [
    path('todos/', TodoListCreateView.as_view()),
    path('todos/<int:pk>/', TodoDetailView.as_view()),
]
```

---

## Technologies Used

* **Django**
* **Django Rest Framework**
* **Django Crispy Forms**
* **Django Cors Headers**
* **Simple JWT (Authentication)**
* **Python Virtual Environments**

---

## Notes

* Make sure your virtual environment is activated before running any Django commands.
* JWT authentication is required for protected API endpoints.
* This project can be extended easily for frontend frameworks or mobile applications.
