import os

# Configuration email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Pour le développement
EMAIL_HOST = 'smtp.gmail.com'  # À configurer pour la production
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre@email.com'
EMAIL_HOST_PASSWORD = 'votre_mot_de_passe'

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ajoutez ces lignes pour le développement
DEBUG = True
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]