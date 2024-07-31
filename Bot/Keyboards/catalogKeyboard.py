# -*- coding: windows-1251 -*-
from aiogram import types
from asql import ASQL
from Bot.Keyboards import backToBrand
from Bot import data

sales = types.InlineKeyboardButton(text = data.Message['sales'], callback_data = data.Callback['sales'])
new_items = types.InlineKeyboardButton(text = data.Message['new_items'], callback_data = data.Callback['new_items'])

async def select_brands() -> types.InlineKeyboardMarkup:
    inline_buttons = [[sales, new_items]] 
    brands = await ASQL.execute("SELECT DISTINCT Бренд FROM Кроссовки WHERE Количество > 0;")

    row = []
    
    for brand in brands:
        row.append(types.InlineKeyboardButton(text=brand[0], callback_data=f"{data.Callback['brand']['def']}{brand[0]}"))
        
        if len(row) == 3:
            inline_buttons.append(row)
            row = [] 

    if row:
        inline_buttons.append(row)

    inline_buttons.append([types.InlineKeyboardButton(text=data.Message['back']['menu'], callback_data=data.Callback['menu'])])
    
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

async def select_models(callback: types.CallbackQuery):
    brand = callback.data.split("_")[1]
    models = await ASQL.execute(f"SELECT DISTINCT Модель FROM Кроссовки WHERE Бренд = ? AND Количество > 0 ", brand)
    inline_buttons = []
    row = []
    for model in models:
        row.append(types.InlineKeyboardButton(text=model[0], callback_data=f"{data.Callback['model']['def']}{brand}_{model[0]}"))
        if len(row) == 3:
            inline_buttons.append(row)
            row = []
    if row:
        inline_buttons.append(row)
    inline_buttons.append([backToBrand.back_to_brand])
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

async def select_brands_with_sales() -> types.InlineKeyboardMarkup:
    inline_buttons = [[new_items]] 
    brands = await ASQL.execute("SELECT DISTINCT Бренд FROM Кроссовки WHERE Скидка = 1 AND Количество > 0")

    row = []
    
    for brand in brands:
        row.append(types.InlineKeyboardButton(text=brand[0], callback_data=f"{data.Callback['brand']['sales']}{brand[0]}"))
        
        if len(row) == 3:
            inline_buttons.append(row)
            row = [] 

    if row:
        inline_buttons.append(row)

    inline_buttons.append([types.InlineKeyboardButton(text=data.Message['back']['catalog'], callback_data=data.Callback['catalog'])])
    
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

async def select_brands_new_items() -> types.InlineKeyboardMarkup:
    inline_buttons = [[sales]] 
    brands = await ASQL.execute("SELECT DISTINCT Бренд FROM Кроссовки WHERE Новинка = 1 AND Количество > 0")

    row = []
    
    for brand in brands:
        row.append(types.InlineKeyboardButton(text=brand[0], callback_data=f"{data.Callback['brand']['new']}{brand[0]}"))
        
        if len(row) == 3:
            inline_buttons.append(row)
            row = [] 

    if row:
        inline_buttons.append(row)

    inline_buttons.append([types.InlineKeyboardButton(text=data.Message['back']['catalog'], callback_data=data.Callback['catalog'])])
    
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

async def select_models_with_sales(callback: types.CallbackQuery):
    brand = callback.data.split("_")[2]
    models = await ASQL.execute(f"SELECT DISTINCT Модель FROM Кроссовки WHERE Бренд = ? AND Скидка = 1 AND Количество > 0", (brand))
    inline_buttons = []
    
    row = []
    for model in models:
        row.append(types.InlineKeyboardButton(text=model[0], callback_data=f"{data.Callback['model']['sales']}{brand}_{model[0]}"))
        if len(row) == 3:
            inline_buttons.append(row)
            row = []
    if row:
        inline_buttons.append(row)
    inline_buttons.append([types.InlineKeyboardButton(text = data.Message['back']['brand']['sales'], callback_data=data.Callback['sales'])])
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)

async def select_models_new_items(callback: types.CallbackQuery):
    brand = callback.data.split("_")[2]
    models = await ASQL.execute(f"SELECT DISTINCT Модель FROM Кроссовки WHERE Бренд = ? AND Новинка = 1 AND Количество > 0", (brand))
    inline_buttons = []
    row = []
    for model in models:
        row.append(types.InlineKeyboardButton(text=model[0], callback_data=f"{data.Callback['model']['new']}{brand}_{model[0]}"))
        if len(row) == 3:
            inline_buttons.append(row)
            row = []
    if row:
        inline_buttons.append(row)
    inline_buttons.append([types.InlineKeyboardButton(text = data.Message['back']['brand']['new'], callback_data=data.Callback['new_items'])])
    return types.InlineKeyboardMarkup(inline_keyboard=inline_buttons)






