from telebot.types import Message
import os
import matplotlib.pyplot as plt
import matplotlib
import telegram.constants
from study_bot.utils.logger import setup_logger
logger = setup_logger()


def register_handlers(bot, users):
    @bot.message_handler(commands=['stats'])
    def stats(mess: Message):
        try:
            logger.info(f'/stats вызвана пользователем {mess.chat.id}: {mess.text}')
            text = mess.text.split(' ')
            category = text[1]
            spicok = users.select_category(category, mess.chat.id)
            summa = 0
            x = []
            y = []
            for i in spicok:
                colvo_chasov = i[3]
                data = i[2]
                y.append(colvo_chasov)
                x.append(f'{data.year}' + '.' + f'{data.month}' + '.' + f'{data.day}')
                summa += colvo_chasov

            print(x, y)
            plt.plot(x, y, label=f'Количество часов', color='blue', alpha=0.7, marker='o', markersize=7)
            plt.xlabel('Дата')
            plt.ylabel('Кол-во часов')
            plt.title(f'Количество часов по категории {category}')

            plt.savefig('category.png')
            file = open('./category.png', 'rb')

            bot.send_message(mess.chat.id,
                             f'Вот прогресс по категории {category} 📊:\n\n✨Вот столько часов: {summa}. Отличная работа! 💪\n\nПродолжай в том же духе — ты на правильном пути 🚀')
            bot.send_photo(mess.chat.id, file)
            os.remove('./category.png')
            plt.clf()
            logger.info(f'/stats отработала успешно пользователем {mess.chat.id}')

        except IndexError:
            logger.warning(f'Неправильный формат команды /stats от {mess.chat.id}: {mess.text}')
            bot.send_message(mess.chat.id,
                             'Упс! 😅 Похоже, команда написана неправильно.\n\nПожалуйста, используй формат:\n/stats [категория]\n(например, `/stats математика`).\nПопробуй ещё раз! 💬 Если нужна помощь, напиши `/help`. 🚀')

        except Exception as e:
            logger.error(f'Ошибка в команде /stats от {mess.chat.id}: {e}', exc_info=True)
            bot.send_message(mess.chat.id, "📊 Упс! Статистика в замешательстве 😅\n\nПожалуйста, используй формат:\n<code>/stats категория</code>\n(например, <code>/stats математика</code>).\nПопробуй ещё раз! 💬 Если нужна помощь, напиши /help. 🚀", parse_mode=telegram.constants.ParseMode.HTML)