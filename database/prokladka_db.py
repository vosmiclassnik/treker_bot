import datetime

import sqlalchemy as db
from study_bot.utils.logger import setup_logger

logger = setup_logger()


# основная бд

class database:
    def __init__(self, databae):

        self.database = databae

    def create_db(self):
        global conn
        engine = db.create_engine(f'sqlite:///{self.database}.db')
        conn = engine.connect()
        meta = db.MetaData()
        self.database = db.Table('users', meta,
                                 db.Column('user_id', db.Integer, primary_key=True),
                                 db.Column('user_telegram_id', db.Integer),
                                 db.Column('date', db.Date),
                                 db.Column('colvo_chasov', db.Integer),
                                 db.Column('category', db.TEXT)
                                 )

        meta.create_all(engine)

    # добавляем часф
    def add_chasi(self, date, colvo_chasov, t_id, category):
        try:
            insert_query = self.database.insert().values([
                {'date': date, 'colvo_chasov': colvo_chasov, 'user_telegram_id': t_id, 'category': category}
            ])
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            logger.сritical(f'(add_chsi)В базе данных users произошла ошибка: {e}', exc_info=True)

    # выбираем часы пользователя за день

    def select_chasi(self, t_id, date):
        try:
            selectuem = db.select(self.database).where(
                db.and_(
                    self.database.columns.date == date,
                    self.database.columns.user_telegram_id == t_id
                )
            )

            zapros = conn.execute(selectuem)
            chasili = zapros.fetchall()
            return chasili[0][3]
        except Exception as e:
            logger.сritical(f'(select_chasi)В базе данных users произошла ошибка: {e}', exc_info=True)

    # выбираем записи по категории
    def select_category(self, category, t_id):
        try:
            selectuem = db.select(self.database).where(
                db.and_(
                    self.database.columns.category == category,
                    self.database.columns.user_telegram_id == t_id
                )
            )

            zapros = conn.execute(selectuem)
            categoryept = zapros.fetchall()
            return categoryept
        except Exception as e:
            logger.сritical(f'(select_category)В базе данных users произошла ошибка: {e}', exc_info=True)

    def check_zapisi(self, t_id):
        selectuem = db.select(self.database).where(self.database.columns.user_telegram_id == t_id)
        zapros = conn.execute(selectuem).scalar()
        return zapros
    def test_output(self):
        select = db.select(self.database)
        res = conn.execute(select)
        output = res.fetchall()
        print(output)
        return output

    def delete_user_users(self, t_id):
        del_q = db.delete(self.database).where(self.database.columns.user_telegram_id == t_id)
        conn.execute(del_q)
        conn.commit()

    def delete_all(self):
        del_q = db.delete(self.database)
        conn.execute(del_q)
        conn.commit()

    def statistica_polsovatelya(self, t_id):
        try:
            select = db.select(self.database).where(self.database.columns.user_telegram_id == t_id)
            res = conn.execute(select)
            output = res.fetchall()
            return output
        except Exception as e:
            logger.сritical(f'(statistica_polsovatelya)В базе данных users произошла ошибка: {e}', exc_info=True)

    #backup
    def backup_users(self, bot, chat_id):
        import shutil
        import datetime

        db_file = f"{self.database}.db"
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{self.database}_backup_{timestamp}.db"
        shutil.copy(db_file, backup_file)
        logger.info(f"Резервная копия базы создана: {backup_file}")

        # Отправляем файл через Telegram
        with open(backup_file, 'rb') as f:
            bot.send_document(chat_id, f, caption="Вот резервная копия базы данных.")

# бд для напоминаний

class rassilka:
    def __init__(self, name):
        self.rassilka = name

    def create_db(self):
        global cursor
        engine = db.create_engine(f'sqlite:///{self.rassilka}.db')
        cursor = engine.connect()
        meta = db.MetaData()
        self.rassilka = db.Table('rassilka', meta,
                                 db.Column('user_id', db.Integer, primary_key=True),
                                 db.Column('user_telegram_id', db.Integer),
                                 db.Column('time', db.Time, nullable=False),
                                 db.Column('active', db.Boolean, default=True)
                                 )

        meta.create_all(engine)

    def set_remind(self, t_id, time):
        try:
            insert_query = self.rassilka.insert().values([
                {'time': time, 'user_telegram_id': t_id}
            ])
            cursor.execute(insert_query)
            cursor.commit()
        except Exception as e:
            logger.сritical(f'(set_remind)В базе данных rassilka произошла ошибка: {e}', exc_info=True)

    def check_remind(self, t_id):
        try:
            check = db.select(self.rassilka).where(self.rassilka.columns.user_telegram_id == t_id)
            zapros = cursor.execute(check)
            if zapros.fetchall():
                return 1
            else:
                return 0
        except Exception as e:
            logger.сritical(f'(check_temind)В базе данных rassilka произошла ошибка: {e}', exc_info=True)

    def select_active(self):
        try:
            check = db.select(self.rassilka).where(
                self.rassilka.columns.active == True)
            zapros = cursor.execute(check)
            res = zapros.fetchall()
            return res
        except Exception as e:
            logger.сritical(f'(select_active)В базе данных rassilka произошла ошибка: {e}', exc_info=True)

    def test_otput(self):
        select = db.select(self.rassilka)
        res = cursor.execute(select)
        output = res.fetchall()
        print(output)
        return output

    def delete_user_rassilka(self, t_id):
        del_q = db.delete(self.rassilka).where(self.rassilka.columns.user_telegram_id == t_id)
        cursor.execute(del_q)
        cursor.commit()


