# Smart Study Planner API

A REST API for managing personal study plans and tasks, built with Django REST Framework. Features JWT authentication, per-user data isolation, search and filter support, and interactive Swagger documentation.

## Features

- JWT authentication (register, login, token refresh)
- Study plan and task CRUD — each user only sees their own data
- Task filtering by subject, priority, and completion status
- Full-text search on task title and subject
- Study plan progress endpoint (completion percentage)
- Interactive Swagger UI at `/api/docs/`
- Auto-generated OpenAPI 3.0 schema
- SQLite for local development, PostgreSQL for production

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 6 + Django REST Framework |
| Auth | djangorestframework-simplejwt |
| Filtering | django-filter |
| API Docs | drf-spectacular (Swagger UI) |
| Static Files | Whitenoise |
| Production Server | Gunicorn |
| Database | SQLite (dev) / PostgreSQL (prod) |

## Project Structure

```
smart_study_planner/        ← Django project config
├── settings.py
├── urls.py
└── wsgi.py

users/                      ← Auth app
├── serializers.py          ← RegisterSerializer, LoginSerializer, token serializers
├── views.py                ← RegisterView, LoginView, RefreshTokenView
├── signals.py              ← Seeds demo user after migrations
└── urls.py

planner/                    ← Core app
├── models.py               ← StudyPlan, Task
├── serializers.py          ← StudyPlanSerializer, TaskSerializer
├── views.py                ← StudyPlanViewSet, TaskViewSet
└── urls.py

templates/
└── drf_spectacular/
    └── swagger_ui.html     ← Custom dark-theme Swagger UI
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Create a new account | No |
| POST | `/api/auth/login/` | Get access + refresh tokens | No |
| POST | `/api/auth/token/refresh/` | Exchange refresh for new access token | No |

### Study Plans

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/planner/study-plans/` | List your study plans |
| POST | `/api/planner/study-plans/` | Create a study plan |
| GET | `/api/planner/study-plans/<id>/` | Get a study plan |
| PUT / PATCH | `/api/planner/study-plans/<id>/` | Update a study plan |
| DELETE | `/api/planner/study-plans/<id>/` | Delete a study plan |
| GET | `/api/planner/study-plans/<id>/progress/` | Get completion percentage |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/planner/tasks/` | List your tasks (supports filters + search) |
| POST | `/api/planner/tasks/` | Create a task |
| GET | `/api/planner/tasks/<id>/` | Get a task |
| PUT / PATCH | `/api/planner/tasks/<id>/` | Update a task |
| DELETE | `/api/planner/tasks/<id>/` | Delete a task |

**Task filters:** `?subject=math`, `?priority=high`, `?is_completed=true`  
**Search:** `?search=algebra`

### Docs

| Endpoint | Description |
|----------|-------------|
| `/api/docs/` | Swagger UI (interactive) |
| `/api/schema/` | Raw OpenAPI 3.0 schema |

## Using the API (Quick Start)

1. Register or use the demo account:
   - **username:** `susanacharya` **password:** `susan123`

2. Login to get a token:
```bash
curl -X POST /api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "susanacharya", "password": "susan123"}'
```

3. Use the token on every protected request:
```bash
curl /api/planner/study-plans/ \
  -H "Authorization: Bearer <your_access_token>"
```

Or open `/api/docs/`, click **Authorize**, and paste `Bearer <token>` to try all endpoints interactively.

## Local Development

```bash
pip install -r requirements.txt
python manage.py migrate        # also seeds the demo user
python manage.py runserver 0.0.0.0:5000
```

The demo account (`susanacharya` / `susan123`) is created automatically on first migration.

To create a superuser:
```bash
python manage.py createsuperuser
```

Run the test suite:
```bash
python manage.py test --verbosity=2
```

## Environment Variables

Copy `.env.example` and set these before deploying:

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Secret key for Django |
| `DJANGO_DEBUG` | `True` for dev, `False` for prod |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hostnames |
| `DATABASE_URL` | PostgreSQL connection string (optional, falls back to SQLite) |

## Deployment (Render)

This repo includes a `Dockerfile`, `Procfile`, and `render.yaml` for Render.

1. Push to GitHub and connect to a Render Web Service.
2. Set the environment variables above in Render's dashboard.
3. Add a Render PostgreSQL database and set `DATABASE_URL`.
4. After the first deploy:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

The production server uses Gunicorn:
```
gunicorn smart_study_planner.wsgi:application --bind 0.0.0.0:5000
```

## Notes

- All study plan and task endpoints are user-scoped — users cannot read or modify each other's data.
- The demo account is auto-seeded on every `manage.py migrate` run via a `post_migrate` signal.
- Passwords are validated against Django's built-in password validators (minimum length, common passwords, etc.).
