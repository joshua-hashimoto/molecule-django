import os

EMAIL_BACKEND = f'django.core.mail.backends.{os.environ.get("EMAIL_BACKEND")}.EmailBackend'
DEFAULT_FROM_EMAIL = 'notification@molecule.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
