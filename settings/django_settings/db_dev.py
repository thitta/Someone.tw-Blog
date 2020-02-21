import os

DB_NAME = "db_dev.sqlite3"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), DB_NAME)
    }
}

CONN_MAX_AGE = 60 * 5 * 1
