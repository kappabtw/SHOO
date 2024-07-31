# -*- coding: windows-1251 -*-
from aiogram.filters import Command
from aiogram import Router, types
from asql import ASQL
from Bot import data
from sqlite3 import IntegrityError


router = Router(name = 'admin')

@router.message(Command('load'))
async def load_photo(message: types.Message):
    is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (message.from_user.id))
    if is_manager[0][0] != 1:
        return
    shoes_id = message.caption.split(" ")[1]
    photo_id = message.photo[-1].file_id
    await ASQL.execute("UPDATE Кроссовки SET Фото = ? WHERE id = ?", (photo_id,shoes_id))

    # Обработка загруженной фотографии
    await message.answer('Фотография успешно загружена.')
    
@router.message(Command('add_manager'))
async def add_manager(message: types.Message):
    is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ? AND access = 1)", (message.from_user.id))
    if is_owner[0][0] != 1:
        return
    text:list = message.text.split(" ")
    if len(text) != 2:
        await message.answer(text = "Неверный аргумент")
        return
    new_username:str = text[1]
    new_id = await ASQL.execute("SELECT id FROM Пользователи WHERE username = ?",(new_username))
    new_id = new_id[0][0]
    if not new_id:                              
        await message.answer("Пользователь не найден. Возможно, что он ещё не зарегистрирован в базе данных нашего бота")
    try:
        await ASQL.execute("INSERT INTO Менеджеры (id, username) VALUES (?,?)", (new_id, new_username))
    except IntegrityError:      
        await message.answer(f"{new_username} уже является менеджером")
        return
    await message.answer(f"Успешно добавлен новый менеджер {new_username}")
    await message.bot.send_message(text = f"{new_username}, Вы были назначены на роль менеджера", chat_id = new_id)
    
@router.message(Command("del_manager"))
async def del_manager(message: types.Message):
    is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ? AND access = 1)", (message.from_user.id))
    if is_owner[0][0] != 1:
        return
    text:list = message.text.split(" ")
    if len(text) != 2:
        await message.answer(text = "Неверный аргумент")
        return
    username_to_delete = text[1]
    id_manager_to_delete = await ASQL.execute("SELECT id FROM Менеджеры WHERE username = ?",(username_to_delete))
    if not id_manager_to_delete:                              
        await message.answer(f"Менеджер \"{username_to_delete}\" не найден. Возможно, что вы ввели неверный username")
        return
    if username_to_delete == f"@{message.from_user.username}":
        await message.answer(text = "Вы не можете удалить самого себя!")
        return
    print(username_to_delete)
    
    await ASQL.execute("DELETE FROM Менеджеры WHERE username = ?", (username_to_delete))
    await message.answer(text = f"{username_to_delete} был удалён из списка менеджеров!")
    await message.bot.send_message(text = f"{username_to_delete}, Вы были удалены из списка менеджеров", chat_id = id_manager_to_delete[0][0])

#@router.message(Command("op"))
async def op(message: types.Message):
    await ASQL.execute("INSERT INTO Менеджеры (id, username, access) VALUES (?,?, 1)",(message.from_user.id, f"@{message.from_user.username}"))
    
    
