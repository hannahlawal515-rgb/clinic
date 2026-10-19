# Careline Clinic Queue

A lightweight front-desk queue manager built with Django, HTML, CSS, and JavaScript. Staff can register patients, call the next person, track visits in service, and review completed visits for today.

## Requirements

- Python 3.12 or newer

## Setup

Create and activate the local virtual environment, install dependencies, and initialize the database:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. The `.venv` directory is local and ignored by Git; dependencies are recorded in `requirements.txt`.

## Queue actions

- **Add patient** registers a name, optional phone number, and service.
- **Call next** moves the earliest waiting patient into service.
- Each ticket can be returned to waiting or marked complete.
- Search and status filters help staff find today's tickets. The Django admin is available at `/admin/` after creating a superuser with `python manage.py createsuperuser`.

This starter uses SQLite and Django's development server. Configure production settings, authentication, and a production database before deploying with real patient information.