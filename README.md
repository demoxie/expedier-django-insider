# Incidence Search — Expedier Assessment

A production-ready **Incidence Search** feature built with **Django + DRF** (backend) and **React + Vite** (frontend).

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm 9+

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # create a staff user
python manage.py seed_incidences   # seed 50 sample incidences

python manage.py runserver         # → http://127.0.0.1:8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev    # → http://localhost:5173
```

> **Note:** The React dev server proxies `/api/*` to Django automatically.

### Login
1. Open `http://127.0.0.1:8000/admin/` and log in with your superuser
2. Open `http://localhost:5173` — the session cookie is shared

### Running Tests
```bash
# Backend (33 tests)
cd backend && source venv/bin/activate
python manage.py test incidences --verbosity=2

# Frontend (13 tests)
cd frontend
npx vitest run
```

## Project Structure
```
expediate/
├── backend/
│   ├── config/            # Django project settings
│   ├── incidences/        # Incidence app
│   │   ├── models.py      # Incidence model (UUID, indexes)
│   │   ├── serializers.py # DRF serializer
│   │   ├── filters.py     # django-filter FilterSet (7 params)
│   │   ├── views.py       # ReadOnlyModelViewSet
│   │   ├── urls.py        # DRF router
│   │   ├── admin.py       # Admin registration
│   │   ├── tests/         # 33 tests (model, filter, API)
│   │   └── management/    # seed_incidences command
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # FilterPanel, IncidenceTable, Pagination
│   │   ├── pages/         # IncidenceSearchPage
│   │   ├── services/      # API client (axios)
│   │   ├── __tests__/     # 13 tests (component tests)
│   │   └── index.css      # Premium CSS design system
│   └── vite.config.js     # Vite + proxy + vitest config
├── PR_DESCRIPTION.md
├── OPERATIONAL_READINESS.md
└── README.md
```

## API Reference

### `GET /api/incidences/`

**Permission:** Staff users only

| Parameter | Type | Behavior |
|-----------|------|----------|
| `q` | string | Case-insensitive text search on title |
| `fingerprint` | string | Exact match |
| `status` | enum | `unresolved`, `resolved`, `ignored` |
| `first_seen_from` | ISO date | Inclusive lower bound |
| `first_seen_to` | ISO date | Inclusive upper bound |
| `last_seen_from` | ISO date | Inclusive lower bound |
| `last_seen_to` | ISO date | Inclusive upper bound |
| `ordering` | string | e.g. `-last_seen`, `title` |
| `page` | int | Page number (25 per page) |
