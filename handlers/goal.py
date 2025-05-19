import time
import threading

import telegram.constants
from telebot.types import Message
import datetime
from utils.logger import setup_logger
logger = setup_logger()


def register_handlers(bot, goals):
    @bot.message_handler(commands=['goal'])
    def set_goal(mess: Message):
        try:
            xyinya = mess.text.split()
            category = xyinya[1]
            target = xyinya[2]

            date = xyinya[3]
            deadline = datetime.datetime.strptime(date, '%d-%m-%Y').date()


            #проверка
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            if deadline < tomorrow:
                raise ValueError("Дедлайн должен быть не раньше завтрашнего дня!")

            goals.set_goal(mess.chat.id, category, target, deadline)
            text = f"🎯 Цель установлена: {target} ч. по {category} до {deadline}"
            if int(target) >= 250 and int(target) < 500:
                text += f'\nУх, {target} это многовато, но мы в тебя верим!🔥'
            elif int(target) > 500:
                raise ValueError('Значение больше 500')
            bot.send_message(mess.chat.id, text)
            logger.info(f'Пользователь {mess.chat.id} установил цель {target}ч по {category} до {deadline}')
        except ValueError as e:
            logger.warning(f'{mess.chat.id} сделал ошибку в установлении цели: {e}')
            bot.send_message(mess.chat.id, '🎯 Похоже, ты пытался установить цель… но для вселенной это слишком большая цель, давай меньше 500... Или ты решил сделать дедлайн прошедшей датой😅\n\nВот предполагаемый формат:\n<code>/goal категория часы дата</code>.\n<i>Попробуй еще раз!</i>', parse_mode=telegram.constants.ParseMode.HTML)
        except Exception as e:
            bot.send_message(mess.chat.id, "🎯 Похоже, ты пытался установить цель… но Вселенная не поняла тебя 😅\n\nВот предполагаемый формат:\n<code>/goal категория часы дата</code>.\n<i>Попробуй еще раз!</i>", parse_mode=telegram.constants.ParseMode.HTML)
            logger.error(f'Ошибка в установке цели у пользователя {mess.chat.id}: {e}')




    def send_deadlines():
        while True:
            now = datetime.date.today()
            spicok = goals.test_otput()
            for i in spicok:
                if str(i.deadline) == str(now):
                    try:

                        bot.send_message(i.user_telegram_id,  f"😕 К сожалению, цель по категории {i.category} не была достигнута.\nНо не сдавайся — ты можешь попробовать снова!")
                        goals.delete_deadline(i.user_telegram_id, i.category)
                        logger.info(f'Дедлайн отправлен пользователю {i.user_telegram_id}')

                    except Exception as e:
                        logger.error(f'Ошибка в отправке дедлайна от {i.user_telegram_id}: {e}', exc_info=True)
            time.sleep(86400)

    threading.Thread(target=send_deadlines, daemon=True).start()
