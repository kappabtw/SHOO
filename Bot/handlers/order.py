# -*- coding: windows-1251 -*-
import datetime
from aiogram import Router, types
from aiogram.enums import ParseMode
from asql import ASQL
from Bot import data
from Bot.Keyboards import orderKeyboard

router = Router	(name = "orders")

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
	await callback.answer("Спасибо за заказ!\nВ ближайшем времени с вами свяжется наш менеджер", show_alert=True)
	all_managers = await ASQL.execute("SELECT id FROM Менеджеры")
	for manager in all_managers:
		await callback.bot.send_message(text="Только что был оформлен новый заказ.", chat_id=manager[0], parse_mode=ParseMode.MARKDOWN, reply_markup= await orderKeyboard.to_new_orders())
	

	await callback.answer()
	
@router.callback_query(lambda callback: callback.data == "to_new_orders")
async def show_new_orders(callback: types.CallbackQuery):
	try:
		order_data = await ASQL.execute("SELECT * FROM Заказы WHERE order_closed = 0 AND order_in_proccess = 0 AND order_id = (SELECT MAX(order_id) FROM Заказы WHERE order_closed = 0 AND order_in_proccess = 0)")
		
		order_data = order_data[0]
		order_model_id = order_data[0]
		order_id = order_data[1]
		order_user_id = order_data[2]
		order_user_name = order_data[3]
		order_date = order_data[4]
		
		model_data = await ASQL.execute("SELECT Бренд,Модель,Размер,Расцветка FROM Кроссовки WHERE id = ?", (order_model_id))
		
		model_data = model_data[0]
		model_brand = model_data[0]
		model_name = model_data[1]
		model_size = model_data[2]
		model_color = model_data[3]
		
		order_text = f'''
Заказ #{order_id}
Время создания - {order_date}
Заказчик - {order_user_name}

Бренд - {model_brand}
Модель - {model_name}
Размер - {model_size}
Расцветка - {model_color}
		'''
		
		keyboard_next_prev = types.InlineKeyboardMarkup(
			inline_keyboard= [
				[
					types.InlineKeyboardButton(text = "Назад", callback_data = f"prev_order_{order_id}"),
					types.InlineKeyboardButton(text = "Вперёд", callback_data = f"next_order_{order_id}")
				],
				[
					types.InlineKeyboardButton(text = "Чат с заказчиком", url = f"tg://user?id={order_user_id}")	
				]
			]
		)
		await callback.message.edit_text(text=order_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_next_prev)
	except Exception as e:
		await callback.answer(f"Ошибка: {e}", show_alert=True)
        
@router.callback_query(lambda callback: callback.data.startswith("next_order") or callback.data.startswith("prev_order"))
async def next_prev_order():
	pass

	

