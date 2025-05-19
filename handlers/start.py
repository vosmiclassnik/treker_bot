from telebot.types import Message
import telegram.constants
from utils.logger import setup_logger
from utils.achievements import nachalo
logger = setup_logger()
def register_handlers(bot, users, rassilka, achieve, goals):
    @bot.message_handler(commands=['start'])
    def start(mess: Message):
        nachalo(mess, achieve)
        logger.info(f'/start вызвана от пользователя {mess.chat.id}')
        text = (
            "Привет! 👋 Я — твой учебный бот-трекер. Помогаю отслеживать, сколько времени ты посвящаешь учёбе каждый день 📚💪\n\n"
            "Чтобы добавить сегодняшние часы, просто введи команду:\n"
            "<code>/add n категория</code>\n"
            "где <b>n</b> — это количество часов, а <b>категория</b> — предмет или тип занятия.\n"
            "Например: <code>/add 2 математика</code>\n\n"
                        "Вот что я умею:\n"
            "➕ <code>/add n категория</code> — Добавить часы\n"
            "📊 <code>/stats категория</code> — График по категории\n"
            "🎯 <code>/goal категория часы дата</code> — Установить цель (например: <code>/goal математика 20 01-06-2025</code>)\n"
            "⏰ <code>/setremind ЧЧ:ММ</code> — Установить напоминание\n"
            "👤 /profile — Твой личный профиль\n"
            "🚫 /unsetremind — Удалить напоминания\n"
            '🏆/achieve - Список достижений\n'
            "ℹ️ /help — Помощь\n\n"
            "Успехов в учёбе! 🌟"
        )

        bot.send_message(mess.chat.id, text, parse_mode=telegram.constants.ParseMode.HTML)

        # Проверка БД
        achieve.test_otput()




    @bot.message_handler(commands=['help'])
    def help_command(mess: Message):
        logger.info(f'/help вызвана от пользователя {mess.chat.id}')
        help_text = (
            "ℹ️ Вот список команд, которые ты можешь использовать:\n\n"
            "➕ <b>/add</b> n категория — Добавить часы учёбы (например: <code>/add 2 физика</code>)\n"
            "📊 <b>/stats</b> категория — Показать статистику по одной категории\n"
            "👤 <b>/profile</b> — Показать личный профиль со всеми категориями\n"
            "⏰ <b>/setremind</b> ЧЧ:ММ — Установить напоминание\n"
            "🎯 <b>/goal категория часы дата</b> — Установить цель (например: <code>/goal математика 20 01-06-2025</code>)\n"
            "🚫 <b>/unsetremind</b> — Удалить все напоминания\n"
            "🏆 <b>/achieve</b> — Список достижений достижения!\n\n"
            "Если что-то непонятно — просто напиши ещё раз /help 🙂"
        )
        bot.send_message(mess.chat.id, help_text, parse_mode=telegram.constants.ParseMode.HTML)