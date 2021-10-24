import random
import re

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import markups
from config import bot_token
from aiogram import Bot, Dispatcher, executor, types
from db import create_table, add_user, get_count_users, has_referrer, get_all_users, add_referrer, get_username_from_id, \
    get_id_from_username, get_ref_count_by_id, get_balance, ban_user_by_id, check_for_ban, set_balance, is_worker, \
    add_worker, del_worker, is_chosen_pay_meth, set_payment_methods_and_data, get_paymeths, get_profile, get_all_ids
from asyncio import sleep
import datetime
from markups import menu, admin_menu, refresh, payment_methods, chose_p_m


class EditMsg(StatesGroup):
    start_message = State()
    rules_message = State()
    news_message = State()


class GetPayMeth(StatesGroup):
    meth = State()
    username = State()


class SendPM(StatesGroup):
    message = State()


class Ref(StatesGroup):
    referrer_id = State()
    del_ref = State()


class Ban(StatesGroup):
    banned_username = State()


class AddBalance(StatesGroup):
    username_and_amount = State()


data = ''
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
create_table()


@dp.message_handler(commands='start')
async def start(msg: types.Message):
    if not markups.tech:
        f_name = msg.from_user.first_name
        l_name = msg.from_user.last_name
        username = msg.from_user.username
        user_id = msg.from_user.id
        if user_id in [465379386, 1974238472]:
            add_user(user_id, f_name, username, is_worker='True')
        else:
            add_user(user_id, f_name, username, is_worker='False')
        if not check_for_ban(msg.from_user.id):
            if not has_referrer(user_id):
                if ' ' in msg.text:
                    referrer_id = msg.text.split()[1]
                    if referrer_id.isnumeric():
                        referrer_id = int(referrer_id)
                        if user_id != referrer_id:
                            add_referrer(user_id, referrer_id)
                            referrer_username = get_username_from_id(referrer_id)
                            await bot.send_message(465379386,
                                                   f'У пользователя @{referrer_username} новый реферал — @{username}')
                            await bot.send_message(referrer_id, f'У вас новый реферал — @{username}')
                            await dp.current_state(user=user_id).reset_state()

            if is_worker(user_id):
                await msg.answer(f"""Здравствуйте, {f_name.title()}!
Я Бот. Помогу получить от 1 000 до 100.000 ₽! 🤖""", reply_markup=menu)
            else:
                await msg.answer(f"""Здравствуйте, {f_name.title()}!
Я Бот. Помогу получить от 1 000 до 100.000 ₽! 🤖""")
            await sleep(1)
            await msg.answer("Подбираю компании...⏳")
            await sleep(1)
            await msg.answer("Готово! ✅")
            await sleep(1)
            await msg.answer(f"""Информация для вас:
ФИ:  {f_name} {l_name if l_name else ""}
Дата и время подачи заявки:  {datetime.datetime.now().strftime(f"%d.%m.%Y %H:%M:%S")}
Номер заявки: #{random.randint(30, 9998)}""")
            await sleep(1)
            await msg.answer(markups.start_message, reply_markup=refresh)
        else:
            await msg.answer('Вы забанены.')
    else:
        await msg.answer('Бот на технических работах.')


@dp.callback_query_handler(lambda call: call.data == 'edit_start_message')
async def get_msg_to_edit(call: types.CallbackQuery):
    await call.message.answer('Введите сообщение для изменения')
    await EditMsg.start_message.set()


@dp.message_handler(state=EditMsg.start_message)
async def edit_start(message: types.Message):
    text = message.text
    markups.start_message = text
    await message.answer('Успешно. /start')
    await dp.current_state(user=message.from_user.id).reset_state()


@dp.callback_query_handler(lambda call: call.data == 'refresh')
async def refresher(call: types.CallbackQuery):
    if not markups.tech:
        await call.message.answer(f"""♻ 1. Перейдите по ссылке
📝 2. Заполните анкету
💳 3. Деньги придут через 3 минуты
👇🏻👇🏻👇🏻

⚡Moneyman👉 https://finlg.ru/SHHON 

💸ТУРБОЗАЙМ 👉 https://finlg.ru/SHHOO

💸Займер 👉 https://finlg.ru/SHHOQ

💸ДоЗарплаты👉 https://finlg.ru/SHHOP

⚠ Заполните несколько анкет для 100% одобрения!""", reply_markup=refresh)
    else:
        await call.message.answer('Бот на технических работах.')


