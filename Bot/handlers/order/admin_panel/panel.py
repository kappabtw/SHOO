# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.filters import Command
from asql import ASQL
from Bot.Keyboards import adminCatalogKeyboard
from Bot import data


router = Router(name = "admin_panel")

redact_catalog_kb = types.InlineKeyboardButton(text = "Редактировать каталог", callback_data = "redact_catalog")
list_managers = types.InlineKeyboardButton(text = "Список менеджеров", callback_data = "managers_show")
show_orders = types.InlineKeyboardButton(text = "Заказы", callback_data = "types_orders")

admin_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[redact_catalog_kb],
															 [list_managers, show_orders]])
															   
															 

@router.message(Command("admin"))
async def admin_start_panel(message: types.Message):
	try:
		assert (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (message.from_user.id)))[0][0] == 1
		await message.answer_photo(photo = data.time_photo ,caption = "Выберите опцию", reply_markup= admin_keyboard)
	except AssertionError:
		pass
	
@router.callback_query(lambda callback: callback.data == "adminpanel")
async def admin_start_panel(callback: types.CallbackQuery):
	try:
		assert (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] == 1
		await callback.message.edit_caption(caption = "Выберите опцию", reply_markup= admin_keyboard)
	except AssertionError:
		pass
	
	
@router.callback_query(lambda callback : callback.data == "redact_catalog")
async def redact_catalog(callback: types.CallbackQuery):
	try:
		assert (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] == 1
		keyboard_brands = await adminCatalogKeyboard.select_brands()
		await callback.message.edit_caption(text = "Выберите бренд:", reply_markup = keyboard_brands)
	except AssertionError:
		pass
	
@router.callback_query(lambda callback: callback.data.startswith("brandadminpanel_"))
async def show_models(callback: types.CallbackQuery):
	try:
		assert (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] == 1
		show_models_kb = await adminCatalogKeyboard.select_models(callback)
		await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo, caption="Выберите модель:"), reply_markup=show_models_kb)
	except AssertionError:
		pass
	




