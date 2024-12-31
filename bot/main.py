import database
import asyncio
import config

from aiogram import Bot, Dispatcher

from handlers import admin_handlers, other_handlers, meeting_handlers

async def update_routes(dp: Dispatcher):

    dp.include_router(meeting_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    await database.initialize()

    await update_routes(dp)

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")