@dp.message_handler(commands='admin')
async def admin(msg: types.Message):
    if msg.from_user.id in [465379386, 1974238472]:
        await msg.answer(f'Привет, {msg.from_user.first_name.title()}!\n', reply_markup=admin_menu)


@dp.message_handler(lambda message: message.text == 'Счета')
async def get_check(message: types.Message):
    try:
        if is_worker(message.from_user.id):
            if not markups.tech and not check_for_ban(message.from_user.id):
                start = datetime.date(year=2021, month=10, day=9)
                now = datetime.date.today()
                dif = now - start
                if dif == 15:
                    start = datetime.date.today()
                else:
                    dif1 = 15 - dif.days
                    if dif1 != 1:
                        await message.answer(
                            f'Следующая выплата ({get_balance(message.from_user.id)} руб.) будет через {dif1} дней')
                    else:
                        await message.answer('Ожидайте выплату в течение 3-ех рабочий дней.')
            else:
                await message.answer('Вы забанены.')
        else:
            await message.answer('Доступ запрещен.')
    except TypeError:
        await message.answer('Пропишите /start и попробуйте еще раз.')


@dp.message_handler(lambda message: message.text == 'Профиль')
async def get_balance_from_tg(message: types.Message):
    try:
        if is_worker(message.from_user.id):
            if not markups.tech and not check_for_ban(message.from_user.id):
                f_name = message.from_user.first_name
                l_name = message.from_user.last_name
                user_id = message.from_user.id
                third = f'Количество приглашенных рефералов: {get_ref_count_by_id(user_id)}\n' if get_ref_count_by_id(
                    user_id) != 0 else ''

                await message.answer(f'Фамилия и имя: {f_name} {l_name if l_name else ""}\n'
                                     f'ID: {user_id}\n'
                                     f'{third}'
                                     f'Ваш баланс: {get_balance(user_id)}',
                                     reply_markup=payment_methods)
            else:
                await message.answer('Вы забанены.')
        else:
            await message.answer('Доступ запрещен.')
    except TypeError:
        await message.answer('Пропишите /start и попробуйте снова')


@dp.callback_query_handler(lambda call: call.data == 'payment_methods')
async def pay_meths(call: types.CallbackQuery):
    if not is_chosen_pay_meth(call.from_user.id):
        await call.message.answer('Выберите способ выплаты ниже.', reply_markup=chose_p_m)
    else:
        await call.message.answer('Нажмите, чтобы изменить способ выплаты', reply_markup=markups.change_paymeth)


@dp.callback_query_handler(lambda call: call.data == 'get_pay_meth')
async def get_pppmmm(call: types.CallbackQuery):
    await call.message.answer('Введите username человека.')
    await GetPayMeth.username.set()


@dp.message_handler(state=GetPayMeth.username)
async def print_pm(message: types.Message):
    username = message.text[1:] if '@' in message.text else message.text
    if username in get_all_users():
        user_id = get_id_from_username(username)
        meth = get_paymeths(user_id)
        refs = get_ref_count_by_id(user_id)
        third = f'Количество приглашенных рефералов: {refs}\n' if refs != 0 else ''
        await message.answer(f'Пользователь: {"@" + username}\n'
                             f'ID: {user_id}\n'
                             f'{third}'
                             f'Баланс: {get_balance(user_id)}\n'
                             f'Количество рефералов: {refs}\n'
                             f'{meth if meth else ""}')
        await dp.current_state(user=message.from_user.id).reset_state()

    else:
        await message.answer('Пользователь не найден.')
        await dp.current_state(user=message.from_user.id).reset_state()


@dp.callback_query_handler(lambda call: call.data == 'chose_meth')
async def pay_meths(call: types.CallbackQuery):
    await call.message.answer('Выберите способ выплаты ниже.', reply_markup=chose_p_m)


@dp.callback_query_handler(lambda call: call.data in ['chose_qiwi', 'chose_card', 'chose_web'])
async def chose_paymeth(call: types.CallbackQuery):
    global data
    data = call.data[6:].title()
    await call.message.answer('Пожалуйста, введите данные для отправки.')
    await GetPayMeth.meth.set()


