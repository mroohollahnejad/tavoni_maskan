from pathlib import Path
import dj_database_url
import os

# ==============================
# مسیر اصلی پروژه
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# تنظیمات امنیتی
# ==============================
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# فقط برای Render
ALLOWED_HOSTS = ['*']

# ==============================
# اپلیکیشن‌ها
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # اپ‌های جانبی
    'django.contrib.humanize',
    'django_jalali',

    # اپ‌های پروژه
    'accounts',
]

# ==============================
# میان‌افزارها
# ترتیب مهم است!
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise برای سرو static در Render
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ==============================
# قالب‌ها
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ==============================
# پایگاه داده (Render + Supabase)
# ==============================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# ==============================
# امنیت رمز عبور
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================
# زبان و زمان
# ==============================
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# ==============================
# فایل‌های استاتیک – مخصوص Render
# ==============================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# فقط در حالت توسعه staticfiles داخلی فعال شود
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'static']

# فعال‌سازی GZip + Compression whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================
# فایل‌های رسانه‌ای
# ==============================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================
# مسیرهای ورود / خروج
# ==============================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# ==============================
# تنظیم کلید اصلی
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
