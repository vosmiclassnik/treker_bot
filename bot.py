import telebot
import matplotlib
from study_bot.database.prokladka_db import database, rassilka, achieve, goals
from utils import achievements
from config import api
from handlers import add, start, stats, profile, remind, admin, goal, proverka
from study_bot.utils import logger
logger = logger.setup_logger()

bot = telebot.TeleBot(api)
matplotlib.use('agg')

#базы данных
rassilka = rassilka('rassilka') 
users = database('users')
achieve = achieve('achieve')
goals = goals('goals')
users.create_db()
rassilka.create_db()
achieve.create_db()
goals.create_db()



#проверка на текст
proverka.register_handlers(bot)
#старт бота знакомство пользователя с функционалом
start.register_handlers(bot, users, rassilka, achieve, goals)
#базовый функционал
add.register_handlers(bot, users, achieve)
#статистика
stats.register_handlers(bot, users)
#личный профиль
profile.register_handlers(bot, users, achieve, goals, rassilka)
#рассылка напоминаний
remind.register_handlers(bot, users, rassilka)
#достижения
achievements.register_handlers(bot, achieve)
#goal
goal.register_handlers(bot, goals)
#adminskie
admin.register_handlers(bot, users, achieve)











bot.infinity_polling()
