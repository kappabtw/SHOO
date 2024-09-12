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
		
		list_id:list = await model_display.get_models_id(callback.data, positive_count = False)  # Получаем список ID моделей
		if not list_id: 
			await callback.answer(text = "Извините, модель не найдена", show_alert=True)
			return
		
		current_index:int = 0
		count_list_id:int = len(list_id)
		model_data = callback.data.split("_")
		if model_data[-1] == "+" or model_data[-1] == "-":
			current_index = int(model_data.pop(-2))
			try:
				await ASQL.execute(f"UPDATE Кроссовки SET Количество = Количество {model_data[-1]} 1 WHERE id = ?", (list_id[current_index]))
				model_data.pop(-1)
			except IntegrityError:
				await callback.answer("Количество не может быть меньше нуля", show_alert = True)
				return
				
		txt:str = await model_display.get_text_about_model(list_id[current_index], current = 1, count=count_list_id, enable_manager_info= True)  # Получаем подпись к изображению
		photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE id = ?", (list_id[current_index]))
		photo_id = photo_from_db[0][0]
			
			
		brand = model_data[1] 
		model_data = "_".join(model_data)  #это и есть callback.data
		print(f"prev_{model_data}_{current_index}")
		if not photo_id:
			photo_id = model_display.data.no_image_photo
		
	
		if count_list_id > 1:
			keyboard_prev_next = types.InlineKeyboardMarkup(
															inline_keyboard=[
																[
																	  types.InlineKeyboardButton(text = "-", callback_data = f"{model_data}_{current_index}_-"),
																	  types.InlineKeyboardButton(text = "+", callback_data = f"{model_data}_{current_index}_+")
																],
																[
																		types.InlineKeyboardButton(text = "Редактировать", callback_data = f"redactmodels_{','.join(map(str,list_id))}")
																],
																  
																[
																	  types.InlineKeyboardButton(text = "Назад", callback_data=f"prev_{model_data}_{current_index}"),
																	  types.InlineKeyboardButton(text = "Вперед", callback_data=f"next_{model_data}_{current_index}")
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
																	types.InlineKeyboardButton(text = "-", callback_data = f"{model_data}_{current_index}_-"),
																	types.InlineKeyboardButton(text = "+", callback_data = f"{model_data}_{current_index}_+")
																	],
																[
																		types.InlineKeyboardButton(text = "Редактировать", callback_data = f"redactmodels_{','.join(map(str,list_id))}")
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

@router.callback_query(lambda callback: callback.data.startswith("prev_modeladminpanel_") or callback.data.startswith("next_modeladminpanel_"))   
async def callback_prev_next(callback: types.CallbackQuery):
	try:
		
		is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id =  ?)", (callback.from_user.id))
		assert is_manager[0][0] == 1
		
		model_data = callback.data.split("_")
		sign = None
		if model_data[-1] == "+" or model_data[-1] == "-":
			sign = model_data.pop(-1)
			index_for_change = int(model_data.pop(-1))
		print(model_data)
		current_index = int(model_data[-1])
		brand = model_data[2]
		model_data = "_".join(model_data[1:-1])
		list_id = await model_display.get_models_id(model_data, positive_count = False)
		
		if sign is not None:
			try:
				await ASQL.execute(f"UPDATE Кроссовки SET Количество = Количество {sign} 1 WHERE id = ?", (list_id[index_for_change]))
			except IntegrityError:
				await callback.answer("Количество не может быть меньше нуля", show_alert = True)
				return
		count_list_id = len(list_id)
		if callback.data.startswith("prev_"):
			current_index -= 1
		elif callback.data.startswith("next_"):
			current_index += 1
		if current_index < 0:
			current_index = len(list_id) - 1
		elif current_index >= len(list_id):
			current_index = 0  
		txt = await model_display.get_text_about_model(list_id[current_index], current=current_index + 1, count = len(list_id), enable_manager_info= True)
		photo_from_db = await ASQL.execute("SELECT Фото FROM Кроссовки WHERE id = ? AND Количество > 0", (list_id[current_index]))
		photo_id = photo_from_db[0][0]
		
		if count_list_id > 1:
			keyboard_prev_next = types.InlineKeyboardMarkup(
																inline_keyboard=[
																	[
																		types.InlineKeyboardButton(text = "-", callback_data = f"{model_data}_{current_index}_-"),
																		types.InlineKeyboardButton(text = "+", callback_data = f"{model_data}_{current_index}_+")
																	],
																	[
																		types.InlineKeyboardButton(text = "Редактировать", callback_data = f"redactmodels_{','.join(map(str,list_id))}")
																	],
																	[
																		types.InlineKeyboardButton(text = "Назад", callback_data=f"prev_{model_data}_{current_index}"),
																		types.InlineKeyboardButton(text = "Вперед", callback_data=f"next_{model_data}_{current_index}")
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
																		types.InlineKeyboardButton(text = "-", callback_data = f"{model_data}_{current_index}_-"),
																		types.InlineKeyboardButton(text = "+", callback_data = f"{model_data}_{current_index}_+")
																	],
																	[
																		types.InlineKeyboardButton(text = "Редактировать", callback_data = f"redactmodels_{','.join(map(str,list_id))}")
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
