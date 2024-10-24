# -*- coding: windows-1251 -*-
from aiogram import Router,types
from aiogram.filters import Command
from asql import ASQL

LEN_ONE_PHOTO = 4

router = Router()

@router.message(Command('load_image'))
async def load_photo(message: types.Message):
	try:
		if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
			return
		
		caption = message.caption.split(" ")[1:]  # Получить строку с идентификаторами или брендом_моделью_расцветкой
		caption = " ".join(caption)
		photos = message.photo  # Получить все фотографии
		
		if len(photos) != LEN_ONE_PHOTO:
			await message.answer("Нужно прикрепить только одну фотографию.")
			return

		# Проверить, является ли строка идентификаторами или брендом_моделью_расцветкой
		if "," in caption or caption.isdigit():
			# Обновить фотографии для каждой модели по идентификаторам
			for shoes_id, photo in zip(caption.split(","), photos):
				photo_id = photo.file_id
				await ASQL.execute("UPDATE Кроссовки SET Фото = ? WHERE id = ?", (photo_id, shoes_id))
		elif "_" in caption:
			# Обновить фотографии для каждой модели с таким же брендом, моделью и цветом
			for photo in photos:
				photo_id = photo.file_id
				brand, model, color = caption.split("_")[0:]
				print(photo_id , brand, model, color)
				await ASQL.execute("UPDATE Кроссовки SET Фото = ? WHERE Бренд IN (?) AND Модель IN (?) AND Расцветка IN (?)", (photo_id, brand, model, color))
		else:
			await message.answer("Неправильный формат строки.")
			return

		# Обработка загруженной фотографии
		await message.answer('Успешно загружено!')
	except AttributeError:
		await message.answer("Пожалуйста, прикрепите одну фотографию.")
	except RuntimeError as asql_error:
		await message.answer(text=asql_error)
