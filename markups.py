from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton(text='Профиль'), KeyboardButton(text='Счета'))

admin_menu = InlineKeyboardMarkup(row_width=2)
admin_menu.add(
    InlineKeyboardButton(text='Пользователи', callback_data='count users'),
    InlineKeyboardButton(text='Данные пользователя', callback_data='get_pay_meth'),
    InlineKeyboardButton(text='Моя реферальная ссылка', callback_data='get_ref_url'),
    InlineKeyboardButton(text='Изменить баланс', callback_data='set_bank'),
    InlineKeyboardButton(text='Забанить пользователя', callback_data='ban'),
    InlineKeyboardButton(text='Отправить личное сообщение', callback_data='send pm'),
    InlineKeyboardButton(text='Добавить воркпанель', callback_data='add work'),
    InlineKeyboardButton(text='Изъять воркпанель', callback_data='del work'),
    InlineKeyboardButton(text='Рассылка по воркерам', callback_data='mailing'),
    InlineKeyboardButton(text='Рассылка всем', callback_data='all_mailing'),
    InlineKeyboardButton(text='Изменить стартовое сообщение', callback_data='edit_start_message'),
    InlineKeyboardButton(text='Изменить новости', callback_data='edit_news'),
    InlineKeyboardButton(text='Изменить правила', callback_data='edit_rules'),
    InlineKeyboardButton(text='Включить тех.работы', callback_data='on'),
    InlineKeyboardButton(text='Выключить тех.работы', callback_data='off'),
    InlineKeyboardButton(text='Изменить способ выплаты', callback_data='change_pay')
)


refresh = InlineKeyboardMarkup()
refresh.row(InlineKeyboardButton(text='Перезапустить бота', callback_data='refresh'))

back = InlineKeyboardMarkup()
back.row(InlineKeyboardButton(text='Вернуться назад', callback_data='refresh'))

payment_methods = InlineKeyboardMarkup(row_width=1)
payment_methods.row(InlineKeyboardButton(text='Способы выплат', callback_data='payment_methods'))

chose_p_m = InlineKeyboardMarkup(row_width=1)
chose_p_m.add(
    InlineKeyboardButton(text='Qiwi', callback_data='chose_qiwi'),
    InlineKeyboardButton(text='WebMoney', callback_data='chose_web'),
    InlineKeyboardButton(text='Перевод на карту', callback_data='chose_card')
)

change_paymeth = InlineKeyboardMarkup()
change_paymeth.row(InlineKeyboardButton(text='Изменить способ выплаты.', callback_data='chose_meth'))

start_message = """♻ 1. Перейдите по ссылке
📝 2. Заполните анкету
💳 3. Деньги придут через 3 минуты
👇🏻👇🏻👇🏻

⚡Moneyman👉 https://finlg.ru/SHHON 

💸ТУРБОЗАЙМ 👉 https://finlg.ru/SHHOO

💸Займер 👉 https://finlg.ru/SHHOQ

💸ДоЗарплаты👉 https://finlg.ru/SHHOP

⚠ Заполните несколько анкет для 100% одобрения!
Created by @prog_heroku"""

rules_message = 'Здесь пока пусто. Если вы администратор, измените через панель администратора.'
news_message = 'Здесь пока пусто. Если вы администратор, измените через панель администратора.'

tech = False
