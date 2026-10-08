# Neurosciensemble

Neurosciensemble is an interdisciplinary study circle exploring neuroscience and related topics through physics, biology, mathematics, psychology, philosophy, cognitive science, and other fields.

Website:

https://neurosciensemble.org

Admin:

https://neurosciensemble.org/admin/

GitHub:

https://github.com/nimahamed88/study-circle

---

## 1. Project overview

This is a Django 6.1 project.

Main application:

    core/

Main features:

- Home page
- Monthly programme/calendar
- Upcoming and previous sessions
- Official `.ics` calendar feed
- Members
- Member detail pages
- Subgroups
- Subgroup detail pages
- Individual session pages
- Session speakers/presenters
- Session resources
- Journal Clubs
- Google Meet links
- Recording links
- Uploaded session PDFs
- Django administration

The public navigation is:

    Home
    Programme
    Members
    Subgroups
    Contact

---

## 2. Technology

Backend:

- Python
- Django 6.1
- PostgreSQL in production
- SQLite can be used for a simple local development setup
- Gunicorn in production

Frontend:

- Django templates
- HTML
- CSS
- No frontend framework

Production server:

- Ubuntu
- Nginx
- Gunicorn
- PostgreSQL
- Let's Encrypt HTTPS

Python package management:

- `uv`

---

## 3. Repository structure

    config/
        settings.py
        urls.py
        asgi.py
        wsgi.py

    core/
        admin.py
        apps.py
        models.py
        views.py
        urls.py

        migrations/

        templates/core/
            base.html
            home.html
            programme.html
            members.html
            member_detail.html
            subgroups.html
            subgroup_detail.html
            session_detail.html
            contact.html

        static/core/
            css/
            images/

    manage.py
    requirements.txt
    .gitignore

---

## 4. Important models

### Member

The Django model is still called `Speaker` for migration/backwards-compatibility reasons.

Public terminology is:

    Member

The model contains:

- name
- title
- biography
- email
- Instagram
- LinkedIn
- photo
- slug

Do not rename the Django model casually because existing migrations and database relationships depend on it.

### Subgroup

A subgroup contains:

- name
- slug
- description
- email
- head
- members

Members can belong to multiple subgroups.

### Session

A session contains:

- title
- description
- multiple speakers/members
- start time
- end time
- session type
- room
- Google Meet link
- recording URL
- optional PDF
- related subgroups

Session types currently include:

- Main Session
- Extensive Session
- Journal Club

### SessionResource

External resources associated with a session.

Current resource types:

- Paper
- Book
- Article
- Website
- Other

Each resource has:

- title
- type
- URL
- summary

---

## 5. Local development

### Requirements

You need:

- Python 3.13+ recommended
- `uv`
- Git

Clone the repository:

    git clone git@github.com:nimahamed88/study-circle.git
    cd study-circle

Create the virtual environment:

    uv venv --python 3.13

Activate it:

    source .venv/bin/activate

Install dependencies:

    uv pip install -r requirements.txt

Run migrations:

    python manage.py migrate

Create an admin user if necessary:

    python manage.py createsuperuser

Start the development server:

    python manage.py runserver

Then open:

    http://127.0.0.1:8000/

Admin:

    http://127.0.0.1:8000/admin/

---

## 6. Local database

Production uses PostgreSQL.

For simple local development, Django can use SQLite if the local settings are configured accordingly.

Never copy the production `.env` or production database credentials into the repository.


## 7. Django admin

Production admin:

    https://neurosciensemble.org/admin/

The admin is used to manage:

- Members
- Subgroups
- Sessions
- Session resources

For sessions, multiple members/speakers and multiple subgroups can be selected.

Session resources can be added directly inside the Session admin page.

### Terminology

Use:

    Member

for people who participate in the study circle.

The Django model is named:

    Speaker

because this was the original model name and changing it would require unnecessary database/migration work.

"Speaker" is still appropriate when referring specifically to a person presenting a particular session.

---

## 8. Programme and calendar

The Programme page contains:

- monthly calendar
- previous/next month navigation
- upcoming sessions
- previous sessions

Official calendar feed:

    https://neurosciensemble.org/calendar.ics

The Django database is the source of truth.

Do not create a separate Google Calendar as the primary source of sessions.

The `.ics` feed is generated dynamically by Django from future sessions.

### Google Calendar subscription

Users can subscribe manually through:

Google Calendar → Other calendars → From URL

using:

    https://neurosciensemble.org/calendar.ics

The calendar feed contains future sessions and includes:

- title
- start/end time
- location
- description
- speakers
- session type
- Google Meet link
- session page URL

---

## 9. Adding a new session

Use:

    Admin → Sessions → Add session

Fill in:

- title
- description
- speakers
- start time
- end time
- session type
- room
- Google Meet link
- recording URL if available
- PDF if available
- related subgroups

External resources can be added in the Session Resources section on the same admin page.

After saving the session, it automatically appears in:

- the Programme
- the monthly calendar
- the upcoming sessions list
- the official `.ics` calendar feed

---

## 10. Adding members

Go to:

    Admin → Members

Add:

