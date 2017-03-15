#!/usr/bin/env bash
rm -r migrations
rm app.db
python manage.py create_db
python manage.py db init
python manage.py db upgrade
python manage.py db migrate
python manage.py create_fake_users 100
python manage.py rununicorn -p 9000 -w 10