# бд для достижений
class achieve:
    def __init__(self, name):
        self.achieve = name

    def create_db(self):
        global session
        engine = db.create_engine(f'sqlite:///{self.achieve}.db')
        session = engine.connect()
        meta = db.MetaData()
        self.achieve = db.Table('achieve', meta,
                                db.Column('user_id', db.Integer, primary_key=True),
                                db.Column('user_telegram_id', db.Integer),
                                db.Column('achieve_code', db.String),
                                db.Column('achieved', db.Boolean, default=False),
                                db.Column('description', db.String),
                                db.Column('date', db.Date)
                                )

        meta.create_all(engine)

    def check_achieve(self, t_id, code):
        try:
            check = db.select(self.achieve).where(
                db.and_(self.achieve.columns.user_telegram_id == t_id, self.achieve.columns.achieve_code == code, self.achieve.columns.achieved == True))
            zapros = session.execute(check)
            if zapros.fetchall():
                return 1
            else:
                return 0
        except Exception as e:
            logger.critical(f'(chechk_achieve)В базе данных achieve произошла ошибка: {e}', exc_info=True)

    def set_achieve(self, t_id, code,desc, active):
        try:
            check = db.select(self.achieve).where(
                db.and_(
                    self.achieve.columns.user_telegram_id == t_id,
                    self.achieve.columns.achieve_code == code)
            )

            zapros = session.execute(check)

            if not zapros.fetchall():
                new_achieve = self.achieve.insert().values([
                    {'date': datetime.datetime.today(), 'achieve_code': code, 'user_telegram_id': t_id,
                     'achieved': active, 'description': desc}
                ])
                session.execute(new_achieve)
                session.commit()
            else:
                pass
        except Exception as e:
            logger.error(f'(set_achieve)В базе данных achieve произошла ошибка: {e}', exc_info=True)


    def change_status(self, t_id, code, date):
        try:
            change = db.update(self.achieve).where(
                db.and_(
                    self.achieve.columns.user_telegram_id == t_id,
                    self.achieve.columns.achieve_code == code,
                    self.achieve.columns.achieved == False
                )
            ).values(achieved=True, date=date)
            session.execute(change)
            session.commit()
        except Exception as e:
            logger.error(f'(change_status)В базе данных achieve произошла ошибка: {e}')


    def all_achieve(self, t_id):
        selectuem = db.select(self.achieve).where(db.and_(self.achieve.columns.user_telegram_id == t_id, self.achieve.columns.achieved == True))
        zapros = session.execute(selectuem)
        return zapros.fetchall()

    def test_otput(self):
        select = db.select(self.achieve)
        res = session.execute(select)
        output = res.fetchall()
        return output
    #backup
    def backup_achieve(self, bot, chat_id):
        import shutil
        import datetime

        db_file = f"{self.achieve}.db"
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{self.achieve}_backup_{timestamp}.db"
        shutil.copy(db_file, backup_file)
        logger.info(f"Резервная копия базы создана: {backup_file}")

        # Отправляем файл через Telegram
        with open(backup_file, 'rb') as f:
            bot.send_document(chat_id, f, caption="Вот резервная копия базы данных.")
    def delete_user_achieve(self, id):
        del_q = db.delete(self.achieve).where(self.achieve.columns.user_telegram_id == id)
        session.execute(del_q)
        session.commit()







class goals:
    def __init__(self, name):
        self.goals = name

    def create_db(self):
        global penis
        engine = db.create_engine(f'sqlite:///{self.goals}.db')
        penis = engine.connect()
        meta = db.MetaData()
        self.goals = db.Table('goals', meta,
                                db.Column('user_id', db.Integer, primary_key=True),
                                db.Column('user_telegram_id', db.Integer),
                                db.Column('category', db.String),
                                db.Column('target', db.Integer, default=False),
                                db.Column('deadline', db.Date),
                                db.Column('date', db.Date, default=datetime.date.today())
                                )

        meta.create_all(engine)


    def set_goal(self, t_id, category, target, deadline):
        try:
            insert = db.insert(self.goals).values([
                {
                    'user_telegram_id': t_id, 'category': category, 'target': target, 'deadline': deadline
                }
            ]
            )
            penis.execute(insert)
            penis.commit()
            logger.info(f'Пользователь {t_id} установил цель')
        except Exception as e:
            logger.error(f'(set_goal) Произошла ошибка в goals: {e}', exc_info=True)
    def select_goals(self, t_id):
        select = db.select(self.goals).where(self.goals.columns.user_telegram_id == t_id)
        zapros = penis.execute(select)
        return zapros.fetchall()



    def select_goal(self, t_id, category):
        select = db.select(self.goals).where(db.and_(self.goals.columns.user_telegram_id == t_id, self.goals.columns.category == category))
        zapros = penis.execute(select)
        return zapros.fetchall()

    def test_otput(self):
        select = db.select(self.goals)
        res = penis.execute(select)
        output = res.fetchall()
        print(output)
        return output


    def delete_deadline(self, t_id, category):
        del_q = db.delete(self.goals).where(db.and_(self.goals.columns.user_telegram_id == t_id, self.goals.columns.category == category))
        penis.execute(del_q)
        penis.commit()



    def delete_user_goals(self, id):
        del_q = db.delete(self.goals).where(self.goals.columns.user_telegram_id == id)
        penis.execute(del_q)
        penis.commit()