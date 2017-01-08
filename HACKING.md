Running openstates.org Locally
===

- Navigate to the `openstates.org` directory
- Invoke the `openstates` virtualenv (most importantly Django 1.8 and Python 2)
- Set the SECRET_KEY environment variable to anything, it just can't be missing
- Run `python manage.py runserver —-settings openstates.settings.dev`
- View the website at `localhost:8000`
