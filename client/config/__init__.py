from os import getenv

if getenv("ACODER_CLIENT_ENV") == 'dev':
    from .dev import config
else:
    from .prod import config
