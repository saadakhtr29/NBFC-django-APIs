import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Dynamic host configuration - Single point of truth
HOST_IP = os.getenv('HOST_IP', '127.0.0.1')
HOST_DOMAIN = os.getenv('HOST_DOMAIN', HOST_IP)

# Auto-generate allowed hosts from HOST_IP
DYNAMIC_HOSTS = [
    HOST_IP,
    HOST_DOMAIN,
    '0.0.0.0',
    'localhost',
    '127.0.0.1',
    'web',  # Docker service name
]

# Allow custom ALLOWED_HOSTS override or use dynamic
CUSTOM_ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '')
if CUSTOM_ALLOWED_HOSTS:
    ALLOWED_HOSTS = CUSTOM_ALLOWED_HOSTS.split(',')
else:
    ALLOWED_HOSTS = DYNAMIC_HOSTS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    
    # Local apps
    'nbfc_accounts.apps.NbfcAccountsConfig',
    'nbfc_organizations.apps.NbfcOrganizationsConfig',
    'nbfc_employees.apps.NbfcEmployeesConfig',
    'nbfc_loans.apps.NbfcLoansConfig',
    'nbfc_repayments.apps.NbfcRepaymentsConfig',
    'nbfc_attendance.apps.NbfcAttendanceConfig',
    'nbfc_salaries.apps.NbfcSalariesConfig',
    'nbfc_documents.apps.NbfcDocumentsConfig',
    'nbfc_settings.apps.NbfcSettingsConfig',
    'nbfc_auth.apps.AuthConfig',
    'nbfc_bulk_upload.apps.BulkUploadConfig',
    'nbfc_dashboard.apps.DashboardConfig',
    'nbfc_transaction_logs.apps.TransactionLogsConfig',
    'nbfc_loan_deficit.apps.LoanDeficitConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nbfc_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nbfc_django.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, os.getenv('STATIC_ROOT', 'staticfiles'))

# Additional static files directories (for development)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# Static files finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT', 'media'))

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'nbfc_accounts.User'

# URL Configuration
APPEND_SLASH = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# CORS settings - Auto-generate from HOST_IP
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Auto-generate CORS origins
FRONTEND_PORT = '3000'
API_PORT = '8000'
ADMIN_PORT = '80'

DYNAMIC_CORS_ORIGINS = [
    f"http://{HOST_IP}:{FRONTEND_PORT}",
    f"https://{HOST_IP}:{FRONTEND_PORT}",
    f"http://{HOST_IP}:{API_PORT}",
    f"http://{HOST_IP}:{ADMIN_PORT}",
    f"http://{HOST_IP}",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Allow custom CORS origins or use dynamic
CUSTOM_CORS_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '')
if CUSTOM_CORS_ORIGINS:
    CORS_ALLOWED_ORIGINS = CUSTOM_CORS_ORIGINS.split(',')
else:
    CORS_ALLOWED_ORIGINS = DYNAMIC_CORS_ORIGINS

# Security Headers Configuration
SECURE_CROSS_ORIGIN_OPENER_POLICY = None  # Disable COOP for IP-based access
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Since you're using IP address, we need to be less strict
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0  # Disable HSTS for IP access
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Content Security Policy (optional but recommended)
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:")

# X-Frame options
X_FRAME_OPTIONS = 'SAMEORIGIN'