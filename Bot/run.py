
#from aiogram.fsm.state import State, StatesGroup
from Bot.ini import dp, bot
from Bot.handlers import start, catalog, models, admin, order

async def run():
	
	await bot.delete_webhook(drop_pending_updates=True)
	dp.include_routers(start.router, catalog.router, models.router, admin.router, order.router)