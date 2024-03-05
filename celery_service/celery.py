from celery import Celery

from config.config import settings

celery_app = Celery(
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "celery_service.tasks.saving_transactions",
    ],
)
celery_app.autodiscover_tasks()
