# Car Dealership Capstone

A Django + Django REST Framework starter implementation for the Car Dealership capstone rubric. Includes dealer, review, car-make APIs, Django session authentication, sentiment analysis, static About/Contact pages, a React registration component, tests, Docker configuration, and GitHub Actions CI.

> This is a runnable starter project. You must run it, verify the APIs, take your own screenshots, push it to your own public GitHub repository, and deploy it using your course-supported platform. Real terminal logs, GitHub URLs, and deployment URLs cannot be pre-generated.

## Features
- Dealer listing, dealer detail, state filtering, reviews, car makes/models
- Django login/logout and registration API
- Review submission for authenticated users
- Sentiment endpoint for review text
- Django admin
- About and Contact static HTML pages
- React Register component
- Tests and GitHub Actions workflow

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations dealership
python manage.py migrate
python manage.py seed_dealers
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin/.

## API endpoints
- `GET /api/dealers/` — list dealers
- `GET /api/dealers/<id>/` — dealer detail
- `GET /api/dealers/state/<state>/` — dealers in a state
- `GET /api/dealers/<id>/reviews/` — reviews for a dealer
- `GET /api/carmakes/` — car makes and models
- `POST /api/analyze_review/` — JSON body `{"review": "Fantastic services"}`
- `POST /api/register/` — JSON username, first_name, last_name, email, password
- `POST /accounts/login/` — Django session login; form-encoded username/password and CSRF
- `POST /accounts/logout/` — session logout; CSRF required
- `POST /api/dealers/<id>/reviews/create/` — authenticated review creation

For session-authenticated POST requests, fetch a page or `/api/csrf/` first to establish a CSRF cookie, then send its value in the `X-CSRFToken` header and preserve cookies.

## Example cURL: public endpoints
```bash
curl -s http://127.0.0.1:8000/api/dealers/
curl -s http://127.0.0.1:8000/api/dealers/1/
curl -s http://127.0.0.1:8000/api/dealers/state/Kansas/
curl -s http://127.0.0.1:8000/api/dealers/1/reviews/
curl -s http://127.0.0.1:8000/api/carmakes/
curl -s -X POST http://127.0.0.1:8000/api/analyze_review/ \
  -H "Content-Type: application/json" \
  -d '{"review":"Fantastic services"}'
```

## GitHub and deployment
1. Create a public GitHub repository and push this project.
2. Confirm `.env`, credentials, database files, and secrets are not committed.
3. Configure GitHub Actions in `.github/workflows/django.yml`.
4. Deploy using the platform required by your course. Configure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, and a persistent production database as appropriate.
5. Replace `deploymentURL.txt` with the actual deployment URL after a successful deployment.

## Rubric evidence
Use the task checklist provided by your course. Capture screenshots yourself from the running local/deployed app. Save actual cURL commands and responses; never fabricate logs or screenshots.
