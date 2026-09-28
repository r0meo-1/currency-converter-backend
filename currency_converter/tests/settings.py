SECRET_KEY = 'isolated-api-tests-only'
INSTALLED_APPS = ['rest_framework']
ROOT_URLCONF = 'api.urls'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
}
DATABASES = {}
CELERY_BROKER_URL = 'memory://'