@dp.message_handler(state=GetPayMeth.meth)
async def get_meth(message: types.Message):
    global data
    data += f' {message.text}'
    await message.answer('Спасибо!')
    set_payment_methods_and_data(message.from_user.id, data)
    await bot.send_message(465379386, f'Пользователь: @{message.from_user.username}\n'
                                      f'Выплата: {": ".join(data.split())}')
    await bot.send_message(1974238472, f'Пользователь: @{message.from_user.username}\n'
                                       f'Выплата: {": ".join(data.split())}')
    await dp.current_state(user=message.from_user.id).reset_state()


@dp.callback_query_handler(lambda call: call.data == 'count users')
async def counter_users(call: types.CallbackQuery):
    await call.message.answer(f'Общее количество пользователей: {get_count_users()}')


@dp.callback_query_handler(lambda call: call.data == 'add work')
async def add_word(call: types.CallbackQuery):
    await call.message.answer('Введите username человека, которому нужно выдать ворк панель.')
    await Ref.referrer_id.set()


@dp.callback_query_handler(lambda call: call.data == 'del work')
async def add_word(call: types.CallbackQuery):
    await call.message.answer('Введите username человека, которому нужно выдать ворк панель.')
    await Ref.del_ref.set()


@dp.message_handler(state=Ref.del_ref)
async def give_work_panel(msg: types.Message):
    referrer_username = msg.text[1:] if '@' in msg.text else msg.text
    if referrer_username not in get_all_users():
        await msg.answer('Пользователь не найден. Попросите его написать боту любоe сообщение.')
        await dp.current_state(user=msg.from_user.id).reset_state()
    else:
        referrer_id = get_id_from_username(referrer_username)
        del_worker(referrer_id)
        await bot.send_message(referrer_id, 'Вы были удалены из воркера.')
        await msg.answer(f'Пользователь был удален.')
        await dp.current_state(user=msg.from_user.id).reset_state()


@dp.callback_query_handler(lambda call: call.data == 'ban')
async def ban_user(call: types.CallbackQuery):
    await call.message.answer('Введите юзернейм пользователя')
    await Ban.banned_username.set()


@dp.message_handler(state=Ban.banned_username)
async def get_banned(message: types.Message):
    if message.text.lower() != 'отмена':
        if len(message.text.split()) != 1:
            await message.answer('Отправьте ТОЛЬКО юзернейм.')
            await dp.current_state(user=message.from_user.id).reset_state()
        else:
            username = message.text[1:] if '@' in message.text else message.text
            user_id = get_id_from_username(username)
            if username.lower() not in list(map(lambda x: x.lower(), get_all_users())):
                await message.answer('Неверный юзернейм либо пользователь не писал боту.')
                await dp.current_state(user=message.from_user.id).reset_state()
            else:
                if not check_for_ban(user_id):
                    ban_user_by_id(user_id)
                    await message.answer('Пользователь успешно забанен.')
                    await dp.current_state(user=message.from_user.id).reset_state()
                else:
                    await message.answer('Пользователь уже забанен.')
                    await dp.current_state(user=message.from_user.id).reset_state()


@dp.message_handler(state=Ref.referrer_id)
async def give_work_panel(msg: types.Message):
    referrer_username = msg.text[1:] if '@' in msg.text else msg.text
    if referrer_username not in get_all_users():
        await msg.answer('Пользователь не найден. Попросите его написать боту любоe сообщение.')
        await dp.current_state(user=msg.from_user.id).reset_state()
    else:
        add_worker(get_id_from_username(referrer_username))
        referrer_id = get_id_from_username(referrer_username)
        url = f't.me/zaem0nline_bot?start={referrer_id}'
        await bot.send_message(referrer_id, 'Вам была выдана воркпанель.')
        await msg.answer(f'Готово!\nВаша ссылка: {url}')
        await dp.current_state(user=msg.from_user.id).reset_state()


@dp.callback_query_handler(lambda call: call.data == 'get_ref_url')
async def get_my_url(call: types.CallbackQuery):
    url = f't.me/zaem0nline_bot?start={call.from_user.id}'
    add_worker(call.message.from_user.id)
    await call.message.answer(f'Ваша реферальная ссылка — {url}')


