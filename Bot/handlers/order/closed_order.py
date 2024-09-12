# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.enums import ParseMode
from asql import ASQL
from Bot.Keyboards import orderKeyboard

router = Router	(name = "closed_orders")

@router.callback_query(lambda callback: callback.data.startswith("to_closed_orders"))
async def show_closed_orders(callback: types.CallbackQuery):
	query = """
		SELECT 
			(SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id =?)) AS is_manager,
			o.order_id, o.order_user_id, o.order_user_name, o.order_date, k.Бренд, k.Модель, k.Размер, k.Расцветка,o.order_closed_date, o.order_closed_by, o.order_closed_write_off,
			o.order_taken_by
		FROM 
			Заказы o
		JOIN 
			Кроссовки k ON o.model_id = k.id
		WHERE 
			o.order_closed = 1 AND o.order_id = (SELECT MAX(order_id) FROM Заказы WHERE order_closed = 1)
	"""
	try:
		result = await ASQL.execute(query, (callback.from_user.id))
		print(result)
		is_manager = result[0][0]
		order_id = result[0][1]
		order_user_id = result[0][2]
		order_user_name = result[0][3]
		order_date = result[0][4]
		model_brand = result[0][5]
		model_name = result[0][6]
		model_size = result[0][7]
		model_color = result[0][8]
		order_closed_date = result[0][9]
		order_closed_by = result[0][10]
		order_write_off = result[0][11]
		order_taken_by = result[0][12]
		
		order_taken_by = (await callback.bot.get_chat(order_taken_by)).username
		order_closed_by = (await callback.bot.get_chat(order_closed_by)).username
		assert is_manager == 1

		order_text = f'''
Заказ #{order_id}
Время создания - {order_date}
Заказчик - {order_user_name}

Бренд - {model_brand}
Модель - {model_name}
Размер - {model_size}
Расцветка - {model_color}

Время закрытия заказа - {order_closed_date}
Взял : @{order_taken_by}
Закрыл : @{order_closed_by}
Списано: {'да' if order_write_off else 'нет'}
		'''
		
		keyboard_next_prev = types.InlineKeyboardMarkup(
			inline_keyboard= [
				[
					types.InlineKeyboardButton(text = "Назад", callback_data = f"prevclosedorder_{order_id}"),
					types.InlineKeyboardButton(text = "Вперёд", callback_data = f"nextclosedorder_{order_id}")
				],
				[
					types.InlineKeyboardButton(text = "Чат с заказчиком", url = f"tg://user?id={order_user_id}")	
				],
				[
					orderKeyboard.new_orders_button,
					orderKeyboard.processed_orders_button
				],
				[
					types.InlineKeyboardButton(text = "К меню", callback_data = "adminpanel")
					]
			]
		)
		await callback.message.edit_text(text=order_text, reply_markup=keyboard_next_prev)
	except AssertionError:
		await callback.answer()
	except IndexError:
		await callback.answer("Закрытые заказы отсутствуют")
		return
	finally:
		await callback.answer()
		
@router.callback_query(lambda callback: callback.data.startswith("nextclosedorder_") or callback.data.startswith("prevclosedorder_"))        
async def next_prev_closed_orders(callback: types.CallbackQuery):
	try:
			call_data = callback.data.split("_")
			direction = "<" if call_data[0] == "nextclosedorder" else ">"
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
				WHERE order_id {direction} ? AND order_closed = 1
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
				o.order_closed_date,
				o.order_closed_by,
				o.order_closed_write_off,
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
			order_closed_date = order_data[9]
			order_closed_by = order_data[10]
			order_write_off = order_data[11]
			order_taken_by = order_data[12]
			
			order_taken_by = (await callback.bot.get_chat(order_taken_by)).username
			order_closed_by = (await callback.bot.get_chat(order_closed_by)).username

			order_text = f'''
Заказ #{order_id}
Время создания - {order_date}
Заказчик - {order_user_name}

Бренд - {model_brand}
Модель - {model_name}
Размер - {model_size}
Расцветка - {model_color}

Время закрытия заказа - {order_closed_date}
Взял: @{order_taken_by}
Закрыл : @{order_closed_by}
Списано: {'да' if order_write_off else 'нет'}
			'''

			keyboard_next_prev = types.InlineKeyboardMarkup(
				inline_keyboard=[
					[
						types.InlineKeyboardButton(text="Назад", callback_data=f"prevclosedorder_{order_id}"),
						types.InlineKeyboardButton(text="Вперёд", callback_data=f"nextclosedorder_{order_id}")
					],
					[
						types.InlineKeyboardButton(text="Чат с заказчиком", url=f"tg://user?id={order_user_id}")
					],
					[
						orderKeyboard.new_orders_button,
						orderKeyboard.processed_orders_button
					],
					[
						types.InlineKeyboardButton(text = "К меню", callback_data = "adminpanel")
					]
				]
			)
			await callback.message.edit_text(text=order_text, reply_markup=keyboard_next_prev)
	except AssertionError:
		pass
	except IndexError:
		pass
	finally:
		await callback.answer()



