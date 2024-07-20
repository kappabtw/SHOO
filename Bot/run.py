from Bot.ini import dp, bot
from Bot.handlers import start

async def run():
	
	await bot.delete_webhook(drop_pending_updates=True)
	dp.include_routers(start.router)