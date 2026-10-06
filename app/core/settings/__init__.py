# Django settings for the SalesIQ project.
# These settings are organized to support multiple environments (local, production, testing) using environment variables
# core/settings/__init__.py

from decouple import config


ENVIRONMENT = config("ENV", default="local")

if ENVIRONMENT == "local":
    from .local import *

elif ENVIRONMENT == "prod":
    from .prod import *
    
elif ENVIRONMENT == "test":
    from .test import *
    
else:
    raise ValueError(f"Invalid environment: {ENVIRONMENT}")