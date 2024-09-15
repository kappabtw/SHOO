# -*- coding: windows-1251 -*-
import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from asql import ASQL
from Bot.Keyboards import orderKeyboard

router = Router	(name = "new_orders")

@router.callback_query(lambda callback: callback.data == "to_new_orders")
async def show_new_orders(callback: types.CallbackQuery):
	query = """
		SELECT 
			(SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id =?)) AS is_manager,
			o.order_id, o.order_user_id, o.order_user_name, o.order_date, k.Бренд, k.Модель, k.Размер, k.Расцветка,k.Количество,
			(SELECT COUNT(*) FROM Заказы WHERE model_id = o.model_id AND order_in_process = 1) AS orders_in_process_count
		FROM 
			Заказы o
		JOIN 
			Кроссовки k ON o.model_id = k.id
		WHERE 
			o.order_closed = 0 AND o.order_in_process = 0 AND o.order_id = (SELECT MIN(order_id) FROM Заказы WHERE order_closed = 0 AND order_in_process = 0)
	"""
	try:
		result = await ASQL.execute(query, (callback.from_user.id))
		
		if not result:
			await callback.answer("Новых заказов нет")
			return
		
		is_manager = result[0][0]
		
		if is_manager != 1:
			return
		
		order_id = result[0][1]
		order_user_id = result[0][2]
		order_user_name = result[0][3]
		order_date = result[0][4]
		model_brand = result[0][5]
		model_name = result[0][6]
		model_size = result[0][7]
		model_color = result[0][8]
		model_count = result[0][9]
		orders_model_count = result[0][10]

		print(result)		



		order_text = f'''
Заказ #{order_id}
Время создания - {order_date}
Заказчик - {order_user_name}

Бренд - {model_brand}
Модель - {model_name}
Размер - {model_size}
Расцветка - {model_color}
Количество на складе - {model_count}

Заказов в обработке с такой же моделью - {orders_model_count}
		'''
		
		keyboard_next_prev = types.InlineKeyboardMarkup(
			inline_keyboard= [
				[
					types.InlineKeyboardButton(text = "Назад", callback_data = f"prevorder_{order_id}"),
					types.InlineKeyboardButton(text = "Вперёд", callback_data = f"nextorder_{order_id}")
				],
				[
					types.InlineKeyboardButton(text = "Взять заказ", callback_data = f"in_process_order_{order_id}"),
					types.InlineKeyboardButton(text = "Закрыть заказ", callback_data= f"close_order_{order_id}_write-off_fromnew"),
					types.InlineKeyboardButton(text = "Закрыть без списания", callback_data = f"close_order_{order_id}_no-write-off_fromnew")
				],
				[
					types.InlineKeyboardButton(text = "Чат с заказчиком", url = f"tg://user?id={order_user_id}")	
				],
				[
					orderKeyboard.processed_orders_button,
					orderKeyboard.closed_orders_button
					
				]	
			]
		)
		await callback.message.edit_text(text=order_text, reply_markup=keyboard_next_prev)
	except AssertionError:
		await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("nextorder_") or callback.data.startswith("prevorder_"))        
async def next_prev_new_orders(callback: types.CallbackQuery):
	try:
			call_data = callback.data.split("_")
			direction = ">" if call_data[0] == "nextorder" else "<"
			det_func = "MAX" if direction == "<" else "MIN"
			call_order_id = call_data[1]

			query = """
			   WITH is_manager AS (
				SELECT 1 AS is_exists
				FROM Менеджеры
				WHERE id = ?
			), next_order AS (
				SELECT {det_func}(order_id) AS next_order_id
				FROM Заказы
				WHERE order_id {direction} ? AND order_in_process = 0 AND order_closed = 0
			)
			SELECT 
				o.order_id, 
				o.order_user_id, 
				o.order_user_name, 
				o.order_date, 
				k.Бренд, 
				k.Модель, 
				k.Размер, 
				k.Расцветка,
				(SELECT 1 FROM is_manager) AS is_manager,
				k.Количество,
				(SELECT COUNT(*) FROM Заказы WHERE model_id = o.model_id AND order_in_process = 1) AS orders_in_process_count
			FROM 
				Заказы o
			JOIN 
				Кроссовки k ON o.model_id = k.id
			WHERE 
				o.order_id = (SELECT next_order_id FROM next_order)
				
			""".format(det_func=det_func, direction=direction)
			
			result = await ASQL.execute(query, (callback.from_user.id, call_order_id))
			
			if not result:
				await callback.answer("Новых заказов нет")
				return
			
			is_manager = result[0][8]
			
			if is_manager != 1:
				return

			order_data = result[0]
			order_id = order_data[0]
			order_user_id = order_data[1]
			order_user_name = order_data[2]
			order_date = order_data[3]
			model_brand = order_data[4]
			model_name = order_data[5]
			model_size = order_data[6]
			model_color = order_data[7]
			model_count = order_data[9]
			orders_model_count = order_data[10]

			order_text = f'''
Заказ #{order_id}
Время создания - {order_date}
Заказчик - {order_user_name}

Бренд - {model_brand}
Модель - {model_name}
Размер - {model_size}
Расцветка - {model_color}
Количество на складе - {model_count}

Заказов в обработке с такой же моделью - {orders_model_count}
			'''
			print(order_text)

			keyboard_next_prev = types.InlineKeyboardMarkup(
				inline_keyboard=[
					[
						types.InlineKeyboardButton(text="Назад", callback_data=f"prevorder_{order_id}"),
						types.InlineKeyboardButton(text="Вперёд", callback_data=f"nextorder_{order_id}")
					],
					[
						types.InlineKeyboardButton(text = "Взять заказ", callback_data = f"in_process_order_{order_id}"),
						types.InlineKeyboardButton(text = "Закрыть заказ", callback_data= f"close_order_{order_id}_write-off"),
						types.InlineKeyboardButton(text = "Закрыть без списания", callback_data = f"close_order_{order_id}_no-write-off")
					],
					[
						types.InlineKeyboardButton(text="Чат с заказчиком", url=f"tg://user?id={order_user_id}")
					],
					[
						orderKeyboard.processed_orders_button,
						orderKeyboard.closed_orders_button
					]
				]
			)
			await callback.message.edit_text(text=order_text, reply_markup=keyboard_next_prev)
	finally:
		await callback.answer()
