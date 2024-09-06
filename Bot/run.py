
#from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Bot.ini import dp, bot
from Bot.handlers import start, catalog, models, admin
from Bot.handlers.order import closed_order, new_order, other_order, processed_order
from Bot.handlers.order.admin_panel import panel, redact_showmodels, redact_commands

async def run():
	
	await bot.delete_webhook(drop_pending_updates=True)
	dp.include_routers(start.router, catalog.router, models.router, admin.router, closed_order.router, new_order.router, other_order.router, processed_order.router)
	dp.include_routers(panel.router , redact_showmodels.router, redact_commands.router)