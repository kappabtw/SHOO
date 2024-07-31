# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.filters import Command
from Bot.Keyboards import startKeyboard, backToMenuKeyboard
from asql import ASQL
from Bot import data

router = Router()

@router.message(Command("start"))
async def cmd_start(msg: types.Message):
    
    await msg.answer_photo(photo = data.time_photo, caption = data.Message['upper_menu'], reply_markup=startKeyboard.keyboard)
    await ASQL.execute(f"INSERT OR IGNORE INTO Пользователи (id, name, username) VALUES (?,?,?)",(msg.from_user.id,msg.from_user.first_name,f'@{msg.from_user.username}'))

@router.callback_query(lambda callback: callback.data == data.Callback['info'])
async def info_callback(callback: types.CallbackQuery):
    await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo,caption = data.Message['upper_info']),
                                      reply_markup = backToMenuKeyboard.keyboard)
    
@router.callback_query(lambda callback: callback.data == data.Callback['reviews'])
async def callback_to_reviews(callback: types.CallbackQuery):
    
    await callback.answer()
    
@router.callback_query(lambda callback: callback.data == data.Callback['manager'])
async def callback_to_manager(callback:types.CallbackQuery):
    
    await callback.answer()
    
@router.callback_query(lambda callback: callback.data == data.Callback['menu'])
async def callback_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo,caption = data.Message['upper_menu']),
                                      reply_markup=startKeyboard.keyboard)

    

    

    
    