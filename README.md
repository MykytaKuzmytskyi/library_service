# Library service API

The system optimizes the work of library administrators and has an online book borrowing management system.

### Installing using GitHub

Install PostgresSQL and create db

1. Clone the source code:

```bash
git clone https://github.com/Thirteenthskyi/library_service.git
cd library_service
```

2. Install PostgresSQL and create DB.
3. Install modules and dependencies:

```bash
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

4. `.env_sample`
   This is a sample .env file for use in local development.
   Duplicate this file as .env in the root of the project
   and update the environment variables to match your
   desired config. You can use [djecrety.ir](https://djecrety.ir/)

5. Use the command to configure the database and tables:

```bash
python manage.py migrate
```

6. Run Redis server.

7. Run celery for tasks handling:

```bash
celery -A library_service worker -l info
```

8. Start the app:

```bash
python manage.py runserver
```

### Run with docker

Docker should be installed

```commandline
docker-compose up --build
```

### Getting access

- You can use following superuser (or create another one by yourself):
    - Login: `admin@admin.com`
    - Password: `admin12345`
- create user via /api/users/
- get access token via /api/users/token/

## Features

- JWT authenticated
- Admin panel /admin/
- Managing books and borrowings
- Create, update, delete Books
- Create and return Borrowings
- Filtering borrowings by is_active & user_id
- Sending Telegram notifications about each Borrowing creation

*REST API documentation*
----
  **Books Service**

 - POST:      `books/`      - add new 
 - GET:       `books/`      - get a list of books
 - GET:       `books/<id>/` - get book's detail info 
 - PUT/PATCH: `books/<id>/` - update book 
 - DELETE:    `books/<id>/` - delete book

  **Users Service**

 - POST:       `users/`                - register a new user 
 - POST:       `users/token/`          - get JWT tokens
 - POST:       `users/token/refresh/` - refresh JWT token 
 - POST:       `users/token/verify/ `  - verify JWT token
 - GET:        `users/me/`             - get my profile info
 - PUT/PATCH:  `users/me/`             - update profile info

  **Borrowings Service**

 - POST:      `borrowings/`      - add new borrowing 
 - GET:       `borrowings/?user_id=...&is_active=...`- get borrowings by user id and whether is borrowing still active or not
 - GET:       `borrowings/<id>/` - get borrowing's detail info 
 - POST: `borrowings/<id>/return/` - set actual return date

