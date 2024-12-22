import celery
import logging

from app.database.models.ticket import Ticket
from app.database.models.user import User

from app.database.queries.create_database_tables import create_database_tables
from app.database.queries.delete_ticket import delete_ticket
from app.database.queries.get_all_user_tickets import get_all_user_tickets
from app.database.queries.get_ticket import get_ticket
from app.database.queries.get_user import get_user
from app.database.queries.set_ticket import set_ticket
from app.database.queries.set_user import set_user
from app.database.queries.update_user import update_user


app = celery.Celery('tasks', broker='redis://redis:6379/0')


app.conf.update(
    task_routes = {
        'app.tasks.celery.*': {'queue': 'database_queues'}
    },
    broker_connection_retry_on_startup = True,
    result_backend = 'redis://redis:6379/0',
)


@app.task
def create_database_tables_task() -> None:
    logging.info('Creating database tables...')
    create_database_tables()
    logging.info('Database tables created.')


@app.task
def delete_ticket_task(ticket_id: int) -> None:
    logging.info(f'Deleting ticket {ticket_id}...')
    delete_ticket(ticket_id)
    logging.info(f'Ticket {ticket_id} deleted.')


@app.task
def get_all_user_tickets_task(telegram_id: int) -> list:
    logging.info(f'Getting all user tickets for user {telegram_id}...')
    return get_all_user_tickets(telegram_id)


@app.task
def get_ticket_task(ticket_id: int) -> Ticket | None:
    logging.info(f'Getting ticket {ticket_id}...')
    return get_ticket(ticket_id)


@app.task
def get_user_task(telegram_id: int) -> User | None:
    logging.info(f'Getting user {telegram_id}...')
    return get_user(telegram_id)


@app.task
def set_ticket_task(telegram_id: int, ticket_id: int, chat_id: int) -> None:
    logging.info(f'Setting ticket {ticket_id} for user {telegram_id}...')
    set_ticket(telegram_id, ticket_id, chat_id)
    logging.info(f'Ticket {ticket_id} set for user {telegram_id}.')


@app.task
def set_user_task(telegram_id: int) -> None:
    logging.info(f'Setting user {telegram_id}...')
    set_user(telegram_id)
    logging.info(f'User {telegram_id} set.')


@app.task
def update_user_task(telegram_id: int, **kwargs) -> None:
    logging.info(f'Updating user {telegram_id}...')
    update_user(telegram_id, **kwargs)
    logging.info(f'User {telegram_id} updated.')