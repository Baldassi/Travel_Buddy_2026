<div align="center">

<h1>✈ TravelBuddy</h1>

<p><strong>Group travel planning · Flight booking · Secure payments · Destination guides</strong></p>

<p>
  <img src="https://img.shields.io/badge/version-2.0-1a6b6b?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/flask-3.0-black?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/tests-31%20passing-2e7d5a?style=flat-square&logo=pytest&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/license-MIT-c9922a?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/i18n-EN--GB%20%7C%20PT--BR-5E4A8A?style=flat-square" alt="i18n">
</p>

<p>
  <a href="#-quick-start">Quick Start</a> ·
  <a href="#-features">Features</a> ·
  <a href="#-project-structure">Structure</a> ·
  <a href="#-api-integrations">API Integrations</a> ·
  <a href="#-running-tests">Tests</a> ·
  <a href="#-business-rules">Business Rules</a>
</p>

</div>

---

## Overview

TravelBuddy is a full-stack web application built with **Python / Flask** that evolves a collaborative group travel planner into a complete travel-agency platform. It runs entirely on your local machine with no external database — all data is stored in a self-contained **SQLite** file.

> **Academic context:** Developed as an MVP deliverable for PRD 6300 (Saturday\_Agile6301 · Academic Year 2025–2026). The project follows a Scrumban methodology across five sprints tracked in Jira (Linear).

---

## ✨ Features

### Core (v1)

| Feature | Description |
|---|---|
| **User Authentication** | Register, login, logout with PBKDF2-SHA256 password hashing (Werkzeug) |
| **Group Trip Planning** | Create, view, and delete group trips with destination, date, and capacity |
| **RSVP System** | Add and remove guests; duplicate and overbooking guards enforced at DB level |
| **Dashboard** | Live stats: total trips, your trips, total RSVPs across all groups |
| **i18n / Localisation** | Full British English ↔ Brazilian Portuguese toggle (Flask-Babel) |

### New in v2

