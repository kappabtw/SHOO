# -*- coding: windows-1251 -*-
from aiogram import types
from asql import ASQL
from Bot import data

new_orders_button = types.InlineKeyboardButton(text = "Новые заказы", callback_data="to_new_orders")
processed_orders_button = types.InlineKeyboardButton(text = "Заказы в обработке", callback_data="to_processed_orders")
closed_orders_button = types.InlineKeyboardButton(text = "Закрытые заказы", callback_data="to_closed_orders")

async def to_new_orders():
    new_orders_keyboard = types.InlineKeyboardButton(text = "Новые заказы", callback_data="to_new_orders")
    return types.InlineKeyboardMarkup(inline_keyboard=[[new_orders_keyboard]])

async def to_proccessed_orders():
    new_orders_keyboard = types.InlineKeyboardButton(text = "Заказы в обработке", callback_data="to_processed_orders")
    return types.InlineKeyboardMarkup(inline_keyboard=[[new_orders_keyboard]])

async def to_closed_orders():
    new_orders_keyboard = types.InlineKeyboardButton(text = "Закрытые заказы", callback_data="to_closed_orders")
    return types.InlineKeyboardMarkup(inline_keyboard=[[new_orders_keyboard]])

async def new_orders_keyboard(): 
    pass
    
