# -*- coding: windows-1251 -*-
from aiogram import Router,types
from aiogram.filters import Command
from asql import ASQL

router = Router()

@router.message(Command('load_image'))
async def load_photo(message: types.Message):
	try:
		if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (message.from_user.id)))[0][0] != 1:
			return
		
		caption = message.caption.split(" ")[1:]  # �������� ������ � ���������������� ��� �������_�������_����������
		caption = " ".join(caption)
		photos = message.photo  # �������� ��� ����������
		print(len(photos))
		

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
		
@router.message(Command("getid"))
async def get_photo_id(message:types.Message):
    photo_id = message.photo[0].file_id
    message.reply(photo_id)
