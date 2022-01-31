from .local_settings import TB_TOKEN
from aiogram import Bot, Dispatcher


bot = Bot(token=TB_TOKEN)
dp = Dispatcher(bot)
