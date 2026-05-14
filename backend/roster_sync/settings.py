import os
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-secret-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'true').lower() == 'true'
ALLOWED_HOSTS = [host for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',') if host]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'sync_api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'roster_sync.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'roster_sync.wsgi.application'
ASGI_APPLICATION = 'roster_sync.asgi.application'

def _database_settings_from_url(database_url: str) -> dict:
    parsed = urlparse(database_url)
    query = parse_qs(parsed.query)

    if parsed.scheme in {'postgres', 'postgresql', 'pgsql'}:
        host = parsed.hostname or query.get('host', [''])[0]
        port = parsed.port or query.get('port', [''])[0]
        options = {}

        for option_name in ('sslmode', 'target_session_attrs'):
            option_value = query.get(option_name, [''])[-1]
            if option_value:
                options[option_name] = option_value

        database_settings = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': unquote((parsed.path or '').lstrip('/')),
            'USER': unquote(parsed.username or ''),
            'PASSWORD': unquote(parsed.password or ''),
            'HOST': unquote(host or ''),
            'PORT': str(port or ''),
        }

        if options:
            database_settings['OPTIONS'] = options

        return database_settings

    if parsed.scheme == 'sqlite':
        sqlite_path = unquote(parsed.path or '')
        if not sqlite_path:
            sqlite_path = BASE_DIR / 'db.sqlite3'

        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': sqlite_path,
        }

    raise ValueError(f'Unsupported database scheme: {parsed.scheme}')


def _default_database_settings() -> dict:
    cloud_sql_connection_name = os.environ.get('INSTANCE_CONNECTION_NAME') or os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    database_host = os.environ.get('POSTGRES_HOST')

    if not database_host and cloud_sql_connection_name:
        database_host = f'/cloudsql/{cloud_sql_connection_name}'

    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'dantedoglcb'),
        'USER': os.environ.get('POSTGRES_USER', 'dantedoglcb'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'dantedoglcb'),
        'HOST': database_host or 'postgres',
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }


DATABASES = {
    'default': _database_settings_from_url(os.environ['DATABASE_URL'])
    if os.environ.get('DATABASE_URL')
    else _default_database_settings()
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
FILE_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024

GOOGLE_OAUTH_CLIENT_IDS = [
    client_id.strip()
    for client_id in os.environ.get('GOOGLE_OAUTH_CLIENT_IDS', os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')).split(',')
    if client_id.strip()
]