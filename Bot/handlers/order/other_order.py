# -*- coding: windows-1251 -*-
from ast import parse
import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiosqlite import IntegrityError
from asql import ASQL
from Bot.Keyboards import orderKeyboard

router = Router	(name = "other_orders")
@router.callback_query(lambda callback: callback.data == "types_orders")
async def choice_orders_type(callback: types.CallbackQuery):
	
	try:
		is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id))
		assert is_owner[0][0] == 1
		orderTypesKeyboard = types.InlineKeyboardMarkup(
			inline_keyboard = [
				[
					types.InlineKeyboardButton(text = "Новые", callback_data = "to_new_orders"),
					types.InlineKeyboardButton(text = "В обработке", callback_data = "to_processed_orders"),
					types.InlineKeyboardButton(text = "Закрытые", callback_data = "to_closed_orders")
				]
			]
	
		)

		await callback.message.answer("Выберите тип заказов", reply_markup = orderTypesKeyboard)
	except AssertionError:
		pass
	except Exception as handler_exception:
		await callback.message.reply(f"Произошла ошибка: {handler_exception}") 

@router.callback_query(lambda callback: callback.data.startswith("order_"))
async def create_order(callback: types.CallbackQuery):
	try:
		order_data = callback.data.split("_")	   
		ordered_model = order_data[1]
		ordered_brand = order_data[2]
		ordered_color = order_data[3]
		print(order_data)
		#order_from_user_id = callback.from_user.id
		#order_from_user_name = f"@{callback.from_user.username}"
		#current_datetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

		sizes_and_ids = await ASQL.execute("SELECT Размер, id FROM Кроссовки WHERE Бренд = ? AND Модель = ? AND Расцветка = ? AND Количество > 0", (ordered_brand, ordered_model, ordered_color))
		
		# Create a keyboard with sizes as text and IDs as callback data
		keyboard = []
		row = []
		for size, model_id in sizes_and_ids:
			row.append(types.InlineKeyboardButton(text =  size, callback_data = f"generateorder_{model_id}"))
			if len(row) == 4:
				keyboard.append(row)
				row = []
		if row:
			keyboard.append(row)

		await callback.message.answer(f"Выберите *Размер* для `{ordered_brand} {ordered_model} ({ordered_color})`\nПосле *Вашего* выбора информация о заказе перейдёт нашим Менеджерам", 
								reply_markup= (types.InlineKeyboardMarkup(inline_keyboard=keyboard)),
								parse_mode= ParseMode.MARKDOWN)
		
	
	except Exception as order_create_error:
		await callback.answer(f"Извините, при обработке вашего заказа произошла ошибка : {order_create_error}", show_alert=True)
		return
	#all_managers = await ASQL.execute("SELECT id FROM Менеджеры")
	#for manager in all_managers:
		#await callback.bot.send_message(text="Только что был оформлен новый заказ.", chat_id=manager[0], parse_mode=ParseMode.MARKDOWN, reply_markup= await orderKeyboard.to_new_orders())
	

	await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("generateorder_"))
async def generate_order(callback:types.CallbackQuery):
	order_data = callback.data.split("_")[1:]
	ordered_id = int(order_data[0])
	order_from_user_id = callback.from_user.id
	order_from_user_name = f"@{callback.from_user.username}"
	current_datetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
	print(ordered_id)
	
	result = await ASQL.execute("INSERT INTO Заказы (\"model_id\", \"order_user_id\", \"order_user_name\", \"order_date\") VALUES(?,?,?,?) RETURNING \"order_id\"", (ordered_id, order_from_user_id, order_from_user_name, current_datetime))

	await callback.answer()	

	if result:
		await callback.message.edit_text(text = "Спасибо за заказ! В скором времени с Вами свяжется наш менеджер.")
		all_managers = await ASQL.execute("SELECT id FROM Менеджеры")
		for manager in all_managers:
			await callback.bot.send_message(text="Только что был оформлен новый заказ.", chat_id=manager[0], parse_mode=ParseMode.MARKDOWN, reply_markup= await orderKeyboard.to_new_orders())
	
	else:
		return
	


@router.callback_query(lambda callback: callback.data.startswith("close_order_"))
async def close_order(callback: types.CallbackQuery):
	try:
		data = callback.data.split("_")
		order_id = data[2]
		if data[-1] == "fromnew":
			fromnew = f",order_taken_by = {callback.from_user.id}"
		else:
			fromnew = ""
		current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
		write_off = True if data[3] == "write-off" else False
		is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id))
		if is_manager[0][0] != 1:
			return
		request = f"UPDATE Заказы SET order_in_process = ?, order_closed = ?, order_closed_date = ?, order_closed_by = ?, order_closed_write_off = ?{fromnew} WHERE order_id = ?"
		print(request)
		if write_off:
			await ASQL.execute("UPDATE Кроссовки SET Количество = Количество - 1 WHERE id = (SELECT model_id FROM Заказы WHERE order_id = ?)", (order_id))
		await ASQL.execute(request,(0, 1, current_time, callback.from_user.id, 1 if write_off else 0, order_id))
		await callback.answer(text = f"Заказ {order_id} был успешно закрыт {'без списания' if not write_off else ''}", show_alert = True)
	except IntegrityError as e:
		await callback.answer(text=f'Ошибка: {e}', show_alert=True) 
	except RuntimeError as runtime_error:
		callback.answer(text = runtime_error)
		

		
@router.callback_query(lambda callback: callback.data.startswith("in_process_order_"))
async def take_order(callback: types.CallbackQuery):
	try:
		is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id))
		if is_manager[0][0] != 1:
			return
		data = callback.data.split("_")
		order_id = data[3]
		if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Заказы WHERE order_id = ? AND order_in_process = 1)", (order_id)))[0][0] == 1:
			await callback.answer("Заказ уже был взят")
			return
		await ASQL.execute("UPDATE Заказы SET order_in_process = 1, order_taken_by = ? WHERE order_id = ?", (callback.from_user.id, order_id))
		await callback.answer("Заказ помечен как обрабатываемый")
	except IntegrityError as e:
		await callback.answer(text=f'Ошибка: {e}', show_alert=True) 
	except RuntimeError as runtime_error:
		await callback.answer(text = runtime_error, show_alert= True)
		
	
	
	

	

