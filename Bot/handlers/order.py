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
		await ASQL.execute("INSERT INTO ������ (model_id, order_user_id, order_date, order_user_name) VALUES (?,?,?,?)", (ordered_model_id, order_from_user_id, current_datetime, order_from_user_name))
	except Exception as order_create_error:
		await callback.answer(f"��������, ��� ��������� ������ ������ ��������� ������ : {order_create_error}", show_alert=True)
		return
	await callback.answer("������� �� �����!\n� ��������� ������� � ���� �������� ��� ��������", show_alert=True)
	all_managers = await ASQL.execute("SELECT id FROM ���������")
	for manager in all_managers:
		await callback.bot.send_message(text="������ ��� ��� �������� ����� �����.", chat_id=manager[0], parse_mode=ParseMode.MARKDOWN, reply_markup= await orderKeyboard.to_new_orders())
	

	await callback.answer()
	
@router.callback_query(lambda callback: callback.data == "to_new_orders")
async def show_new_orders(callback: types.CallbackQuery):
	try:
		order_data = await ASQL.execute("SELECT * FROM ������ WHERE order_closed = 0 AND order_in_proccess = 0 AND order_id = (SELECT MAX(order_id) FROM ������ WHERE order_closed = 0 AND order_in_proccess = 0)")
		
		order_data = order_data[0]
		order_model_id = order_data[0]
		order_id = order_data[1]
		order_user_id = order_data[2]
		order_user_name = order_data[3]
		order_date = order_data[4]
		
		model_data = await ASQL.execute("SELECT �����,������,������,��������� FROM ��������� WHERE id = ?", (order_model_id))
		
		model_data = model_data[0]
		model_brand = model_data[0]
		model_name = model_data[1]
		model_size = model_data[2]
		model_color = model_data[3]
		
		order_text = f'''
����� #{order_id}
����� �������� - {order_date}
�������� - {order_user_name}

����� - {model_brand}
������ - {model_name}
������ - {model_size}
��������� - {model_color}
		'''
		
		keyboard_next_prev = types.InlineKeyboardMarkup(
			inline_keyboard= [
				[
					types.InlineKeyboardButton(text = "�����", callback_data = f"prevorder_{order_id}"),
					types.InlineKeyboardButton(text = "�����", callback_data = f"nextorder_{order_id}")
				],
				[
					types.InlineKeyboardButton(text = "��� � ����������", url = f"tg://user?id={order_user_id}")	
				]
			]
		)
		await callback.message.edit_text(text=order_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_next_prev)
	except Exception as e:
		await callback.answer(f"������: {e}", show_alert=True)
        
@router.callback_query(lambda callback: callback.data.startswith("nextorder_") or callback.data.startswith("prevorder_"))
async def next_prev_order(callback: types.CallbackQuery):
	try:
		call_data = callback.data.split("_")
		direction = "<" if call_data[0] == "nextorder" else ">"
		t = "MAX" if direction == "<" else "MIN"
		call_order_id = call_data[1]
		print(call_order_id)
	
		order_id = await ASQL.execute(f"SELECT {t}(order_id) FROM ������ WHERE order_id {direction} ?", (call_order_id))
		order_id = order_id[0][0]
		order_data = await ASQL.execute(f"SELECT * FROM ������ WHERE order_id = ?", (order_id))
		order_data = order_data[0]
		order_model_id = order_data[0]
		order_user_id = order_data[2]
		order_user_name = order_data[3]
		order_date = order_data[4]
		
		model_data = await ASQL.execute("SELECT �����,������,������,��������� FROM ��������� WHERE id = ?", (order_model_id))
		
		model_data = model_data[0]
		model_brand = model_data[0]
		model_name = model_data[1]
		model_size = model_data[2]
		model_color = model_data[3]
		
		order_text = f'''
����� #{order_id}
����� �������� - {order_date}
�������� - {order_user_name}

����� - {model_brand}
������ - {model_name}
������ - {model_size}
��������� - {model_color}
		'''
		
		keyboard_next_prev = types.InlineKeyboardMarkup(
			inline_keyboard= [
				[
					types.InlineKeyboardButton(text = "�����", callback_data = f"prevorder_{order_id}"),
					types.InlineKeyboardButton(text = "�����", callback_data = f"nextorder_{order_id}")
				],
				[
					types.InlineKeyboardButton(text = "��� � ����������", url = f"tg://user?id={order_user_id}")	
				]
			]
		)
		await callback.message.edit_text(text=order_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_next_prev)
	except ValueError:
		await callback.answer(f"������: {e}", show_alert=True)
	
	

	

