import telegram.constants
from telebot.types import Message
import datetime
from study_bot.utils.logger import setup_logger
from study_bot.utils.achievements import check_first_step, check_monday
logger = setup_logger()
def register_handlers(bot, users, achieve):
    @bot.message_handler(commands=['add'])
    def add(mess: Message):
        try:
            logger.info(f"/add вызвана пользователем {mess.chat.id} с текстом: {mess.text}")
            date = datetime.date.today()
            text = mess.text.split(' ')

            colvo_chasov = text[1].lower()
            if int(colvo_chasov) <= 12:
                category = text[2].lower()
                if str.isdigit(category):
                    raise Exception
                users.add_chasi(date, colvo_chasov, mess.chat.id, category)
                logger.info(f"Добавлены часы: {colvo_chasov} | Категория: {category} | ID: {mess.chat.id}")
                bot.send_message(mess.chat.id,
                    f'Часы учёбы успешно добавлены! ✅\n\nОтличная работа! 💪 Ты записал вот столько часов: {colvo_chasov}, по категории {category}. Продолжай в том же духе! 🚀')
                check_first_step(bot, mess, achieve, users)
                check_monday(bot, mess, achieve, date.weekday())
            else:
                text = (
                    "🛑 Эй-эй-эй! Ты указал больше 12 часов учёбы за день...\n"
                    "Это, конечно, впечатляет, но мы тут за здоровый подход! 💆‍️📚\n\n"
                    "Учёба дольше 12 часов в день не идёт в зачёт — ты же не робот (пока 😅).\n"
                    "Попробуй разбить нагрузку на несколько дней — мозг скажет тебе спасибо! 🧠💤"
                )
                bot.send_message(mess.chat.id, text)
                logger.warning(f"Пользователь {mess.chat.id} вписал больше 12 часов в команду /add")
        except IndexError:
                logger.warning(f"Неправильный формат команды /add от {mess.chat.id}: {mess.text}")
                bot.send_message(mess.chat.id,
                    'Упс! 😅 Похоже, команда написана неправильно.\n\nПожалуйста, используй формат:\n<code>/add n категория</code>\nгде n — это количество часов (например, <code>/add 2 математика</code>).\nПопробуй ещё раз! 💬 Если нужна помощь, напиши /help. 🚀', parse_mode=telegram.constants.ParseMode.HTML)
        except Exception as e:
                logger.error(f"Ошибка в команде /add от {mess.chat.id}: {e}", exc_info=True)
                bot.send_message(mess.chat.id,  "⏱️ Хм... Кажется, часы потерялись во времени 😅\n\nПожалуйста, используй формат:\n<code>/add n категория</code>\nгде n — это количество часов (например, <code>/add 2 математика</code>).\nПопробуй ещё раз! 💬 Если нужна помощь, напиши /help. 🚀.", parse_mode=telegram.constants.ParseMode.HTML)
