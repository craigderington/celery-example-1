CELERY_BROKER_URL = "pyamqp://172.17.0.2/"
CELERY_RESULT_BACKEND = "redis://172.17.0.3/"
TASK_SERIALIZER = "json"
RESULT_SERIALZIER = "json"
ACCEPT_CONTENT = ["json", "pickle"]
TIMEZONE = "America/New_York"
ENABLE_UTC = True
