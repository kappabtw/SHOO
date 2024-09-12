# -*- coding: windows-1251 -*-
from tkinter import CURRENT
from aiogram import Router, types
from aiogram.enums import ParseMode
from asql import ASQL
from Bot import data
from Bot.requests.model_display import *

router = Router(name = "models")

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

@router.callback_query(lambda callback: any(callback.data.startswith(model_options) for model_options in data.model_options))
async def callback_show_model_info(callback: types.CallbackQuery):
    list_id:list = await get_models_id(callback.data)  # Получаем список ID моделей
    if not list_id: 
        await callback.answer(text = "Извините, модель не найдена", show_alert=True)
        return
    current_index:int = 0
    count_list_id:int = len(list_id)
    txt:str = await get_text_about_model(list_id[current_index], current = 1, count=count_list_id)  # Получаем подпись к изображению
    photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE id = ? AND Количество > 0", (list_id[current_index]))
    photo_id = photo_from_db[0][0]
    if not photo_id:
        photo_id = data.no_image_photo
        
    
    if count_list_id > 1:
        keyboard_prev_next = types.InlineKeyboardMarkup(
                                                          inline_keyboard=[
                                                              [
                                                                  types.InlineKeyboardButton(text = "Назад", callback_data=f"prev_{callback.data}_{current_index}"),
                                                                  types.InlineKeyboardButton(text = "Вперед", callback_data=f"next_{callback.data}_{current_index}")
                                                                ],
                                                              [
                                                              types.InlineKeyboardButton(text = "Заказать", callback_data = f"order_{list_id[current_index]}_{callback.from_user.id}")    
                                                                ],
                                                              [
                                                                  types.InlineKeyboardButton(text = "Назад к моделям", callback_data= await get_back_model_callback(f"zero_{callback.data}"))
                                                                  ]
                                                          ]
                                                        )

        await callback.message.edit_media(media=types.InputMediaPhoto(media = photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
                                      reply_markup=keyboard_prev_next)
    else:
        keyboard_alone = types.InlineKeyboardMarkup(
                                                          inline_keyboard=[
                                                              
                                                            [
                                                                types.InlineKeyboardButton(text = "Заказать", callback_data = f"order_{list_id[current_index]}_{callback.from_user.id}")    
                                                                ],
                                                              [
                                                                  types.InlineKeyboardButton(text = "Назад к моделям", callback_data= await get_back_model_callback(f"zero_{callback.data}"))
                                                                  ]
                                                          ]
                                                        )
        await callback.message.edit_media(media=types.InputMediaPhoto(media = photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
                                      reply_markup=keyboard_alone)
    await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("prev_defmodel_") or callback.data.startswith("next_defmodel_") or callback.data.startswith("prev_model_") or callback.data.startswith("next_model_")) #todo: hand 1
async def callback_prev_next(callback: types.CallbackQuery):
    print(callback.data)
    parts = callback.data.split("_")
    model_data = "_".join(parts[1:-1])
    current_index = int(parts[-1])
    list_id = await get_models_id(model_data)  # Получаем список ID моделей
    count_list_id = len(list_id)
    if callback.data.startswith("prev_"):
        current_index -= 1
    elif callback.data.startswith("next_"):
        current_index += 1
    if current_index < 0:
        current_index = len(list_id) - 1
    elif current_index >= len(list_id):
        current_index = 0
    txt = await get_text_about_model(list_id[current_index], current=current_index + 1, count = len(list_id))
    photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE id = ? AND Количество > 0", (list_id[current_index]))
    photo_id = photo_from_db[0][0]
    if count_list_id > 1:
        keyboard_prev_next = types.InlineKeyboardMarkup(
                                                            inline_keyboard=[
                                                                [
                                                                    types.InlineKeyboardButton(text = "Назад", callback_data=f"prev_{model_data}_{current_index}"),
                                                                    types.InlineKeyboardButton(text = "Вперед", callback_data=f"next_{model_data}_{current_index}")
                                                                    ],
                                                                [
                                                                    types.InlineKeyboardButton(text = "Заказать", callback_data = f"order_{list_id[current_index]}_{callback.from_user.id}")    
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
    else:
        keyboard_prev_next = types.InlineKeyboardMarkup(
                                                            inline_keyboard=[
                                                                [
                                                                    types.InlineKeyboardButton(text = "Заказать", callback_data = f"order_{list_id[current_index]}_{callback.from_user.id}")    
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
