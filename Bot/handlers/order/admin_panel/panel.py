# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.filters import Command
from asql import ASQL
from Bot.Keyboards import adminCatalogKeyboard
from Bot import data


router = Router(name = "admin_panel")

redact_catalog_kb = types.InlineKeyboardButton(text = "������������� �������", callback_data = "redact_catalog")

@router.message(Command("admin"))
async def admin_start_panel(message: types.Message):
	try:
		assert (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (message.from_user.id)))[0][0] == 1
		await message.answer_photo(photo = data.time_photo ,caption = "�������� �����", reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[redact_catalog_kb]]))
	except AssertionError:
		pass
	
@router.callback_query(lambda callback: callback.data == "admin_panel")
async def admin_start_panel(callback: types.CallbackQuery):
	try:
		assert (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (callback.from_user.id)))[0][0] == 1
		await callback.message.edit_caption(caption = "�������� �����", reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[redact_catalog_kb]]))
	except AssertionError:
		pass
	
	
@router.callback_query(lambda callback : callback.data == "redact_catalog")
async def redact_catalog(callback: types.CallbackQuery):
	keyboard_brands = await adminCatalogKeyboard.select_brands()
	await callback.message.edit_caption(text = "�������� �����:", reply_markup = keyboard_brands)
	
@router.callback_query(lambda callback: callback.data.startswith("brand_adminpanel_"))
async def show_models(callback: types.CallbackQuery):
	show_models_kb = await adminCatalogKeyboard.select_models(callback)
	await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo, caption="�������� ������:"), reply_markup=show_models_kb)
	




