# -*- coding: windows-1251 -*-
import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from asql import ASQL
from Bot.Keyboards import orderKeyboard

router = Router	(name = "processed_orders")

@router.callback_query(lambda callback: callback.data.startswith("to_processed_orders"))
async def show_processed_orders(callback: types.CallbackQuery):
	query = """
		SELECT 
			(SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id =?)) AS is_manager,
			o.order_id, o.order_user_id, o.order_user_name, o.order_date, k.Бренд, k.Модель, k.Размер, k.Расцветка, k.Количество,
			(SELECT COUNT(*) FROM Заказы WHERE model_id = o.model_id AND order_in_process = 1) AS orders_in_process_count, o.order_taken_by
		FROM 
			Заказы o
		JOIN 
			Кроссовки k ON o.model_id = k.id
		WHERE 
			o.order_in_process = 1 AND o.order_closed = 0 AND o.order_id = (SELECT MIN(order_id) FROM Заказы WHERE order_in_process = 1 AND order_closed = 0)
	"""
	try:
		result = (await ASQL.execute(query, (callback.from_user.id)))[0]
		print(result)
		is_manager = result[0]
		order_id = result[1]
		order_user_id = result[2]
		order_user_name = result[3]
		order_date = result[4]
		model_brand = result[5]
		model_name = result[6]
		model_size = result[7]
		model_color = result[8]
		model_count = result[9]
		orders_model_count = result[10] - 1
		order_taken_by = result[11]
		assert is_manager == 1
		order_taken_by = (await callback.bot.get_chat(order_taken_by)).username

		order_text = f'''
Заказ #{order_id}
Время создания - {order_date}
Заказчик - {order_user_name}

Бренд - {model_brand}
Модель - {model_name}
Размер - {model_size}
Расцветка - {model_color}
Количество на складе - {model_count}

Заказ взял : @{order_taken_by}
Заказов в обработке с такой же моделью - {orders_model_count}
		'''
		
		keyboard_next_prev = types.InlineKeyboardMarkup(
			inline_keyboard= [
				[
					types.InlineKeyboardButton(text = "Назад", callback_data = f"prevprocessedorder_{order_id}"),
					types.InlineKeyboardButton(text = "Вперёд", callback_data = f"nextprocessedorder_{order_id}")
				],
				[
					types.InlineKeyboardButton(text = "Закрыть заказ", callback_data= f"close_order_{order_id}_write-off"),
					types.InlineKeyboardButton(text = "Закрыть без списания", callback_data = f"close_order_{order_id}_no-write-off")
				],
				[
					types.InlineKeyboardButton(text = "Чат с заказчиком", url = f"tg://user?id={order_user_id}")	
				],
				[
					orderKeyboard.new_orders_button,
					orderKeyboard.closed_orders_button
				]
			]
		)
		await callback.message.edit_text(text=order_text, reply_markup=keyboard_next_prev)
	except AssertionError:
		await callback.answer()
		return
	except IndexError:
		await callback.answer("Заказы в обработке отсутствуют")
		return
	finally:
		await callback.answer()
		
@router.callback_query(lambda callback: callback.data.startswith("nextprocessedorder_") or callback.data.startswith("prevprocessedorder_"))        
async def next_prev_processed_orders(callback: types.CallbackQuery):
	try:
			call_data = callback.data.split("_")
			direction = ">" if call_data[0] == "nextprocessedorder" else "<"
			det_func = "MAX" if direction == "<" else "MIN"
			call_order_id = call_data[1]

			query = """
			   WITH is_manager AS (
				SELECT 1
				FROM Менеджеры
				WHERE id = ?
			), next_order AS (
				SELECT {det_func}(order_id) AS next_order_id
				FROM Заказы
				WHERE order_id {direction} ? AND order_in_process = 1
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
				(SELECT COUNT(*) FROM Заказы WHERE model_id = o.model_id AND order_in_process = 1) AS orders_in_process_count,
				o.order_taken_by
			FROM 
				Заказы o
			JOIN 
				Кроссовки k ON o.model_id = k.id
			WHERE 
				o.order_id = (SELECT next_order_id FROM next_order)
			""".format(det_func=det_func, direction=direction)
			result = await ASQL.execute(query, (callback.from_user.id, call_order_id))

			assert result[0][8] == 1

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
			order_taken_by = order_data[11]

			order_taken_by = (await callback.bot.get_chat(order_taken_by)).username
			order_text = f'''
Заказ #{order_id}
Время создания - {order_date}
Заказчик - {order_user_name}

Бренд - {model_brand}
Модель - {model_name}
Размер - {model_size}
Расцветка - {model_color}
Количество на складе - {model_count}

Заказ взял: @{order_taken_by} 
Заказов в обработке с такой же моделью - {orders_model_count}
			'''

			keyboard_next_prev = types.InlineKeyboardMarkup(
				inline_keyboard=[
					[
						types.InlineKeyboardButton(text="Назад", callback_data=f"prevprocessedorder_{order_id}"),
						types.InlineKeyboardButton(text="Вперёд", callback_data=f"nextprocessedorder_{order_id}")
					],
					[
						types.InlineKeyboardButton(text = "Закрыть заказ", callback_data= f"close_order_{order_id}_write-off"),
						types.InlineKeyboardButton(text = "Закрыть без списания", callback_data = f"close_order_{order_id}_no-write-off")
					],
					[
						types.InlineKeyboardButton(text="Чат с заказчиком", url=f"tg://user?id={order_user_id}")
					],
					[
						orderKeyboard.new_orders_button,
						orderKeyboard.closed_orders_button
					]
				]
			)
			await callback.message.edit_text(text=order_text, reply_markup=keyboard_next_prev)
	except AssertionError:
		pass
	except IndexError:
		await callback.answer("Заказы в обработке отсутствуют")
		return
	finally:
		await callback.answer()