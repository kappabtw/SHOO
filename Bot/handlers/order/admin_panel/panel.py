# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from asql import ASQL
from Bot.Keyboards import adminCatalogKeyboard
from Bot import data


router = Router(name = "admin_panel")

redact_catalog_kb = types.InlineKeyboardButton(text = "Редактировать каталог", callback_data = "redact_catalog")
list_managers = types.InlineKeyboardButton(text = "Список менеджеров", callback_data = "managers_show")
show_orders = types.InlineKeyboardButton(text = "Заказы", callback_data = "types_orders")
clear_state = types.InlineKeyboardButton(text = "Очистить память", callback_data = "clearstate")

admin_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[redact_catalog_kb],
															 [list_managers, show_orders],
															 [clear_state]])
															   
															 

@router.message(Command("admin"))
async def admin_start_panel(message: types.Message):
	if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (message.from_user.id)))[0][0] != 1:
			return
	await message.answer_photo(photo = data.time_photo ,caption = "Выберите опцию", reply_markup= admin_keyboard)
	
@router.callback_query(lambda callback: callback.data == "adminpanel")
async def admin_start_panel(callback: types.CallbackQuery):
	if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
			return
	await callback.message.edit_caption(caption = "Выберите опцию", reply_markup= admin_keyboard)

	
	
@router.callback_query(lambda callback : callback.data == "redact_catalog")
async def redact_catalog(callback: types.CallbackQuery):
		if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
			return
		keyboard_brands = await adminCatalogKeyboard.select_brands()
		await callback.message.edit_caption(text = "Выберите бренд:", reply_markup = keyboard_brands)

	
@router.callback_query(lambda callback: callback.data.startswith("brandadminpanel_"))
async def show_models(callback: types.CallbackQuery):
	if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
			return
	show_models_kb = await adminCatalogKeyboard.select_models(callback)
	await callback.message.edit_media(media = types.InputMediaPhoto(media = data.time_photo, caption="Выберите модель:"), reply_markup=show_models_kb)
	

@router.callback_query(lambda callback: callback.data == "clearstate")
async def clearstate(callback: types.CallbackQuery, state: FSMContext):
	await state.clear()
	await callback.answer("Очищено")
	
@router.callback_query(lambda callback:callback.data == "managers_show")       
async def show_managers(callback : types.CallbackQuery):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ? AND access = 1)", (callback.from_user.id))
        if is_owner[0][0] != 1:
            return
        all_managers = await ASQL.execute("SELECT * FROM Менеджеры WHERE access = 0"                                  )
        text = "Список менеджеров [username|userid]:\n"
        print(all_managers)
        for manager in all_managers:
            text+= f"{manager[1]}|{manager[0]}\n\n"
        await callback.message.answer(text = text)
    except Exception as handler_error:
        await callback.answer(text = f"При обработке вашего запроса произошла ошибка : `{handler_error}`", show_alert = True)




