# Sale Package Notes

## What changed in this clean package
- Removed the local `.venv` virtual environment and Python cache files to reduce archive size and avoid shipping machine-specific dependencies.
- Removed `db.sqlite3` so local database records, sessions, and demo data are not distributed.
- Kept application source, migrations, templates, static assets, and `requirements.txt`.

## Local setup
Use Python 3.10 or newer. From the project root:

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. `seed_data` creates sample restaurant data and demo users with fixed passwords in the command source. This is for local demo only. Never use those accounts in a public deployment. If you want a clean database without demo data, skip `seed_data` and create a user with `python manage.py createsuperuser`; note that the custom staff login/roles may require configuring a profile.

## Important security warnings
The supplied `restaurant/settings.py` still has development settings: `DEBUG = True`, `ALLOWED_HOSTS = ["*"]`, and a placeholder `SECRET_KEY`. These were not silently changed because changing configuration can affect whether the project starts in your environment. They are **not safe for public production deployment**. Before deploying, set a strong secret key via environment variables, set `DEBUG = False`, restrict `ALLOWED_HOSTS` to the real hostnames, configure HTTPS/security settings, and run `python manage.py check --deploy`.

The database file was removed from this package, but still inspect all source and media files for anything you do not own or do not have permission to resell. The application has not been run or end-to-end tested in this environment. Verify each advertised feature and installation steps before claiming that it is fully functional.

## Sale status
This is a pre-launch source-code project. No live deployment, customers, revenue, production-readiness, or independent security audit are being claimed. The buyer should review and test the project before purchase.
