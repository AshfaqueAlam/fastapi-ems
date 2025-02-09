from celery import Celery
from celery.schedules import crontab

from core.config import config

celery_app = Celery(
    "worker",
    backend=config.CELERY_BACKEND_URL,
    broker=config.CELERY_BROKER_URL,
)

# celery_app.conf.task_routes = {"worker.celery_worker.test_celery": "test-queue"}
# celery_app.conf.update(task_track_started=True)
celery_app.conf.task_track_started = False
celery_app.conf.worker_hijack_root_logger = False

celery_app.autodiscover_tasks(["worker"], force=True)

import worker.tasks.update_completed_events

celery_app.conf.beat_schedule = {
    "update-completed-events-every-minute": {
        "task": "worker.tasks.update_completed_events",
        "schedule": crontab(minute="*"),
    }
}
celery_app.conf.timezone = "UTC"
