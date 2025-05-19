from config import id
from telebot.types import Message
from utils.logger import setup_logger
logger = setup_logger()
def send_logs(bot, log_file='./logs/bot.log'):
    try:
        with open(log_file, 'rb') as f:
            bot.send_document(id, f, caption="📄 Логи бота")
    except Exception as e:
        logger.error(f"Ошибка при отправке логов: {e}", exc_info=True)
def send_message(bot, ids, text):
    for uid in ids:
        try:
            bot.send_message(uid, text)
        except Exception as e:
            logger.warning(f"❌ Не удалось отправить сообщение пользователю {uid}: {e}")
def register_handlers(bot, users, achieve):
    @bot.message_handler(commands=['backup'])
    def backup(mess: Message):
        if int(mess.chat.id) == int(id):
            users.backup_users(bot, id)
            achieve.backup_achieve(bot, id)
            logger.info(f'Успешно произошел backup')
        else:
            bot.send_message(mess.chat.id, "❌ Только админы могут делать бэкап.")
            logger.warning(f"Пользователь {mess.chat.id} попытался сделать бэкап")




    @bot.message_handler(commands=['broadcast'])
    def broadcast(mess: Message):
        if int(mess.chat.id) == int(id):
            try:
                xyinya = mess.text.split('$')
                text = xyinya[1]
                spicok = users.test_output()
                ids = []
                for i in spicok:
                    ids.append(i[1])

                all_ids = set(ids)
                bot.send_message(bot, all_ids, text)
                logger.info(f'Рассылка с текстом {text} пришла успешно')
            except Exception as e:
                bot.send_message(mess.chat.id,'что то пошло не так')
                logger.error(f'Рассылку отправить не удалось: {e}', exc_info=True)
        else:
            bot.send_message(mess.chat.id, "❌ Только админы могут делать рассылку.")
            logger.warning(f"Пользователь {mess.chat.id} попытался сделать рассылку")



    @bot.message_handler(commands=['log'])
    def logs(mess: Message):
        if int(mess.chat.id) == int(id):
            send_logs(bot)
            logger.info(f'Логи успешно отправлены')
        else:
            bot.send_message(mess.chat.id, "❌ У вас нет доступа к логам.")
            logger.warning(f"Пользователь {mess.chat.id} попытался сделать рассылку логов")
