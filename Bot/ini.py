from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token="6471379376:AAGy8aNQfESqxQnYiFVmBgRgNnbpbsFzgzc")
dp = Dispatcher(storage= MemoryStorage());  
	