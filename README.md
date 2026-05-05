Smart Study Planner — Render deployment

Quick steps to deploy to Render (Docker recommended):

1. Push this repository to GitHub.
2. In Render dashboard, create a new Web Service and connect your GitHub repo.
   - Choose "Docker" (Render will build using the provided `Dockerfile`).
   - Or choose "Static/Python" and set the Build Command to `pip install -r requirements.txt` and Start Command to `gunicorn smart_study_planner.wsgi:application --bind 0.0.0.0:$PORT`.
3. Add Environment variables (in Render service settings):
   - `DJANGO_SECRET_KEY` set to a secure value
   - `DJANGO_DEBUG` set to `False`
   - `DJANGO_ALLOWED_HOSTS` set to your service host (e.g. `myapp.onrender.com`)
   - `DATABASE_URL` — if you add a Render Postgres database, Render will provide this.
4. After deploy completes, open Render Shell and run migrations once:

   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. Optionally create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

Local development quick-start:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API docs (once deployed):
- Swagger UI: `/api/docs/`
- OpenAPI schema: `/api/schema/`
