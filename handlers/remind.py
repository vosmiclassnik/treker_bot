import telegram.constants
from telebot.types import Message
import datetime
import time
import threading
from utils.logger import setup_logger
logger = setup_logger()
def register_handlers(bot, users, rassilka):
    # напоминания
    #пенис
    @bot.message_handler(commands=['setremind'])
    def set_napominashky(mess: Message):
        print(1)
        try:
            logger.info(f'/setremind вызвана пользователем {mess.chat.id}')
            # беру время
            from datetime import time
            time_str = mess.text.split()[1]
            hour, minute = map(int, time_str.split(':'))

            #reminder_time = time(hour, minute)

            # проверяю есть ли другие рассылки
            #old = rassilka.check_remind(mess.chat.id)
            #if old:
                #rassilka.delete_user_rassilka(mess.chat.id)

            #rassilka.set_remind(mess.chat.id, reminder_time)
            #logger.info(f'/setremind сработала верно, у пользователя {mess.chat.id} установлено напоминание на {hour:02d}:{minute:02d}')
            #bot.send_message(mess.chat.id, f'✅ Напоминание установлено на {hour:02d}:{minute:02d}')
        except IndexError:
            logger.warning(f'Неправильно введена команда пользователем {mess.chat.id}: {mess.text}')
            bot.send_message(mess.chat.id, '❗ Используй формат: <code>/setremind ЧЧ:ММ</code> (например: <code>/setremind 18:30</code>)', parse_mode=telegram.constants.ParseMode.HTML)
        except Exception as e:
            logger.error(f"Ошибка в команде /setremind от {mess.chat.id}: {e}", exc_info=True)
            bot.send_message(mess.chat.id, '🔔 Я пытался установить напоминание… но запутался во времени и пространстве 😵‍💫\n\n❗ Используй формат: <code>/setremind ЧЧ:ММ</code> (например: <code>/setremind 18:30)</code>', parse_mode=telegram.constants.ParseMode.HTML)


    def send_reminders():
        # раз в минуту цикл
        while True:
            now = str(datetime.datetime.now().replace(second=0, microsecond=0)).split(' ')
            spicok = rassilka.select_active()

            for i in spicok:  # проходится по активным напоминашкам и сравнивает время
                if str(i.time) == now[1]:
                    try:
                        bot.send_message(i.user_telegram_id, "⏰ Пора учиться! Не забудь записать /add 😉")
                        logger.info(f'Напоминание отправлено пользователю {i.user_telegram_id}')
                    except Exception as e:
                        logger.error(f'Ошибка в отправке напоминание от {i.user_telegram_id}: {e}', exc_info=True)
                        print(f"Ошибка отправки: {e}")
            time.sleep(60)

    threading.Thread(target=send_reminders, daemon=True).start()

    # удаление напоминаний

    @bot.message_handler(commands=['unsetremind'])
    def un_set(mess: Message):
        logger.info(f'Пользователь {mess.chat.id} удалил все напоминания командой /unsetremind')
        rassilka.delete_user(mess.chat.id)
        bot.send_message(mess.chat.id,
                         '🗑 Все напоминания удалены!\n\nЕсли захочешь снова получать уведомления — просто используй команду /setremind. ⏰')