- name
- title
- biography
- email
- social links
- photo
- slug

The public member page will be available under:

    /members/<slug>/

---

## 11. Adding subgroups

Go to:

    Admin → Subgroups

Each subgroup can have:

- name
- description
- email
- head
- members

Subgroups can also be associated with sessions.

---

## 12. Media files

Member photos and uploaded session PDFs are stored in the production `media/` directory.

They are NOT stored in Git.

Production media is served by Nginx.

Do not add production media files to Git unless there is a deliberate reason to make them part of the source repository.

---

## 13. Production architecture

The production architecture is:

    Internet
        |
        v
    Nginx
        |
        v
    Gunicorn
        |
        v
    Django
        |
        v
    PostgreSQL

Nginx also serves:

    /static/
    /media/

The Django/Gunicorn process listens only on:

    127.0.0.1:8000

Port 8000 should NOT be publicly exposed.

HTTPS is provided by Let's Encrypt.

---

## 14. Production server

The production server is a Hetzner Cloud VPS.

Project directory:

    /home/nima/study-circle

Virtual environment:

    /home/nima/study-circle/.venv

Production service:

    study-circle.service

Gunicorn:

    127.0.0.1:8000

Nginx handles public HTTP/HTTPS traffic.

### Important

Do not put production passwords, `.env` contents, SSH private keys, or other secrets in this README.

Each person who needs server access should have their own SSH key.

Do not share another person's private SSH key.

---

## 15. Updating the production website

The normal deployment workflow is:

### On the development machine

Make and test changes.

Check:

    git status

Run Django checks:

    python manage.py check

Commit:

    git add .
    git commit -m "Describe the change"

Push:

    git push origin main

### On the production server

SSH into the server.

Then:

    cd ~/study-circle
    git pull origin main

Activate the environment if needed:

    source .venv/bin/activate

Install dependencies if `requirements.txt` changed:

    uv pip install -r requirements.txt

If there are database migrations:

    python manage.py migrate

If static files changed:

    python manage.py collectstatic --noinput

Restart Gunicorn:

    sudo systemctl restart study-circle

Check the service:

    sudo systemctl status study-circle --no-pager

Then verify the website.

---

## 16. If the website returns HTTP 500

First check Gunicorn:

    sudo journalctl -u study-circle -n 100 --no-pager

Check the service:

    sudo systemctl status study-circle --no-pager

Then check Django:

    source .venv/bin/activate
    python manage.py check

Do not immediately change configuration without checking the Gunicorn traceback.

---

## 17. Production environment variables

Production secrets are stored in:

    /home/nima/study-circle/.env

This file is NOT tracked by Git.

It contains things such as:

- Django `SECRET_KEY`
- database credentials
- `DEBUG`
- `ALLOWED_HOSTS`

Never commit `.env`.

Never send the production `.env` through GitHub, email, Discord, or the README.

Recommended permissions:

    chmod 600 .env

---

## 18. Git workflow

The main branch is:

    main

Remote:

    git@github.com:nimahamed88/study-circle.git

Before making changes:

    git pull origin main

After making changes:

    git status
    git add .
    git commit -m "Describe the change"
    git push origin main

Keep commits reasonably focused.

Example:

    git commit -m "Add journal club resources"

rather than putting unrelated changes into the same commit.

---

## 19. Before deploying

Always run:

    python manage.py check

For production-related changes, also consider:

    python manage.py check --deploy

Remember that `check --deploy` can report configuration recommendations that are separate from application errors.

---

## 20. Security rules

Never commit or share:

- production `.env`
- `SECRET_KEY`
- PostgreSQL passwords
- SSH private keys
- Hetzner account credentials
- personal GitHub access tokens

Do not use another person's SSH private key.

If another developer needs server access, create a separate Linux account or add their public SSH key to an appropriate account.

For website content administration, a person only needs a Django admin account and does not need SSH access.

---

## 21. Roles

There are currently two conceptually different levels of access.

### Content administrator

Needs:

    https://neurosciensemble.org/admin/

Can manage:

- Members
- Subgroups
- Sessions
- Session resources

Does NOT need:

- VPS access
- PostgreSQL access
- `.env`
- SSH private keys

### Developer/server administrator

Needs additional access to:

- GitHub repository
- development environment
- VPS
- deployment process

This level should only be given when necessary.

---

## 22. Current public website

Main website:

    https://neurosciensemble.org

Admin:

    https://neurosciensemble.org/admin/

Programme:

    https://neurosciensemble.org/programme/

Members:

    https://neurosciensemble.org/members/

Subgroups:

    https://neurosciensemble.org/subgroups/

Calendar feed:

    https://neurosciensemble.org/calendar.ics

---

## 23. Project conventions

When modifying the site:

- Preserve the existing visual language unless intentionally redesigning it.
- Keep public terminology consistent: "Member", "Subgroup", "Session".
- Keep the Django model name `Speaker` unless there is a strong reason to migrate it.
- Use Django's timezone-aware datetimes.
- Keep the production database as the source of truth for website content.
- Keep secrets outside Git.
- Test locally before deploying.
- Do not expose Gunicorn port 8000 publicly.