| Feature | Description |
|---|---|
| **Flight Search** | Search and compare flights by origin, destination, dates, passengers, and cabin class |
| **Secure Checkout** | Stripe Elements card tokenisation (PCI-DSS compliant). Raw card data never stored |
| **Instalment Plans** | 1×, 2×, 3× (interest-free) and 6×, 12× payment plans selectable at checkout |
| **Cancellation Policy** | Automated refund logic: >72 h before departure = 80% refund; ≤72 h = no refund |
| **Seat Selection** | Standard (free, assigned at check-in) or Premium (£10/pax, pre-selected at checkout) |
| **Online Check-in** | Standard: 24 h before departure. Premium: 20 days before departure |
| **Boarding Pass** | Digital boarding pass with seat numbers, barcode, and full print support |
| **Destination Guides** | AI-generated travel guides with overview, attractions, nature, festivals, and local tips |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher — [python.org](https://www.python.org/downloads/)
- `pip` (bundled with Python 3.9+)

### 1 — Clone the repository

```bash
git clone https://github.com/your-username/travelbuddy.git
cd travelbuddy
```

### 2 — Create a virtual environment

```bash
# Create
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows (Command Prompt)
venv\Scripts\activate

# Activate — Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

> Your terminal prompt will show `(venv)` when the environment is active. Always activate before running or testing the app.

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Run the application

```bash
python app.py
```

```
  ✈  TravelBuddy v2 is running →  http://127.0.0.1:5000
```

Open **http://127.0.0.1:5000** in your browser. The SQLite database (`travelbuddy.db`) is created automatically on first launch.

> **No API keys are required to run locally.** The application ships with realistic mock data for flights, payments, and destination guides. See [API Integrations](#-api-integrations) for optional live integrations.

---

## 🧪 Running Tests

```bash
# Full suite (31 tests)
python -m pytest

# Verbose output
python -m pytest -v

# Individual suites
python -m pytest tests/test_unit.py        -v   # 11 tests
python -m pytest tests/test_integration.py -v   # 12 tests
python -m pytest tests/test_regression.py  -v   #  8 tests
```

Tests use an isolated **in-memory SQLite** database — no files are written to disk and no running application instance is required.

| Suite | Tests | Covers |
|---|---|---|
| `test_unit.py` | 11 | Model logic, password hashing, `spots_left` property |
| `test_integration.py` | 12 | Full auth, trip creation, and RSVP workflows end-to-end |
| `test_regression.py` | 8 | Bug guards: duplicate RSVPs, overbooking, auth security, duplicate registration |
| **Total** | **31** | **31 / 31 passing** |

---

## 📁 Project Structure

```
travelbuddy/
├── app.py                    # Application factory & entry point
├── extensions.py             # Shared db, login_manager, babel instances
├── models.py                 # All SQLAlchemy models (v1 + v2)
├── requirements.txt
├── pytest.ini
├── babel.cfg
│
├── routes/
│   ├── auth.py               # Register · Login · Logout
│   ├── trips.py              # Group trip CRUD
│   ├── rsvp.py               # RSVP add / remove
│   ├── lang.py               # Language toggle
│   ├── flights.py            # Search · Checkout · Bookings · Check-in · Boarding pass
│   └── destinations.py       # Destination guide (AI-powered / mock)
│
├── templates/
│   ├── base.html             # Master layout (navbar, flash messages, footer)
│   ├── login.html            # Split-screen editorial login
│   ├── register.html
│   ├── dashboard.html
│   ├── create_trip.html
│   ├── trip_detail.html
│   ├── flights/
│   │   ├── search.html
│   │   ├── checkout.html
│   │   ├── my_bookings.html
│   │   ├── booking_detail.html
│   │   ├── checkin.html
│   │   └── boarding_pass.html
│   └── destinations/
│       └── guide.html
│
├── static/css/
│   ├── style.css             # Full design system (v1 + v2 components)
│   └── auth.css              # Split-screen login / register layout
│
└── tests/
    ├── conftest.py           # Fixtures: app, db, test_client, sample data
    ├── test_unit.py
    ├── test_integration.py
    └── test_regression.py
```

---

## 🗄 Data Models

```
User ──< Trip ──< RSVP
     ──< Booking ──< Flight
                ──< Payment
                ──< Seat
```

| Model | Key Fields |
|---|---|
| `User` | `username`, `email`, `password_hash` |
| `Trip` | `destination`, `date`, `max_guests`, `user_id` |
| `RSVP` | `guest_name`, `guest_email`, `trip_id` · UniqueConstraint on `(guest_name, trip_id)` |
| `Flight` | `origin`, `destination`, `depart_date`, `airline`, `price_gbp`, `passengers` |
| `Booking` | `reference`, `status`, `total_gbp`, `premium_seats`, `checked_in` |
| `Payment` | `stripe_payment_id`, `amount_gbp`, `card_last4`, `card_brand`, `installments` |
| `Seat` | `seat_number`, `passenger`, `is_premium` |

---

## 🔌 API Integrations

All external integrations are **entirely optional**. The app runs completely offline with mock data.

| Service | Purpose | Fallback (no key) |
|---|---|---|
| **Amadeus** | Live flight search results | 5 realistic mock flights generated per search |
| **Stripe** | PCI-DSS card tokenisation | Mock payment form; accepts any test card input |
| **Anthropic Claude** | AI-generated destination guides | Structured mock guide with destination name injected |

### Environment variables

Each integration is activated by setting the corresponding environment variable at runtime. Refer to each provider's official documentation to obtain credentials:

- Amadeus: [developers.amadeus.com](https://developers.amadeus.com)
- Stripe: [stripe.com/docs](https://stripe.com/docs)
- Anthropic: [console.anthropic.com](https://console.anthropic.com)

> ⚠️ **Never commit credentials to version control.** Store all keys in a `.env` file (or your deployment platform's secret manager) and ensure `.env` is listed in `.gitignore`.

---

## 🔒 Security

- **Passwords** — PBKDF2-SHA256 hashed via Werkzeug. Plain-text passwords are never stored or logged.
- **Card data** — Tokenised client-side by Stripe Elements (PCI-DSS). Only `card_last4` and `card_brand` are persisted; no full card numbers ever reach the server.
- **Sessions** — Flask session cookies are signed with `SECRET_KEY`. Set a strong, randomly generated value in any non-development environment.
- **Access control** — All protected routes require `@login_required`. Booking actions are scoped to the booking owner.
- **Credentials** — No secrets, tokens, or API keys are present in this repository. See [API Integrations](#-api-integrations) for how to supply them safely at runtime.

---

## 📋 Business Rules

### Cancellation & Refund

| Scenario | Timing | Refund |
|---|---|---|
| ✅ Eligible | More than 72 hours before departure | **80%** of total paid (20% cancellation fee retained) |
| ❌ Not eligible | 72 hours or fewer before departure | **£0.00** — no refund issued |

### Seat Selection & Check-in

| Option | Cost | Check-in Opens | Seat Assignment |
|---|---|---|---|
| Standard | Free | 24 hours before departure | Auto-assigned at check-in |
| ⭐ Premium | £10 per passenger | 20 days before departure | Pre-selected at checkout |

### Instalment Plans

| Plan | Interest | Notes |
|---|---|---|
| 1×, 2×, 3× | **None — interest-free** | Recommended for most bookings |
| 6×, 12× | Applied by payment processor | For higher-value or longer-haul bookings |

---

## 🌍 Localisation

The full interface is available in **British English (EN-GB)** and **Brazilian Portuguese (PT-BR)** via Flask-Babel.

- Language toggle available in the navbar and footer on every page
- Preference stored in the browser session (no account setting required)
- All v2 pages — flights, checkout, boarding pass, destination guides — are fully bilingual

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.9+ · Flask 3.0 · Flask-Login · Flask-Babel |
| **ORM / Database** | Flask-SQLAlchemy 3.1 · SQLite |
| **Payments** | Stripe Elements (PCI-DSS card tokenisation) |
| **AI** | Anthropic Claude API (destination guides) |
| **Flight Data** | Amadeus Travel API |
| **Frontend** | Jinja2 · HTML5 · CSS3 · Vanilla JavaScript |
| **Typography** | Playfair Display · DM Sans (Google Fonts) |
| **Testing** | pytest · pytest-flask |
| **i18n** | Flask-Babel · GNU gettext |

---

## 📄 Licence

This project is released under the [MIT Licence](LICENSE).

---

<div align="center">
  <sub>Built with ✈ for PRD 6300 · Saturday_Agile6301 · 2025–2026</sub>
</div>
#   T r a v e l _ B u d d y _ 2 0 2 6 (by SNB)
 
 
