# -*- coding: windows-1251 -*-
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
    list_id:list = await get_models_id(callback.data)  # �������� ������ ID �������
    if not list_id: 
        await callback.answer(text = "��������, ������ �� �������", show_alert=True)
        return
    current_index:int = 0
    count_list_id:int = len(list_id)
    txt:str = await get_text_about_model(list_id[current_index], current = 1, count=count_list_id)  # �������� ������� � �����������
    photo_from_db = await ASQL.execute("SELECT ���� FROM ��������� WHERE id = ? AND ���������� > 0", (list_id[current_index]))
    photo_id = photo_from_db[0][0]
    model_data = callback.data.split("_")
    del model_data[0:3] 
    model_data = "_".join(model_data)
    if not photo_id:
        photo_id = data.no_image_photo
        
    
    if count_list_id > 1:
        keyboard_prev_next = types.InlineKeyboardMarkup(
                                                          inline_keyboard=[
                                                              [
                                                                  types.InlineKeyboardButton(text = "�����", callback_data=f"prev_{callback.data}_{current_index}"),
                                                                  types.InlineKeyboardButton(text = "������", callback_data=f"next_{callback.data}_{current_index}")
                                                                ],
                                                              [
                                                              types.InlineKeyboardButton(text = "��������", callback_data = f"order_{model_data}")    
                                                                ],
                                                              [
                                                                  types.InlineKeyboardButton(text = "����� � �������", callback_data= await get_back_model_callback(f"zero_{callback.data}"))
                                                                  ]
                                                          ]
                                                        )

        await callback.message.edit_media(media=types.InputMediaPhoto(media = photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
                                      reply_markup=keyboard_prev_next)
    else:
        keyboard_alone = types.InlineKeyboardMarkup(
                                                          inline_keyboard=[
                                                              
                                                            [
                                                                types.InlineKeyboardButton(text = "��������", callback_data = f"order_{model_data}")    
                                                                ],
                                                              [
                                                                  types.InlineKeyboardButton(text = "����� � �������", callback_data= await get_back_model_callback(f"zero_{callback.data}"))
                                                                  ]
                                                          ]
                                                        )
        await callback.message.edit_media(media=types.InputMediaPhoto(media = photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
                                      reply_markup=keyboard_alone)
    await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("prev_") or callback.data.startswith("next_"))
async def callback_prev_next(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    model_data = "_".join(parts[1:-1])
    current_index = int(parts[-1])
    list_id = await get_models_id(model_data)  # �������� ������ ID �������
    if callback.data.startswith("prev_"):
        current_index -= 1
    else:
        current_index += 1
    if current_index < 0:
        current_index = len(list_id) - 1
    elif current_index >= len(list_id):
        current_index = 0
    txt = await get_text_about_model(list_id[current_index], current=current_index + 1, count = len(list_id))
    photo_from_db = await ASQL.execute("SELECT ���� FROM ��������� WHERE id = ? AND ���������� > 0", (list_id[current_index]))
    photo_id = photo_from_db[0][0]
    
    keyboard_prev_next = types.InlineKeyboardMarkup(
                                                        inline_keyboard=[
                                                            [
                                                                types.InlineKeyboardButton(text = "�����", callback_data=f"prev_{model_data}_{current_index}"),
                                                                types.InlineKeyboardButton(text = "������", callback_data=f"next_{model_data}_{current_index}")
                                                                ],
                                                            [
                                                                types.InlineKeyboardButton(text = "��������", callback_data = f"order_{model_data}")    
                                                                ],
                                                            [
                                                              types.InlineKeyboardButton(text = "����� � �������", callback_data= await get_back_model_callback(f"zero_{model_data}"))
                                                          ]
                                                      ]
                                                    )

    await callback.message.edit_media(
                                        media=types.InputMediaPhoto(media=photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
                                        reply_markup=keyboard_prev_next
                                     )                      

    await callback.answer()
