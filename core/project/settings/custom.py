"""Settings specific to this application only (no Django or third-party settings)"""
AUTH_USER_MODEL = 'match.User'
IN_DOCKER = False
print('custom is running!')