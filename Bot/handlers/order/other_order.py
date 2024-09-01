# -*- coding: windows-1251 -*-
import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from asql import ASQL
from Bot.Keyboards import orderKeyboard

router = Router	(name = "other_orders")
@router.message(Command("orders"))
async def choice_orders_type(message: types.Message):
	try:
		is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (message.from_user.id))
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

		await message.answer("Выберите тип заказов", reply_markup = orderTypesKeyboard)
	except AssertionError:
		pass
	except Exception as handler_exception:
		await message.reply(f"Произошла ошибка: {handler_exception}") 

@router.callback_query(lambda callback: callback.data.startswith("order_"))
async def create_order(callback: types.CallbackQuery):
	try:
		order_data = callback.data.split("_")
		ordered_model_id = order_data[1]
		order_from_user_id = order_data[2]
		order_from_user_name = f"@{callback.from_user.username}"
		current_datetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
		await ASQL.execute("INSERT INTO Заказы (model_id, order_user_id, order_date, order_user_name) VALUES (?,?,?,?)", (ordered_model_id, order_from_user_id, current_datetime, order_from_user_name))
	except Exception as order_create_error:
		await callback.answer(f"Извините, при обработке вашего заказа произошла ошибка : {order_create_error}", show_alert=True)
		return
	await callback.answer("Спасибо за заказ!\nПосле проверки наличия модели на складе с Вами свяжется наш менеджер", show_alert=True)
	all_managers = await ASQL.execute("SELECT id FROM Менеджеры")
	for manager in all_managers:
		await callback.bot.send_message(text="Только что был оформлен новый заказ.", chat_id=manager[0], parse_mode=ParseMode.MARKDOWN, reply_markup= await orderKeyboard.to_new_orders())
	

	await callback.answer()
		

@router.callback_query(lambda callback: callback.data.startswith("close_order_"))
async def close_order(callback: types.CallbackQuery):
	try:
		data = callback.data.split("_")
		order_id = data[2]
		current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
		write_off = True if data[3] == "write-off" else False
		is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id))
		assert is_manager[0][0] == 1
		await ASQL.execute(f"UPDATE Заказы SET order_in_process = ?, order_closed = ?, order_closed_date = ?, order_closed_by = ?, order_closed_write_off = ? WHERE order_id = ?",
					 (0, 1, current_time, callback.from_user.id, 1 if write_off else 0, order_id))
		if write_off:
			await ASQL.execute("UPDATE Кроссовки SET Количество = Количество - 1 WHERE id = (SELECT model_id FROM Заказы WHERE order_id = ?)", (order_id))
		await callback.answer(text = f"Заказ {order_id} был успешно закрыт {'без списания' if not write_off else ''}", show_alert = True)
	except AssertionError:
		await callback.answer()
	except RuntimeError as runtime_error:
		callback.answer(text = runtime_error)
		

		
@router.callback_query(lambda callback: callback.data.startswith("in_process_order_"))
async def take_order(callback: types.CallbackQuery):
	try:
		is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id))
		assert is_manager[0][0] == 1
		data = callback.data.split("_")
		order_id = data[3]
		if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Заказы WHERE order_id = ? AND order_in_process = 1)", (order_id)))[0][0] == 1:
			await callback.answer("Заказ уже был взят")
			return
		await ASQL.execute("UPDATE Заказы SET order_in_process = 1, order_taken_by = ? WHERE order_id = ?", (callback.from_user.id, order_id))
		await callback.answer("Заказ помечен как обрабатываемый")
	except AssertionError:
		await callback.answer()
	except RuntimeError as runtime_error:
		await callback.answer(text = runtime_error, show_alert= True)
		
	
	
	

	

