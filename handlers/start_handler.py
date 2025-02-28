from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import start_keyboard as kb
from config_data.config import Config, load_config
from database import requests as rq
from database.models import User
from utils.error_handling import error_handler
from filter.admin_filter import check_super_admin

import logging
from datetime import datetime

router = Router()
config: Config = load_config()


class PersonalData(StatesGroup):
    fullname = State()
    personal_account = State()
    phone = State()


@router.message(CommandStart())
@error_handler
async def process_start_command_user(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обработки запуска бота или ввода команды /start
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await state.set_state(state=None)
    # добавление пользователя в БД если еще его там нет
    user: User = await rq.get_user_tg_id(tg_id=message.from_user.id)
    if not user:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "user_name"
        data_user = {"tg_id": message.from_user.id,
                     "username": username}
        await rq.add_user(data=data_user)
    await message.answer(text='Вас приветствует телеграмм бот, созданный командой учетчиков Санкт-Петербурга.\n'
                              'Он предназначен для систематизации информации по проведению учетов'
                              ' и работой с товаром.\n'
                              'Для того что бы найти нужную информацию выберите соответствующий раздел в меню.',
                         reply_markup=kb.keyboard_start())


@router.message(F.text == 'Учеты')
@error_handler
async def change_role_admin(message: Message, state: FSMContext, bot: Bot):
    """

    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('change_role_admin')
    await message.answer(text=f'Выберите раздел',
                         reply_markup=kb.keyboard_accounting())


@router.message(F.text == 'Работа с товаром')
@error_handler
async def change_role_admin(message: Message, state: FSMContext, bot: Bot):
    """

    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('change_role_admin')
    await message.answer(text=f'Выберите раздел',
                         reply_markup=kb.keyboard_work_product())


@router.message(F.text == 'Контакты')
@error_handler
async def change_role_admin(message: Message, state: FSMContext, bot: Bot):
    """

    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('change_role_admin')
    await message.answer(text='Контакты всех учетчиков:\n'
                              '- Поджидаева Таня @kotovska\n'
                              '- Сердюков Антон @Dear_Friend1986\n'
                              '- Тиманин Александр @SomeAlexTim\n'
                              '- Шелепугина Анна @AnnShelli\n'
                              'Руководитель направления учетов:\n'
                              '- Макаренко Ксения @coffeinthecity')


@router.message(F.text == 'Наставничество')
@error_handler
async def change_role_admin(message: Message, state: FSMContext, bot: Bot):
    """

    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('change_role_admin')
    await message.answer(text=f'Выберите раздел',
                         reply_markup=kb.keyboard_mentoring())


@router.callback_query(F.data.startswith('accounting_'))
@error_handler
async def process_accounting(callback: CallbackQuery, state: State, bot: Bot):
    """
    Учеты
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_accounting')
    select = callback.data
    await callback.message.delete()
    if select == 'accounting_training_manual':
        await callback.message.answer_document(
            document='BQACAgIAAxkBAAIBHWfB15USGtvVfVVVC2nyNiP9yjYXAAKWaAACmTkQStO4cgrvc4caNgQ',
            caption='Методичка по внутренним учетам'
        )
    elif select == 'accounting_mail_account':
        await callback.message.answer(text=f'Для того что бы подать заявку для проведения учёта необходимо'
                                           f' написать на почту ptm@cantata.ru')


@router.callback_query(F.data.startswith('product_'))
@error_handler
async def process_product_(callback: CallbackQuery, state: State, bot: Bot):
    """
    Работа с товаром
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_product_')
    select = callback.data
    await callback.message.delete()
    if select == 'product_correction_file':
        await callback.message.answer_document(
            document='BQACAgIAAxkBAAIBI2fB2M_7iJczO2fXhJI7pBpE3YNFAAK4aAACmTkQSn4WJ96c0NGVNgQ',
            caption='Памятка по видам коррекций'
        )
    elif select == 'product_useful_routines':
        await callback.message.answer(
            text=f'Полезные рутины:\n\n'
                 f'✅ Каждый день проверять все продажи за вчерашний день (позволяет быстро обнаружить ошибки,'
                 f' которые в дальнейшем невозможно отследить по движению товара; К примеру, в продажу вбит Набор'
                 f' Капучино 200 индивидуал, но не вбиты граммы завариваемого кофе)\n\n'
                 f'✅Каждый день проверять все собранные подарки за предыдущий день (позволяет быстро обнаружить'
                 f' и исправить ошибки в комплектации подарков)\n\n'
                 f'✅ Перед закрытием проверять все коррекции (напиток на смене, дегустации, переброски и т.д.)'
                 f' на правильность типа коррекции, состава и направления коррекции увеличение/уменьшение)\n\n'
                 f'✅ Каждый месяц проверять коррекции на фиктивные приходы и наличие обратного фиктивного прихода.\n\n'
                 f'✅ В чате магазина создать подчат «Переброски» и отписываться туда, когда договариваемся о'
                 f' переброске какого-либо товара, и когда это товар отправили/приняли (позволяет предотвратить'
                 f' ситуации с забытыми/потерянными перебросками). Вместо отдельного подчата также можно'
                 f' использовать хэштег #переброски в основном чате.\n\n'
                 f'✅ В чате магазина создать подчат «Приход товара» и отписываться туда после приемки товара'
                 f' в формате «в сегодняшнем приходе ошибок нет»/ «в сегодняшнем приходе не пришло 5 банок'
                 f' крем-карамели «Шоколадный берег», заявку оформила, отв. Иванова» (позволяет исключить'
                 f' ситуации с пропущенными ошибками на приходе). Вместо отдельного подчата также можно'
                 f' использовать хэштег #приход в основном чате.\n\n'
                 f'✅ В календаре дел планировать подготовку к акциям: за день до начала акции списывать'
                 f' акционный товар и приходовать карточки акций. На следующий день после окончания акции,'
                 f' списывать карточки акций и приходовать оставшийся товар (позволяет исключить ситуации,'
                 f' когда оставшийся после акции товар забывают оприходовать назад, в последствии неправильно'
                 f' корректируя его на внутреннем учете)\n\n'
                 f'✅Еженедельно проверять раздел Заявки на предмет получения ответов на ранее оформленные'
                 f' жалобы (позволяет избежать ситуации, когда жалобу на Заявки подали, но забыли обработать'
                 f' ответ по ней)')
    elif select == 'product_сommon_mistakes_and_questions':
        await callback.message.answer(
            text=f'❗️ <b>Ошибки в направлении коррекции (приход и расход)</b>\n'
                 f'Одна из самых частых ошибок это ошибка в направлении коррекции.\n'
                 f'Направления коррекций:\n'
                 f'«Увеличение» - постановка товара на плюс, в следствии фактического его присутствия'
                 f' или корректировки отрицательных остатков\n'
                 f'«Уменьшение» - списание товара, которого нет фактически или планируется его расход'
                 f' (дегустация, списания на акции, прошел срок годности и т.д.)\n\n'
                 f'<b>Что делать, если не верно указали направление коррекции?</b>\n'
                 f'<u>Вариант 1:</u>\n'
                 f'Создаём обратную коррекцию, где указываем верный тип и фиксируем товар в двухкратном'
                 f' размере (для того чтобы исправить коррекцию и фактически выровнять товар) с комментарием'
                 f' «Исправление неверной коррекции ….»\n'
                 f'<u>Вариант 2:</u>\n'
                 f'Создаём обратную коррекцию с комментарием «Исправление неверной коррекции ….» и создаём новую'
                 f' коррекцию с верными значениями и необходимым комментарием.\n\n'
                 f'<b>❗️Не сведены фиктивные коррекции.</b>\n'
                 f'Фиктивная коррекция - парная коррекция с типом «Не учитывать», которая чаще всего используется'
                 f' при перебросках товара между галереями. Первая коррекция добавляет на остаток товар,'
                 f' который уже есть у нас по факту, но еще не загрузился в Retail. Вторая коррекция расходует '
                 f'товар после загрузки приходной накладной, таким образом выравнивая фактические остатки.'
                 f' Суммы приходной и расходной коррекции должны быть одинаковыми (исключение - за время'
                 f' между коррекциями товар успел переоцениться)\n\n'
                 f'<u>Частая ошибка:</u> забывают сводить фиктивные коррекции и не проверяют их наличие.\n'
                 f'Для предотвращения таких ошибок хорошо работает инструмент «кто создал фиктивную коррекцию,'
                 f' тот и создаёт обратный фиктив».\n\n'
                 f'<b>❗️ Не сведены карточки акций.</b>\n'
                 f'Акционные карточки - номенклатура товара для проведения конкретной акции. Подразумевает наличие'
                 f' парных коррекций для начала акции (списываем товар, приходуем карточку акции) и парные коррекции'
                 f' для завершения акции (списываем карточку карточку акции, приходуем товар).\n'
                 f'При анонсе акции на Dashboard выкладывается памятка, в которой подробно прописана техническая'
                 f' часть: тип коррекции, шаги списания товара и установки карточки, а так же прописаны все'
                 f' номенклатуры (самой карточки и какой товар списываем).\n\n'
                 f'<u>Частая ошибка:</u> не выравниваются остатки после прохождения акций.\n'
                 f'Если у вас числится акционная карточка после завершения акции, то велика вероятность расхождения'
                 f' товара.\n'
                 f'Если не сведены акционные карточки, либо сведены некорректно, то высока вероятность, что где-то'
                 f' может быть товар утерян или находится «лишний». А также это снижает эффективность отслеживания'
                 f' акций и нарушение кассовой дисциплины (часто забывают вбить акционные карточки в чеки или'
                 f' наоборот, карточку вбивают, а подарки не выдают).\n\n'
                 f'<b>❗️ Не списан дегустационный товар.</b>\n'
                 f'Списание товара на дегустацию — фактическое списание товара при выставлении/заваривании его на'
                 f' дегустацию гостям или сотрудникам.\n'
                 f'<u>Важно списывать товар по факту.</u> Списание товара на дегустацию постфактум является нарушение'
                 f' приказа № Т11 «Об установлении лимитов и контрагентов списаний на дегустации». В  таком случае'
                 f' товар списывается на тип коррекции «Коррекция» в общий учет товара.\n'
                 f'Списанный на дегустацию товар должен храниться отдельно от основного товара, и по возможности'
                 f' должен иметь понятную маркировку, сигнализирующую о том, что данный товар не подлежит продаже.\n\n'
                 f'<b>❗️Не списан брак.</b>\n'
                 f'Списание на брак — списание испорченного, утилизированного товара на различные контрагенты при '
                 f'разных случая возникновения брака (коррекции «Не учитывать», Брак (утиль на месте), Брак (на склад)).'
                 f' Списания происходят на различные контрагенты, в связи с тем, что за разные формы брака несут'
                 f' ответственность различные отделы.\n\n'
                 f'Тип и правила списания указываются или в автоответе Заявки Виджет, или пишет ответственный за'
                 f' направление, по которому подана жалоба. Важно всегда подавать заявки на бракованный товар, так'
                 f' как это необходимо для принятия решения по товару экспертом, определения типа списания'
                 f'  и статистики по тому или иному товару.\n'
                 f'Если брак не списан своевременно, находится и числится как товар, то он идет в счет учета в'
                 f' материальную ответственность команды.\n'
                 f'Исключение: если подана заявка и по ней еще решается вопрос')
    elif select == 'product_сalculate_the_optimal_CSR':
        await callback.message.answer_document(
            document=f'BQACAgIAAxkBAAIBJGfB3DBha2GR8qdeqYHLff0envpMAAIQaQACmTkQSscv_t0pRyp2NgQ',
            caption='Посчитать оптимальный КСО:')


@router.callback_query(F.data.startswith('mentoring_'))
@error_handler
async def process_mentoring_(callback: CallbackQuery, state: State, bot: Bot):
    """
    Наставничество
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_accounting')
    select = callback.data
    await callback.message.delete()
    if select == 'mentoring_goals_and_objectives':
        await callback.message.answer(
            text='Наставничество — это система, в которой вы приглашаете учетчика в свою галерею для налаживания'
                 ' эффективной системы работы с товаром.\n\n'
                 '🔹Задачи для работы могут быть разные, как и продолжительность такого сотрудничества.\n\n'
                 '🔹Это могут быть несколько смен, где мы разбираем самые частые ошибки, которые совершают сотрудники'
                 ' вашей галереи, и выбираем инструменты для их отработки. А может быть работа на пару месяцев, где мы'
                 ' налаживаем систему внутренних учетов, работаем над правильностью формирования коррекций, помогаем'
                 ' наладить систему работы со сроками годности и так далее. Все будет зависеть от нужд конкретной'
                 ' галереи.\n\n'
                 '🔹Помощь от учетчика можно будет инициировать самостоятельно, написав мне на почту, также,'
                 ' как вы делаете с заявками на учет. И также мы можем обратиться к вам с предложением своей помощи'
                 ' по итогам проведенных учетов, если заметим, что есть много сложностей в работе с товаром.',
        )
    elif select == 'mentoring_submit_a_request':
        await callback.message.answer(text=f'Для того что бы подать заявку для наставничества необходимо'
                                           f' написать на почту ptm@cantata.ru')