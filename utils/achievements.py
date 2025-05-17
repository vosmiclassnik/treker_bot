import datetime
import telegram
from telebot.types import Message
from study_bot.utils.logger import setup_logger
logger = setup_logger()

achievements = {
    "first_step": "Ты сделал(а) первую запись учёбы. Начало положено! 📌 Выдаётся при первом /add.",
    "full_day": "Учился(ась) 6 часов за сутки. Почти марафон! 📌 Когда за день суммарно записано ≥ 6 часов.",
    "master_categories": "Использовано 5 разных категорий. Учёба — это разнообразие! 📌 После добавления 5 уникальных категорий.",
    "night_academic": "Учился(ась) после полуночи. Настоящий ночной воин науки. 📌 При /add между 00:00–04:00.",
    "iron_habit": "30 дней хотя бы с 1 часом учёбы. Это уже система! 📌 Есть ≥ 30 дней с занятиями.",
    "absolute": "Суммарно проведено 100 часов за учёбой. Легендарный уровень! 📌 Общее количество часов ≥ 100.",
    "monday_achievement": "Записал(а) учёбу в понедельник. Начинаешь неделю с правильного шага! 📌 /add в понедельник.",
    "first_true_goal": "Первая выполненная цель. Поздравляем! 📌 Выполнить поставленную цель .",
    "hero_return": "Сделал(а) запись после 7+ дней перерыва. Главное — снова начать! 📌 Когда между записями был перерыв более недели.",
    "max_day": "Записал(а) 4+ занятия в один день. Настоящая серия! 📌 Когда в календарном дне ≥ 4 вызова /add."
}

list_of_achievements = list(achievements.keys())
list_of_descriptions = list(achievements.values())



def register_handlers(bot, achieve):
    @bot.message_handler(commands=['achieve'])
    def achievements_vivod(mess: Message):
        # твои достижения
        try:
            textik = "🎖 <b>Твои достижения:</b>\n\nПоздравляем! Вот твои учебные подвиги 📚🚀\n\n"
            spicok = achieve.all_achieve(mess.chat.id)
            if not spicok:
                bot.send_message(mess.chat.id,
                                 " 🏆<b>Твои достижения:</b>🏆\n\nПока нет ни одного достижения 😔\nНо всё впереди! Начни с команды <code>/add</code>, и первые награды не заставят себя ждать 🎖",
                                 parse_mode=telegram.constants.ParseMode.HTML)
            else:
                for i in spicok:

                    norm_name = ''
                    if i[2] == 'first_step':
                        norm_name = 'Первый шаг🥇'
                    elif i[2] == 'full_day':
                        norm_name = 'Полный день⏳'
                    elif i[2] == 'master_categories':
                        norm_name = 'Мастер категорий'
                    elif i[2] == 'night_academic':
                        norm_name = 'Ночной академик🧙🌙‍️'
                    elif i[2] == 'iron_habit':
                        norm_name = 'Железная привычка⏰'
                    elif i[2] == 'absolute':
                        norm_name = 'Абсолют!🔥'
                    elif i[2] == 'monday_achievement':
                        norm_name = 'Понедельник - день тяжелый🗓'
                    elif i[2] == 'first_true_goal':
                        norm_name = 'Первый выполненная цель!🎯'
                    elif i[2] == 'hero_return':
                        norm_name = 'Возвращение героя🦸‍'
                    elif i[2] == 'max_day':
                        norm_name = 'Катка на максимум😮‍💨'

                    textik += (
                        f"✅ <b>{norm_name}</b>\n"
                        f"<i>{i[4]}</i>\n"
                        f"📅 Получено: {i[5]}\n\n"
                    )
                bot.send_message(mess.chat.id, textik, parse_mode=telegram.constants.ParseMode.HTML)
        except Exception as e:
            logger.error(f'Что-то пошло не так, при отображении достижений пользователя {mess.chat.id}: {e}', exc_info=True)

def nachalo(mess: Message, achieve):
    for i in range(10):
        achieve.set_achieve(mess.chat.id, list_of_achievements[i],desc=list_of_descriptions[i], active=False)
    logger.info(f'Установленые первые достижения пользователя {mess.chat.id}')


def check_first_step(bot, mess: Message, achieve, users):
    try:
        norm_name = "Первый шаг🥇"
        total_bet = users.check_zapisi(mess.chat.id)
        if total_bet == 1 and not achieve.check_achieve(mess.chat.id, 'first_step'):
            achieve.change_status(mess.chat.id, 'first_step', date=datetime.datetime.today())
            logger.info(f'Пользователь {mess.chat.id} разблокировал достижение first_step')
            bot.send_message(mess.chat.id, f"🏆 Достижение разблокировано:\n\n{norm_name}\n<i>Просмотреть свои достижение - /achieve</i>", parse_mode=telegram.constants.ParseMode.HTML)
    except Exception as e:
        logger.error(f'Произошла ошибка в проверке достижения first_step у пользователя {mess.chat.id}: {e}', exc_info=True)



def check_absolute(bot, mess: Message, achieve, summa):
    try:
        norm_name = "Абсолют!🔥"
        if int(summa) >= 100 and not achieve.check_achieve(mess.chat.id, 'absolute' ):

            achieve.change_status(mess.chat.id, 'absolute', datetime.datetime.today())
            logger.info(f'Пользователь {mess.chat.id} разблокировал достижение absolute')
            bot.send_message(mess.chat.id, f"🏆 Достижение разблокировано:\n\n{norm_name}\n<i>Просмотреть свои достижение - /achieve</i>", parse_mode=telegram.constants.ParseMode.HTML)
    except Exception as e:
        logger.error(f'Произошла ошибка в проверке достижения absolute у пользователя {mess.chat.id}: {e}', exc_info=True)


def check_monday(bot, mess: Message, achieve, weekday):
    try:
        norm_name = "Понедельник - день тяжелый🗓!"
        if weekday == 0 and not achieve.check_achieve(mess.chat.id, 'monday_achievement'):

            achieve.change_status(mess.chat.id, 'monday_achievement', datetime.datetime.today())
            logger.info(f'Пользователь {mess.chat.id} разблокировал достижение monday_achievement')
            bot.send_message(mess.chat.id, f"🏆 Достижение разблокировано:\n\n{norm_name}\n<i>Просмотреть свои достижение - /achieve</i>", parse_mode=telegram.constants.ParseMode.HTML)
    except Exception as e:
        logger.error(f'Произошла ошибка в проверке достижения monday_achievement у пользователя {mess.chat.id}: {e}', exc_info=True)

def check_first_goal(bot, mess: Message, achieve, status):
    try:
        norm_name = 'Первый выполненная цель!🎯'
        if status == '✅':
            achieve.change_status(mess.chat.id, 'first_true_goal', datetime.datetime.today())
            logger.info(f'Пользователь {mess.chat.id} разблокировал достижение first_true_goal')
            bot.send_message(mess.chat.id, f"🏆 Достижение разблокировано:\n\n{norm_name}\n<i>Просмотреть свои достижение - /achieve</i>", parse_mode=telegram.constants.ParseMode.HTML)
    except Exception as e:
        logger.error(f'Произошла ошибка в проверке достижения first_true_goal у пользователя {mess.chat.id}: {e}', exc_info=True)
