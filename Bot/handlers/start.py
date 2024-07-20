# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from Bot.Keyboards import startKeyboard, backToMenuKeyboard

router = Router()

startMessage:str = "Старт"
infoMessage:str = "Информация о нас"
catalogMessage:str = "Наш каталог"



@router.message(Command("start"))
async def cmd_start(msg: types.Message):
    await msg.answer(text = startMessage, reply_markup=startKeyboard.keyboard)
    
@router.callback_query(lambda callback: callback.data == "catalog")
async def catalog_callback(callback: types.CallbackQuery):
    
    await callback.message.edit_text(text=catalogMessage)


@router.callback_query(lambda callback: callback.data == "info")
async def info_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(text = infoMessage, reply_markup = backToMenuKeyboard.keyboard)
    
@router.callback_query(lambda callback: callback.data == "reviews")
async def callback_to_reviews(callback: types.CallbackQuery):
    
    await callback.answer()
    
@router.callback_query(lambda callback: callback.data == "manager")
async def callback_to_manager(callback:types.CallbackQuery):
    
    await callback.answer()
    
@router.callback_query(lambda callback: callback.data == "back_to_menu")
async def callback_to_reviews(callback: types.CallbackQuery):
    await callback.message.edit_text(text = startMessage, reply_markup=startKeyboard.keyboard)
    

    

    
    