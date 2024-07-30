from aiogram.filters import Command
from aiogram import Router, types
from asql import ASQL
from Bot import data


router = Router(name = 'admin')

@router.message(Command('load'))
async def load_photo(message: types.Message):
    shoes_id = message.caption.split(" ")[1]
    photo_id = message.photo[-1].file_id
    await ASQL.execute("UPDATE Кроссовки SET Фото = ? WHERE id = ?", (photo_id,shoes_id))

    # Обработка загруженной фотографии
    await message.answer('Фотография успешно загружена.')
