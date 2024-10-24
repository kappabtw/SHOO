# -*- coding: windows-1251 -*-
from aiogram import Router,types
from aiogram.filters import Command
from asql import ASQL

LEN_ONE_PHOTO = 4

router = Router()

@router.message(Command('load_image'))
async def load_photo(message: types.Message):
	try:
		if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
			return
		
		caption = message.caption.split(" ")[1:]  # �������� ������ � ���������������� ��� �������_�������_����������
		caption = " ".join(caption)
		photos = message.photo  # �������� ��� ����������
		
		if len(photos) != LEN_ONE_PHOTO:
			await message.answer("����� ���������� ������ ���� ����������.")
			return

		# ���������, �������� �� ������ ���������������� ��� �������_�������_����������
		if "," in caption or caption.isdigit():
			# �������� ���������� ��� ������ ������ �� ���������������
			for shoes_id, photo in zip(caption.split(","), photos):
				photo_id = photo.file_id
				await ASQL.execute("UPDATE ��������� SET ���� = ? WHERE id = ?", (photo_id, shoes_id))
		elif "_" in caption:
			# �������� ���������� ��� ������ ������ � ����� �� �������, ������� � ������
			for photo in photos:
				photo_id = photo.file_id
				brand, model, color = caption.split("_")[0:]
				print(photo_id , brand, model, color)
				await ASQL.execute("UPDATE ��������� SET ���� = ? WHERE ����� IN (?) AND ������ IN (?) AND ��������� IN (?)", (photo_id, brand, model, color))
		else:
			await message.answer("������������ ������ ������.")
			return

		# ��������� ����������� ����������
		await message.answer('������� ���������!')
	except AttributeError:
		await message.answer("����������, ���������� ���� ����������.")
	except RuntimeError as asql_error:
		await message.answer(text=asql_error)
