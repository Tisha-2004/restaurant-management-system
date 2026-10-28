# Restaurant Management System

A complete restaurant management web application built with **Django 5**, **Bootstrap 5** and **SQLite** —
a modern public-facing restaurant website plus a fully custom admin dashboard (the Django default admin is
*not* used for restaurant management).

## Features

**Public website**
- Hero banner with *Book Table* / *Explore Menu* calls to action
- Featured categories (Pizza, Burger, Pasta, Chinese, South Indian, Desserts, Drinks)
- Popular food cards, about, gallery, testimonials, opening hours, map placeholder, footer
- Menu page with live search, category filter and pagination
- Dark mode toggle, scroll animations, back-to-top button, loading spinner, 404/500 pages

**Accounts**
- Customer register / login / logout (`/register/`, `/login/`, `/logout/`)
- Separate staff login at `/admin-login/` (admin, manager and chef roles only)
- Customer dashboard with reservations, orders and bills

**Custom admin dashboard** (`/dashboard/`)
| Module | What it does |
| --- | --- |
| Dashboard | Stat cards (customers, today's orders/reservations, revenue, table status) + Chart.js charts |
| Customers | Full CRUD, search, pagination, profile page |
| Menu | Food + category CRUD, search, category filter, image upload with live preview |
| Tables | CRUD and colour-coded status grid (green available / orange reserved / red occupied) |
| Reservations | CRUD, cancel, search, status filter and month calendar view |
| Kitchen | Chef kanban board with one-click Pending → Preparing → Ready → Served |
| Billing | Invoice generation with GST, print view, PDF download, cash/card/UPI, paid/unpaid |
| Reports | Daily, monthly, reservation and sales reports with CSV and PDF export |
| Users | Manage accounts and roles |
| Settings | Restaurant name, logo, contact details, GST percentage |

Global search (`/search/`) covers customers, food, reservations, orders and bills.

## Tech stack
Python 3.10+ · Django 5 · SQLite · Bootstrap 5 · Font Awesome 6 · Google Fonts (Poppins) · Chart.js · ReportLab (PDF)

## Getting started

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data        # demo categories, dishes, tables, customers, orders, bills
python manage.py runserver
```

Open http://127.0.0.1:8000/

### Demo logins
| Role | URL | Username | Password |
| --- | --- | --- | --- |
| Admin | `/admin-login/` | `admin` | `Admin@12345` |
| Chef | `/admin-login/` | `chef` | `Chef@12345` |
| Customer | `/login/` | `guest` | `Guest@12345` |

## Project layout

```
RestaurantManagementSystem/
├── manage.py, requirements.txt, db.sqlite3
├── restaurant/          project settings & root URLs
├── core/                public pages, site settings, gallery, testimonials, global search
├── accounts/            auth, roles, staff login, users module
├── dashboard/           admin dashboard & settings
├── customers/  menu/  tables/  reservations/  kitchen/  billing/  reports/
├── templates/           base.html, admin_base.html and per-module templates
├── static/css|js|images
└── media/menu_images|logo
```

## Security
CSRF protection on every form, `login_required` / role-based `staff_required` decorators on all admin
modules, server-side form validation and Bootstrap alert messaging.

> Before deploying, set `DEBUG = False`, replace `SECRET_KEY` and configure `ALLOWED_HOSTS` in
> `restaurant/settings.py`.
