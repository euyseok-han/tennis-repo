"""Settings specific to this application only (no Django or third-party settings)"""
AUTH_USER_MODEL = 'match.User'
MEDIA_ROOT = BASE_DIR / 'core/static/image'  # type:ignore
MEDIA_URL = 'images/'
IN_DOCKER = False
