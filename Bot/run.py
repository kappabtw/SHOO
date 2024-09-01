
#from aiogram.fsm.state import State, StatesGroup
from Bot.ini import dp, bot
from Bot.handlers import start, catalog, models, admin
from Bot.handlers.order import closed_order, new_order, other_order, processed_order
from Bot.handlers.order.admin_panel import panel, redactModels

async def run():
	
	await bot.delete_webhook(drop_pending_updates=True)
	dp.include_routers(start.router, catalog.router, models.router, admin.router, closed_order.router, new_order.router, other_order.router, processed_order.router)
	dp.include_routers(panel.router, redactModels.router)