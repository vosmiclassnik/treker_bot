from telebot.types import Message
from utils.logger import setup_logger
logger = setup_logger()



def register_handlers(bot):
    @bot.message_handler(func=lambda message: not message.text.startswith('/') and message.text not in ["✅ Да, удалить", "❌ Отмена"])
    def handle_text(mess: Message):
        bot.send_message(mess.chat.id, "🤖 Упс! Я пока не умею читать мысли...\n\nПопробуй написать /start или /help — и посмотрим, что из этого выйдет 😉")
        logger.warning(f'Написан текст вместо команды {mess.text}, пользователем {mess.chat.id}')