@dp.callback_query_handler(lambda call: call.data == 'set_bank')
async def add_balance(call: types.CallbackQuery):
    await call.message.answer('Введите через пробел юзернейм и нужный баланс.')
    await AddBalance.username_and_amount.set()


@dp.message_handler(state=AddBalance.username_and_amount)
async def get_user_and_amount(message: types.Message):
    if len(message.text.split()) == 2 and message.text.lower() != 'отмена':
        username, amount = message.text.split()
        username = username[1:] if '@' in username else username
        try:
            user_id = get_id_from_username(username)
        except TypeError:
            await message.answer('Обьект не находится в базе данных. Пропишите /start.')
            await AddBalance.username_and_amount.set()
        else:
            if not amount.isnumeric():
                await message.answer('Неверное количество')

            else:
                amount = int(amount)
                set_balance(user_id, amount)
                await message.answer('Баланс обновлен.')
                await dp.current_state(user=user_id).reset_state()


@dp.callback_query_handler(lambda call: call.data == 'send pm')
async def send_private(call: types.CallbackQuery):
    await call.message.answer('Введите через пробел юзернейм и нужное сообщение.')
    await SendPM.message.set()


@dp.message_handler(state=SendPM.message)
async def send_pm(message: types.Message):
    if len(message.text.split()) >= 2:
        username, text = message.text.split()[0], message.text.split()[1:]
        username = username[1:] if '@' in username else username
        print(username, text)
        try:
            user_id = get_id_from_username(username)
        except TypeError:
            await message.answer('Пользователь не находится в базе данных.')
        else:
            await bot.send_message(user_id, 'От администратора: ' + ' '.join(text))
            await message.answer('Сообщение успешно доставлено')
            await dp.current_state(user=user_id).reset_state()
    else:
        await message.answer('Нет текста отправки')
        await dp.current_state(user=message.from_user.id).reset_state()


@dp.callback_query_handler(lambda call: call.data in ['on', 'off'])
async def tech_works(call: types.CallbackQuery):
    if call.data == 'on':
        await call.message.answer('Технические работы включены')
        markups.tech = True
    else:
        await call.message.answer('Технические работы выключены')
        markups.tech = False


class Mail(StatesGroup):
    work_message = State()
    user_message = State()


@dp.callback_query_handler(lambda call: call.data == 'all_mailing')
async def get_mailing_message(call: types.CallbackQuery):
    await call.message.answer('Введите сообщение для рассылки')
    await Mail.user_message.set()


@dp.message_handler(state=Mail.user_message)
async def send_mail_user(message: types.Message):
    text = message.text
    if text != '-':
        await message.answer('Рассылка началась...')
        c = 0
        for user_id in get_all_ids():
            try:
                await bot.send_message(user_id, text)
            except Exception:
                await message.answer(f'Не удалось отправить сообщение пользователю {get_username_from_id(user_id)}')
            else:
                c += 1
        else:
            await message.answer(f'Рассылка успешно закончена\nКоличество пользователей получивших сообщение: {c}')
            await dp.current_state(user=message.from_user.id).reset_state()
    else:
        await message.answer('Действие отменено.')
        await dp.current_state(user=message.from_user.id).reset_state()


@dp.callback_query_handler(lambda call: call.data == 'mailing')
async def get_mailing_message(call: types.CallbackQuery):
    await call.message.answer('Введите сообщение для рассылки')
    await Mail.work_message.set()


@dp.message_handler(state=Mail.work_message)
async def send_mail(message: types.Message):
    text = message.text
    if text != '-':
        await message.answer('Рассылка началась...')
        c = 0
        for user_id in get_all_ids():
            if is_worker(user_id):
                try:
                    await bot.send_message(user_id, 'Admin: ' + text)
                except Exception:
                    await message.answer(f'Не удалось отправить сообщение пользователю {get_username_from_id(user_id)}')
                else:
                    c += 1
        else:
            await message.answer(f'Рассылка успешно закончена\nКоличество пользователей получивших сообщение: {c}')
            await dp.current_state(user=message.from_user.id).reset_state()
    else:
        await message.answer('Действие отменено.')
        await dp.current_state(user=message.from_user.id).reset_state()


@dp.message_handler(commands='info')
async def send_info(message: types.Message):
    if not markups.tech:
        await message.answer('Created by @prog_heroku')
    else:
        await message.answer('Бот на технических работах.')


