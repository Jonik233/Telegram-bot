from config import Config
from aiogram import Bot, Dispatcher, executor

bot = Bot(Config.bot_token)
dp = Dispatcher(bot)                                                                                                                                              

async def shutdown(dp):
    await bot.close()

if __name__ == '__main__':
    from handlers.handlers import dp
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)