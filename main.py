# -*- coding: windows-1251 -*-
import asyncio
import logging
import aiocache
from Bot.ini import *
from Bot.run import run
from asql import ASQL

logging.basicConfig(level=logging.INFO)

async def main():
    await run()    
    await dp.start_polling(bot)


if __name__ ==  "__main__":
    asyncio.get_event_loop().run_until_complete(main())