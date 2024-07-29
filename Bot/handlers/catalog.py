# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from asql import ASQL
from Bot.Keyboards import catalogKeyboard
from Bot import data
from Bot.requests.show_model import *

router = Router()

async def get_back_model_callback(callback : str):
    callback = callback.split("_")
    callback.pop(0)
    callback = "_".join(callback)
    if callback.startswith(data.Callback['model']['def']):
        parts = callback.split("_")
        return f"{data.Callback['brand']['def']}{parts[1]}"
    elif callback.startswith(data.Callback['model']['sales']):
        parts = callback.split("_")
        return f"{data.Callback['brand']['sales']}{parts[2]}"
    elif callback.startswith(data.Callback['model']['new']):
        parts = callback.split("_")
        return f"{data.Callback['brand']['new']}{parts[2]}"

@router.message(Command("catalog"))
async def cmd_catalog(msg: types.Message):
     await msg.answer_photo(photo = data.time_photo,caption = data.Message['brand']['def'], reply_markup = await catalogKeyboard.select_brands())
     
@router.callback_query(lambda callback: callback.data.startswith(data.Callback['brand']['def'])) #Выбрать модель бренда 
async def model_choice(callback: types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo,caption = data.Message["model"]['def']),
                                                                    reply_markup=await catalogKeyboard.select_models(callback))    
    await callback.answer()
    
@router.callback_query(lambda callback: callback.data == data.Callback['sales']) #Выбрать бренд [Скидка]
async def callback_sales(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media=types.InputMediaPhoto(media = data.time_photo,caption = data.Message['brand']['sales']),
                                      reply_markup= await catalogKeyboard.select_brands_with_sales())
    

@router.callback_query(lambda callback: callback.data == data.Callback['new_items']) #Выбрать бренд [Новинка]
async def callback_new_items(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo,caption = data.Message['brand']['new']),
                                                                    reply_markup= await catalogKeyboard.select_brands_new_items())
    
@router.callback_query(lambda callback: callback.data.startswith(data.Callback['brand']['sales'])) #Выбрать модель бренда [Скидка]
async def model_sales_choice(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo,caption = data.Message['model']['sales']),
                                                                    reply_markup=await catalogKeyboard.select_models_with_sales(callback=callback))
    
@router.callback_query(lambda callback: callback.data.startswith(data.Callback['brand']['new'])) #Выбрать модель бренда [Новинка]
async def model_new_items_choice(callback:types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo,caption = data.Message['model']['new']),
                                                                    reply_markup=await catalogKeyboard.select_models_new_items(callback=callback))
    
@router.callback_query(lambda callback: callback.data == data.Callback['catalog']) #Каталог, выбрать бренд
async def callback_to_catalog(callback: types.CallbackQuery):
    print(callback.data)
    await callback.message.edit_media(media = types.InputMediaPhoto(media =data.time_photo,caption = data.Message['brand']['def']),
                                                                    reply_markup = await catalogKeyboard.select_brands())
    
@router.callback_query(lambda callback: any(callback.data.startswith(model_options) for model_options in data.model_options))
async def callback_show_model_info(callback: types.CallbackQuery):
    list_id = await get_models_id(callback.data)  # Получаем список ID моделей
    current_index = 0
    txt = await show_model(list_id[current_index], current= 1, count=len(list_id))  # Получаем подпись к изображению
    keyboard_prev_next = types.InlineKeyboardMarkup(
                                                      inline_keyboard=[
                                                          [
                                                              types.InlineKeyboardButton(text = "Назад", callback_data=f"prev_{callback.data}_{current_index}"),
                                                              types.InlineKeyboardButton(text = "Вперед", callback_data=f"next_{callback.data}_{current_index}")
                                                          ],
                                                          [
                                                              types.InlineKeyboardButton(text = "Назад к моделям", callback_data= await get_back_model_callback(f"zero_{callback.data}"))
                                                              ]
                                                      ]
                                                    )

    photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE id = ?", (list_id[current_index]))
    photo_id = photo_from_db[0][0]
    await callback.message.edit_media(media=types.InputMediaPhoto(media = photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
                                  reply_markup=keyboard_prev_next)
    await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("prev_") or callback.data.startswith("next_"))
async def callback_prev_next(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    model_data = "_".join(parts[1:-1])
    current_index = int(parts[-1])
    list_id = await get_models_id(model_data)  # Получаем список ID моделей
    if callback.data.startswith("prev_"):
        current_index -= 1
    else:
        current_index += 1
    if current_index < 0:
        current_index = len(list_id) - 1
    elif current_index >= len(list_id):
        current_index = 0
    txt = await show_model(list_id[current_index], current=current_index + 1, count = len(list_id))
    photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE id = ?", (list_id[current_index]))
    photo_id = photo_from_db[0][0]
    
    keyboard_prev_next = types.InlineKeyboardMarkup(
                                                      inline_keyboard=[
                                                          [
                                                              types.InlineKeyboardButton(text = "Назад", callback_data=f"prev_{model_data}_{current_index}"),
                                                              types.InlineKeyboardButton(text = "Вперед", callback_data=f"next_{model_data}_{current_index}")
                                                          ],
                                                          [
                                                              types.InlineKeyboardButton(text = "Назад к моделям", callback_data= await get_back_model_callback(f"zero_{model_data}"))
                                                          ]
                                                      ]
                                                    )

    await callback.message.edit_media(
                                        media=types.InputMediaPhoto(media=photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
                                        reply_markup=keyboard_prev_next
                                     )                      

    await callback.answer()   
        
@router.message(Command('load'))
async def load_photo(message: types.Message):
    shoes_id = message.caption.split(" ")[1]
    photo_id = message.photo[-1].file_id
    await ASQL.execute("UPDATE Кроссовки SET Фото = ? WHERE id = ?", (photo_id,shoes_id))

    # Обработка загруженной фотографии
    await message.answer('Фотография успешно загружена.')
    
    


     
        
    

    
    



