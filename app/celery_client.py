from celery import Celery
import os

broker_url = os.getenv("CELERY_BROKER_URL", "")
backend_url = os.getenv("CELERY_RESULT_BACKEND", broker_url)


if not broker_url or not backend_url:
    raise RuntimeError(
        "Missing CELERY_BROKER_URL or CELERY_RESULT_BACKEND in environment."
    )


celery_app = Celery("fileflow", broker=broker_url, backend=backend_url)
