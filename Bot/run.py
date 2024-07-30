
from aiogram.fsm.state import State, StatesGroup
from Bot.ini import dp, bot
from Bot.handlers import start, catalog, admin

async def run():
	
	await bot.delete_webhook(drop_pending_updates=True)
	dp.include_routers(start.router, catalog.router, admin.router)