import celery

from app.database.queue.set_user import set_user


celery = 


@celery.task
def set_user_task(telegram_id: int) -> None: