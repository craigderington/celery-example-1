import os

# Debug
DEBUG=True

# Celery Settings
CELERY_BROKER_URL = "pyamqp://rabbitmq:5672/"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
TASK_SERIALIZER = "json"
RESULT_SERIALZIER = "json"
ACCEPT_CONTENT = ["json"]

# Timezome
TIMEZONE = "America/New_York"
ENABLE_UTC = True

# APIs
IPINFO_API_URL = "http://ip-api.com/json/"
NEUTRINO_API_URL = "https://neutrinoapi.com/"

# Environment Settings
# NEUTRINO_API_KEY = os.environ.get("NEUTRINO_API_KEY")
# NEUTRINO_API_USERNAME = os.environ.get("NEUTRINO_API_USERNAME")
# BIGFIX_USER = os.environ.get("BF_USER")
# BIGFIX_PWD = os.environ.get("BF_PWD")
