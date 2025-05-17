import telebot.types
import telegram.constants
from telebot.types import Message
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from study_bot.utils.logger import setup_logger
from study_bot.utils.achievements import achievements, check_absolute, check_first_goal
from study_bot.utils.streak import calculate_streak

logger = setup_logger()


def register_handlers(bot, users, achieve, goals, rassilka):
    @bot.message_handler(commands=['profile'])
    def profile(mess: Message):
        try:
            #удаление профиля
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('🗑Удалить профиль', callback_data='delete'))









            logger.info(f'/profile вызвана пользователем {mess.chat.id}')
            # получаем данные
            dannye = defaultdict(int)
            vse_zapisi = users.statistica_polsovatelya(mess.chat.id)

            spicok_category = []
            summa = 0
            for i in vse_zapisi:
                category = i[4]
                colvo_chasov = i[3]
                dannye[category] += colvo_chasov
                summa += colvo_chasov
                spicok_category.append(category)
            true_category = list(set(spicok_category))

            check_absolute(bot, mess, achieve, summa)
            # дата
            dates = [z[2] for z in vse_zapisi]
            last_activity = max(dates) if dates else None

            # streak

            zapisi = users.statistica_polsovatelya(mess.chat.id)
            dati = []
            for i in zapisi:
                dati.append(i[2])
            streak = calculate_streak(dati)







            # техт
            flag = ''
            if last_activity:
                logger.info(f'/profile сработала верно, вызвана пользователем {mess.chat.id}')
                text = f" 📊 Вот как ты прокачиваешь себя:\n📅Последняя активность: {last_activity.strftime('%d.%m.%Y')}\n"
                if streak == 0:
                    text += "Пора возвращаться в ритм! Сегодня отличный день, чтобы начать новый стрик 🚀\n\n"
                elif streak == 1:
                    text += "Ого, начало положено! Первый день в копилке 🎯\n\n"
                elif streak < 5:
                    text += f"Уже {streak} дня подряд учёбы! Хороший старт 🔥\n\n"
                elif streak < 10:
                    text += f"{streak} дней подряд — ты в отличной форме! 📈\n\n"
                else:
                    text += f"{streak} дней без перерывов! Ты машина! 🤖📚 Не останавливайся!\n\n"
                for category, hours in dannye.items():
                    text += f"📚 {category} — {hours} ч\n"
                text += f"\n📈 Всего учёбы: {summa} ч\n"
                # цели
                tseli = goals.select_goals(mess.chat.id)

                if not tseli:
                    text += "\n🎯 У тебя пока нет установленных целей.\n<code>/goal категория часы дата</code> — Установить цель\n"
                else:
                    text += "\n🎯 <b>Цели:</b>\n"

                    for i in tseli:
                        try:
                            done = dannye[f'{i.category}']
                            percent = min(100, round(done / i.target * 100)) if i.target else 0
                            status = "✅" if percent >= 100 else "📈"
                            text += (
                                f"{status} {i.category} — {done}/{i.target} ч. "
                                f"({percent}%) до {i.deadline.strftime('%d.%m.%Y')}\n"
                            )
                            if status == '✅':
                                goals.delete_deadline(mess.chat.id, i.category)
                                check_first_goal(bot, mess, achieve, status)
                        except Exception as e:
                            logger.error(f'Произошла ошибка в отображении целей пользователя {mess.chat.id}: {e}')
                            text += f"\n❌ Пока нет ни одной записи по категории {i.category}.\n➕ <code>/add n [категория]</code> — Добавить часы\n\n"



                text += '\n🔥 Так держать! Не останавливайся 💪'
            else:
                logger.info('/profile сработала верно, у пользователя {mess.chat.id} нет записей')
                text = "\n❌ Пока нет ни одной записи.\n➕ <code>/add n [категория]</code> — Добавить часы"
                flag = True

            # график
            values = list(dannye.values())
            labels = list(dannye.keys())

            plt.pie(values, labels=labels, autopct='%1.1f%%', radius=0.9)
            plt.title(f'Учебный профиль @{mess.from_user.username}')

            plt.savefig('allcategories.png')
            file = open('./allcategories.png', 'rb')
            if flag:
                bot.send_message(mess.chat.id, text, reply_markup=markup, parse_mode=telegram.constants.ParseMode.HTML, )
            else:
                bot.send_photo(mess.chat.id, file)
                bot.send_message(mess.chat.id, text, reply_markup=markup, parse_mode=telegram.constants.ParseMode.HTML )
                os.remove('./allcategories.png')
                plt.clf()





        except Exception as e:
            logger.error(f'В команде профиль произошла ошибка пользователя {mess.chat.id}: {e}', exc_info=True)
            bot.send_message(mess.chat.id,'Попробуйте заново, что-то пошло не так')




    @bot.callback_query_handler(func=lambda call: True)
    def c(call):
        if call.data == 'delete':
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(telebot.types.KeyboardButton("✅ Да, удалить"), telebot.types.KeyboardButton("❌ Отмена"))

            bot.send_message(call.message.chat.id, "Ты точно хочешь удалить профиль? 🗑️", reply_markup=markup)

    @bot.message_handler(func=lambda msg: msg.text in ["✅ Да, удалить", "❌ Отмена"])
    def handle_delete_response(message):
        if message.text == "✅ Да, удалить":
            users.delete_user_users(message.chat.id)
            achieve.delete_user_achieve(message.chat.id)
            goals.delete_user_goals(message.chat.id)
            rassilka.delete_user_rassilka(message.chat.id)
            bot.send_message(
                message.chat.id,
                "🗑️ Профиль успешно удалён.\nОбязательно напиши /start для начала работы с ботом.",
                reply_markup=telebot.types.ReplyKeyboardRemove()
            )
            logger.info(f'Пользователь {message.chat.id} удалил свой профиль')
        else:
            bot.send_message(
                message.chat.id,
                "❌ Удаление отменено./start или /help для другого взаимодействия с ботом",
                reply_markup=telebot.types.ReplyKeyboardRemove()
            )
            logger.info(f'Пользователь {message.chat.id} отменил удаление профиля')
