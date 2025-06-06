from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from database.requests import UserRole
import logging


def keyboard_start() -> ReplyKeyboardMarkup:
    """
    Стартовая клавиатура для каждой роли
    :param role:
    :return:
    """
    logging.info("keyboard_start")
    button_1 = KeyboardButton(text='Учеты')
    button_2 = KeyboardButton(text='Работа с товаром')
    button_3 = KeyboardButton(text='Контакты')
    button_4 = KeyboardButton(text='Наставничество')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2], [button_3, button_4]],
                                   resize_keyboard=True)
    return keyboard


def keyboard_accounting() -> InlineKeyboardMarkup:
    logging.info("keyboard_accounting")
    button_1 = InlineKeyboardButton(text='Методичка по внутренним учетам', callback_data=f'accounting_training_manual')
    button_2 = InlineKeyboardButton(text='Почта для заявки на учет', callback_data=f'accounting_mail_account')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboard_work_product() -> InlineKeyboardMarkup:
    logging.info("keyboard_work_product")
    button_1 = InlineKeyboardButton(text='Коррекции', callback_data=f'product_correction_file')
    button_2 = InlineKeyboardButton(text='Полезные рутины', callback_data=f'product_useful_routines')
    button_3 = InlineKeyboardButton(text='Частые ошибки и вопросы',
                                    callback_data=f'product_сommon_mistakes_and_questions')
    button_4 = InlineKeyboardButton(text='Посчитать оптимальный КСО',
                                    callback_data=f'product_сalculate_the_optimal_CSR')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]],)
    return keyboard


def keyboard_mentoring() -> InlineKeyboardMarkup:
    logging.info("keyboard_mentoring")
    button_1 = InlineKeyboardButton(text='Цель и задачи=-зх',
                                    callback_data=f'mentoring_goals_and_objectives')
    button_2 = InlineKeyboardButton(text='Подать заявку', callback_data=f'mentoring_submit_a_request')
    button_back = InlineKeyboardButton(text='Назад', callback_data=f'back')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard
