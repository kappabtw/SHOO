# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiosqlite import IntegrityError
from asql import ASQL
from Bot.requests import model_display

router = Router()

@router.callback_query(lambda callback: callback.data.startswith("modeladminpanel_"))
async def show_model(callback : types.CallbackQuery):
	try:
		print(callback.data)
		is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id =  ?)", (callback.from_user.id))
		assert is_manager[0][0] == 1
		
		model_data = callback.data.split("_")[1:]
		brand = model_data[0]
		model = model_data[1]
		list_id:list = await model_display.get_models_id(callback.data, False)  # Получаем список ID моделей
		if not list_id: 
			await callback.answer(text = "Извините, модель не найдена", show_alert=True)
			return
		current_index:int = 0
		count_list_id:int = len(list_id)
		color = list_id[current_index][0]
				
		txt:str = await model_display.get_text_about_model(brand,model,list_id, current = 0, count=count_list_id)  # Получаем подпись к изображению
		photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE Бренд = ? AND Модель = ? AND Расцветка = ?", (brand, model, color))
		photo_id = photo_from_db[0][0]
		
		if not photo_id:
			photo_id = model_display.data.no_image_photo
		
	
		if count_list_id > 1:
			keyboard_prev_next = types.InlineKeyboardMarkup(
															inline_keyboard=[
																[
																		types.InlineKeyboardButton(text = "Редактировать", callback_data = f"redactmodels_{brand}_{model}_{color}")
																],
																  
																[
																	  types.InlineKeyboardButton(text = "Назад", callback_data=f"modeladminpanelprev_{brand}_{model}_{current_index}"),
																	  types.InlineKeyboardButton(text = "Вперед", callback_data=f"modeladminpanelnext_{brand}_{model}_{current_index}")
																],

															    [
																	  types.InlineKeyboardButton(text = "Назад к моделям", callback_data= f"brandadminpanel_{brand}")
																]
															  ]
															)

			await callback.message.edit_media(media=types.InputMediaPhoto(media = photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
										  reply_markup=keyboard_prev_next)
		else:
			keyboard_alone = types.InlineKeyboardMarkup(
															inline_keyboard=[
																[
																		types.InlineKeyboardButton(text = "Редактировать",callback_data = f"redactmodels_{brand}_{model}_{color}")
																	],
																[
																	types.InlineKeyboardButton(text = "Назад к моделям", callback_data= f"brandadminpanel_{brand}")
																	]
															  ]
															)
			await callback.message.edit_media(media=types.InputMediaPhoto(media = photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
										  reply_markup=keyboard_alone)
		await callback.answer()
		
	except AssertionError:
		pass
	except RuntimeError as runerror:
		await callback.answer(text = f"Ошибка базы данных: {runerror}", show_alert= True)
	finally:
		await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("modeladminpanelprev_") or callback.data.startswith("modeladminpanelnext_"))   
async def callback_prev_next(callback: types.CallbackQuery):
	try:

		print(callback.data)
		
		is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id =  ?)", (callback.from_user.id))
		assert is_manager[0][0] == 1
		
		parts = callback.data.split("_")
		brand = parts[1]
		model = parts[2]
		current_index = int(parts[-1])
		list_id = await model_display.get_models_id(callback.data, False)  # Получаем список ID моделей
		count_list_id = len(list_id)
		if callback.data.startswith("modeladminpanelprev_"):
			current_index -= 1
		elif callback.data.startswith("modeladminpanelnext_"):
			current_index += 1
		if current_index < 0:
			current_index = len(list_id) - 1
		elif current_index >= len(list_id):
			current_index = 0
		color = list_id[current_index][0]
		print(0)
		txt = await model_display.get_text_about_model(brand,model,list_id,current=current_index, count = count_list_id)
		print(1)
		photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE Бренд = ? AND Модель = ? AND Расцветка = ?", (brand, model, color))
		print(photo_from_db)
		photo_id = photo_from_db[0][0]
		
		if count_list_id > 1:
			keyboard_prev_next = types.InlineKeyboardMarkup(
																inline_keyboard=[
																	[
																		types.InlineKeyboardButton(text = "Редактировать", callback_data = f"redactmodels_{brand}_{model}_{color}")
																	],
																	[
																		types.InlineKeyboardButton(text = "Назад", callback_data=f"modeladminpanelprev_{brand}_{model}_{current_index}"),
																		types.InlineKeyboardButton(text = "Вперед", callback_data=f"modeladminpanelnext_{brand}_{model}_{current_index}")
																		],
																
																	[
																		types.InlineKeyboardButton(text = "Назад к моделям", callback_data= f"brandadminpanel_{brand}")
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
																		types.InlineKeyboardButton(text = "Редактировать", callback_data = f"redactmodels_{brand}_{model}_{color}")
																	],
																
																	[
																		types.InlineKeyboardButton(text = "Назад к моделям", callback_data= f"brandadminpanel_{brand}")
																	]
																]
															)

			await callback.message.edit_media(
												media=types.InputMediaPhoto(media=photo_id, caption=txt, parse_mode=ParseMode.MARKDOWN),
												reply_markup=keyboard_prev_next
												)
	except AssertionError:
		pass
	except RuntimeError as runerror:
		await callback.answer(text = f"Ошибка базы данных: {runerror}", show_alert= True)
	finally:
		await callback.answer()
