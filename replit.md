# Smart Study Planner

A Django REST Framework API for managing study plans and tasks with JWT authentication.

## Tech Stack

- Python 3.12
- Django 6.0.4
- Django REST Framework
- djangorestframework-simplejwt (JWT auth)
- django-filter (search/filter support)
- drf-spectacular (OpenAPI/Swagger docs)
- Whitenoise (static files)
- Gunicorn (production server)
- PostgreSQL (via Replit managed DATABASE_URL secret)

## Project Structure

- `smart_study_planner/` — Django project settings, URLs, WSGI
- `planner/` — Study plans and tasks app (models, views, serializers, URLs)
- `users/` — User registration and JWT login app
- `manage.py` — Django management CLI
- `requirements.txt` — Python dependencies

## Key API Endpoints

- `GET /` — Redirects to Swagger UI
- `POST /api/auth/register/` — Register a user
- `POST /api/auth/login/` — Obtain JWT tokens
- `POST /api/auth/token/refresh/` — Refresh access token
- `GET/POST /api/planner/studyplans/` — List/create study plans
- `GET/PUT/PATCH/DELETE /api/planner/studyplans/<id>/` — Study plan detail
- `GET /api/planner/studyplans/<id>/progress/` — Plan completion %
- `GET/POST /api/planner/tasks/` — List/create tasks
- `GET/PUT/PATCH/DELETE /api/planner/tasks/<id>/` — Task detail
- `GET /api/docs/` — Swagger UI
- `GET /api/schema/` — OpenAPI schema

## Configuration

- `DJANGO_ALLOWED_HOSTS` — defaults to `127.0.0.1,localhost,.onrender.com` plus `*` for Replit proxy
- `DJANGO_SECRET_KEY` — Django secret key
- `DJANGO_DEBUG` — Debug mode (default True)
- `DATABASE_URL` — PostgreSQL connection string (Replit managed secret)

## Running Locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:5000
```

## Workflow

- **Start application**: `python3 manage.py runserver 0.0.0.0:5000` on port 5000

## Deployment

- Target: autoscale
- Run command: `gunicorn --bind=0.0.0.0:5000 --reuse-port smart_study_planner.wsgi:application`