@dp.message_handler(commands='rules')
async def send_rules(message: types.Message):
    if not markups.tech:
        await message.answer(markups.rules_message)
    else:
        await message.answer('Бот на технических работах.')


@dp.callback_query_handler(lambda call: call.data == 'edit_rules')
async def get_edit_rules(call: types.CallbackQuery):
    await call.message.answer('Введите новое сообщение для команды /rules')
    await EditMsg.rules_message.set()


@dp.message_handler(state=EditMsg.rules_message)
async def edit_rules_message(message: types.Message):
    text = message.text
    markups.rules_message = text
    await message.answer('Успешно изменено. /rules')
    await dp.current_state(user=message.from_user.id).reset_state()


@dp.message_handler(commands='news')
async def send_rules(message: types.Message):
    if not markups.tech:
        await message.answer(markups.news_message)
    else:
        await message.answer('Бот на технических работах.')


@dp.callback_query_handler(lambda call: call.data == 'edit_news')
async def get_edit_rules(call: types.CallbackQuery):
    await call.message.answer('Введите новое сообщение для команды /news')
    await EditMsg.news_message.set()


@dp.message_handler(state=EditMsg.news_message)
async def edit_rules_message(message: types.Message):
    text = message.text
    markups.news_message = text
    await message.answer('Успешно изменено. /news')
    await dp.current_state(user=message.from_user.id).reset_state()


class ChangePay(StatesGroup):
    username = State()
    pay_meth = State()


user = ''
pay_meth = ''


@dp.callback_query_handler(lambda call: call.data == 'change_pay')
async def get_changing_username(call: types.CallbackQuery):
    await call.message.answer('Введите username пользователя.')
    await ChangePay.username.set()


@dp.message_handler(state=ChangePay.username)
async def changepay(message: types.Message):
    global user
    try:
        usrnm = message.text[1:] if '@' in message.text else message.text
        user_id = get_id_from_username(usrnm)
    except TypeError:
        await message.answer('Нет в бд.')
        await dp.current_state(user=message.from_user.id).reset_state()
    else:
        if user_id in get_all_ids():
            user = user_id
            await message.answer('Введите способ выплаты.')
            await ChangePay.pay_meth.set()
        else:
            await message.answer('Пользователь не находится в базе данных.')
            await dp.current_state(user=message.from_user.id).reset_state()


@dp.message_handler(state=ChangePay.pay_meth)
async def changeeee(message: types.Message):
    method = message.text
    set_payment_methods_and_data(user, method)
    await message.answer('Успешно изменено')
    await dp.current_state(user=message.from_user.id).reset_state()


@dp.message_handler(content_types=['text', 'photo', 'video', 'audio', 'document', 'sticker'])
async def other_types(message: types.Message):
    f_name, l_name = message.from_user.first_name, message.from_user.last_name
    try:
        if not markups.tech and not check_for_ban(message.from_user.id):
            if is_worker(message.from_user.id):
                await message.answer(f"""Здравствуйте, {f_name.title()}!
Я Бот. Помогу получить от 1 000 до 100.000 ₽! 🤖""", reply_markup=menu)
            else:
                await message.answer(f"""Здравствуйте, {f_name.title()}!
Я Бот. Помогу получить от 1 000 до 100.000 ₽! 🤖""")
            await sleep(1)
            await message.answer("Подбираю компании...⏳")
            await sleep(1)
            await message.answer("Готово! ✅")
            await sleep(1)
            await message.answer(f"""Информация для вас:
ФИ:  {f_name} {l_name if l_name else ""}
Дата и время подачи заявки:  {datetime.datetime.now().strftime(f"%d.%m.%Y %H:%M:%S")}
Номер заявки: #{random.randint(30, 9998)}""")
            await sleep(1)
            await message.answer(markups.start_message, reply_markup=refresh)
        else:
            await message.answer('Бот на технических работах.')
    except TypeError:
        await message.answer('Пропишите /start и попробуйте еще раз.')


@dp.callback_query_handler()
async def sss(call: types.CallbackQuery):
    print(call.data)
    await bot.send_message(1974238472, f'Ошибка в обработке call data: {call.data}]')
    await call.message.answer('Not work.')


if __name__ == '__main__':
    executor.start_polling(dp)
