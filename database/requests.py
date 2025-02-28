from database.models import User, async_session
from sqlalchemy import select
import logging
from dataclasses import dataclass


""" USER """


@dataclass
class UserRole:
    user = "user"
    executor = "executor"
    admin = "admin"


async def add_user(data: dict) -> None:
    """
    Добавление пользователя
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == data['tg_id']))
        if not user:
            session.add(User(**data))
            await session.commit()


async def get_user_tg_id(tg_id: int) -> User:
    """
    Получение информации о пользователе по tg_id
    :param tg_id:
    :return:
    """
    logging.info(f'get_user_tg_id {tg_id}')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
