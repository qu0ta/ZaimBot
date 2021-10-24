import sqlite3


def create_table():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INT,
        name VARCHAR(50),
        tg_username VARCHAR(50),
        referrer INT,
        balance INT,
        is_banned BOOLEAN,
        is_worker BOOLEAN,
        payment_method VARCHAR(50),
        payment_data VARCHAR(50)
        )""")
        db.commit()


def add_user(user_id, name, username, referrer=0, balance=0, is_banned='False',
             is_worker=False, payment_method=None, payment_data=None):
    values = (user_id, name, username, referrer, balance, is_banned, is_worker, payment_method, payment_data)
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
            db.commit()
            return False
        return True


def get_count_users():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        return len(cursor.execute("SELECT user_id FROM users").fetchall())


def get_all_users():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        return tuple(map(lambda x: x[0], cursor.execute("SELECT tg_username FROM users").fetchall()))


def has_referrer(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        referrer = cursor.execute(f"SELECT referrer FROM users WHERE user_id = {user_id}").fetchone()[0]
        if referrer:
            return True
        return False


def add_referrer(user_id, referrer):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET referrer = {referrer} WHERE user_id = {user_id}")
        db.commit()


def get_username_from_id(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        username = cursor.execute(f"SELECT tg_username FROM users WHERE user_id = {user_id}").fetchone()[0]
        return username


def get_id_from_username(username):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        user_id = cursor.execute(f"SELECT user_id FROM users WHERE tg_username = '{username}'").fetchone()[0]
        return user_id


def get_ref_count_by_id(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        count = list(filter(lambda x: x == user_id,
                            map(lambda x: x[0],
                                cursor.execute("SELECT referrer FROM users").fetchall())))
        return len(count)


def get_balance(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = {user_id}").fetchone()[0]
        return balance


def check_for_ban(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        is_banned = cursor.execute(f"SELECT is_banned FROM users WHERE user_id = {user_id}").fetchone()[0]
        if is_banned == 'True':
            return True
        return False


def ban_user_by_id(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET is_banned = 'True' WHERE user_id = {user_id}")
        db.commit()


def set_balance(user_id, amount):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET balance = {amount} WHERE user_id = {user_id}")
        db.commit()


def is_worker(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        is_worker = cursor.execute(f"SELECT is_worker FROM users WHERE user_id = {user_id}").fetchone()[0]
        if is_worker == 'True':
            return True
        return False


def add_worker(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET is_worker = 'True' WHERE user_id = {user_id}")
        db.commit()


def del_worker(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET is_worker = 'False' WHERE user_id = {user_id}")
        db.commit()


def is_chosen_pay_meth(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        meth = cursor.execute(f"SELECT payment_method FROM users WHERE user_id = {user_id}").fetchone()[0]
        if meth == 'True':
            return True
        return False


def set_payment_methods_and_data(user_id, data):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(f'UPDATE users SET payment_method = "True", payment_data = "{data}" WHERE user_id = {user_id}')
        db.commit()


def get_paymeths(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        data = cursor.execute(f"SELECT payment_data FROM users WHERE user_id = {user_id}").fetchone()[0]
        return data

def get_profile(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        res = cursor.execute(f"SELECT name FROM users WHERE user_id = {user_id}").fetchone()[0]
        return res


def get_all_ids():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        return list(map(lambda x: x[0], cursor.execute("SELECT user_id FROM users").fetchall()))