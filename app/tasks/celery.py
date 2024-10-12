import celery

from app.database.models.ticket import Ticket
from app.database.models.user import User

from app.database.queue.create_database import create_database
from app.database.queue.delete_ticket import delete_ticket
from app.database.queue.get_all_user_tickets import get_all_user_tickets
from app.database.queue.get_ticket import get_ticket
from app.database.queue.get_user import get_user
from app.database.queue.set_ticket import set_ticket
from app.database.queue.set_user import set_user
from app.database.queue.update_user import update_user


app = celery.Celery('tasks', broker='redis://localhost:6379/0')


app.conf.update(
    task_routes = {
        'app.tasks.celery.*': {'queue': 'database_queues'}
    },
    broker_connection_retry_on_startup = True,
    result_backend = 'redis://localhost:6379/0',
)


@app.task
def create_database_task() -> None:
    create_database()


@app.task
def delete_ticket_task(ticket_id: int) -> None:
    delete_ticket(ticket_id)


@app.task
def get_all_user_tickets_task(telegram_id: int) -> list:
    return get_all_user_tickets(telegram_id)


@app.task
def get_ticket_task(ticket_id: int) -> Ticket | None:
    return get_ticket(ticket_id)


@app.task
def get_user_task(telegram_id: int) -> User | None:
    return get_user(telegram_id)


@app.task
def set_ticket_task(telegram_id: int, ticket_id: int, chat_id: int) -> None:
    set_ticket(telegram_id, ticket_id, chat_id)


@app.task
def set_user_task(telegram_id: int) -> None:
    set_user(telegram_id)


@app.task
def update_user_task(telegram_id: int, **kwargs) -> None:
    update_user(telegram_id, **kwargs)