if IN_DOCKER: # type: ignore
    print('Running IN_DOCKER  mode...')
    assert MIDDLEWARE[:1] == ['django.middleware.security.SecurityMiddleware',] # type: ignore
