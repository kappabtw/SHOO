# -*- coding: windows-1251 -*-
from aiogram import types
from asql import ASQL

async def select_brands():
    brands = await ASQL.execute("SELECT DISTINCT Бренд FROM Кроссовки")
    
    row = []
    inline_buttons = []
    for brand in brands:
        row.append(types.InlineKeyboardButton(text=brand[0], callback_data=f"brand_adminpanel_{brand[0]}"))
        
        if len(row) == 3:
            inline_buttons.append(row)
            row = [] 

    if row:
        inline_buttons.append(row)

    inline_buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="admin_panel")])
    
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

async def select_models(callback: types.CallbackQuery):
    brand = callback.data.split("_")[2]
    models = await ASQL.execute(f"SELECT DISTINCT Модель FROM Кроссовки WHERE Бренд = ?", brand)
    row = []
    inline_buttons = []
    for model in models:
        row.append(types.InlineKeyboardButton(text=model[0], callback_data=f"model_adminpanel_{brand}_{model[0]}"))
                                            
        if len(row) == 3:
            inline_buttons.append(row)
            row = [] 

    if row:
        inline_buttons.append(row)

    inline_buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="redact_catalog")])
    
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)




    
          
