from aiogram import Router, types
from aiogram.filters import Command
from asql import ASQL

router = Router()

@router.callback_query(lambda callback: callback.data.startswith("model_adminpanel_"))
async def show_model(callback : types.CallbackQuery):
    pass
