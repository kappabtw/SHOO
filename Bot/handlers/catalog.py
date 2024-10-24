# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from Bot.Keyboards import catalogKeyboard
from Bot import data

router = Router()

CURRENT_MEDIA = data.photos["catalog"]

@router.message(Command("catalog"))
async def cmd_catalog(msg: types.Message):
    await msg.answer_photo(photo = CURRENT_MEDIA,caption = data.Message['brand']['def'], reply_markup = await catalogKeyboard.select_brands())
     
@router.callback_query(lambda callback: callback.data.startswith(data.Callback['brand']['def'])) #Выбрать модель бренда 
async def model_choice(callback: types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = CURRENT_MEDIA,caption = data.Message["model"]['def']),
                                                                    reply_markup=await catalogKeyboard.select_models(callback))    
    await callback.answer()
    
@router.callback_query(lambda callback: callback.data == data.Callback['sales']) #Выбрать бренд [Скидка]
async def callback_sales(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media=types.InputMediaPhoto(media = CURRENT_MEDIA,caption = data.Message['brand']['sales']),
                                      reply_markup= await catalogKeyboard.select_brands_with_sales())
    

@router.callback_query(lambda callback: callback.data == data.Callback['new_items']) #Выбрать бренд [Новинка]
async def callback_new_items(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = CURRENT_MEDIA,caption = data.Message['brand']['new']),
                                                                    reply_markup= await catalogKeyboard.select_brands_new_items())
    
@router.callback_query(lambda callback: callback.data.startswith(data.Callback['brand']['sales'])) #Выбрать модель бренда [Скидка]
async def model_sales_choice(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = CURRENT_MEDIA,caption = data.Message['model']['sales']),
                                                                    reply_markup=await catalogKeyboard.select_models_with_sales(callback=callback))
    
@router.callback_query(lambda callback: callback.data.startswith(data.Callback['brand']['new'])) #Выбрать модель бренда [Новинка]
async def model_new_items_choice(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = CURRENT_MEDIA,caption = data.Message['model']['new']),
                                                                    reply_markup=await catalogKeyboard.select_models_new_items(callback=callback))
    
@router.callback_query(lambda callback: callback.data == data.Callback['catalog']) #Каталог, выбрать бренд
async def callback_to_catalog(callback: types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = CURRENT_MEDIA,caption = data.Message['brand']['def']),
                                                                    reply_markup = await catalogKeyboard.select_brands())
      
        
    
    


     
        
    

    
    



