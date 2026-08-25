import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

celery_app = Celery(
    "agentbuilder",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
    include=["app.tasks.document_tasks"],  # <-- add this
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)