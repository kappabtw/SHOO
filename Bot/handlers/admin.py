# -*- coding: windows-1251 -*-
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Router, types
from asql import ASQL
from sqlite3 import IntegrityError


router = Router(name = 'admin')
    
@router.message(Command('addmanager'))
async def add_manager(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ? AND access = 1)", (message.from_user.id))
        if is_owner[0][0] != 1:
            return
        text:list = message.text.split(" ")
        if len(text) != 2:
            await message.reply(text = "Неверный аргумент")
            return
        new_username:str = text[1]
        new_id = await ASQL.execute("SELECT id FROM Пользователи WHERE username = ?",(new_username))
        if not new_id:                              
            await message.reply("Пользователь не найден. Возможно, что он ещё не зарегистрирован в базе данных нашего бота")
            return
        new_id = new_id[0][0]
        try:
            await ASQL.execute("INSERT INTO Менеджеры (id, username) VALUES (?,?)", (new_id, new_username))
        except IntegrityError:      
            await message.reply(f"{new_username} уже является менеджером")
            return
        await message.reply(f"Успешно добавлен новый менеджер {new_username}")
        await message.bot.send_message(text = f"{new_username}, Вы были назначены на роль менеджера", chat_id = new_id)
    except Exception as handler_exception:
        await message.reply(f"Произошла ошибка при обработке запроса `/add_manager {new_username} : {handler_exception} `", parse_mode= ParseMode.MARKDOWN)
    
@router.message(Command("delmanager"))
async def del_manager(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id =? AND access = 1)", (message.from_user.id))
        if is_owner[0][0] != 1:
            return
        text: list = message.text.split(" ")
        target = text[1]
        if target.startswith("@"):
            username_to_delete = target
            id_manager_to_delete = await ASQL.execute("SELECT id FROM Менеджеры WHERE username =?", (username_to_delete))
        else:
            try:
                id_manager_to_delete = int(target)
            except ValueError:
                await message.reply(text="Неверный аргумент")
                return
        if not id_manager_to_delete:
            await message.reply(text=f"Менеджер не найден")
            return
        if username_to_delete == f"@{message.from_user.username}" or id_manager_to_delete == message.from_user.id:
            await message.reply(text="Вы не можете удалить самого себя!")
            return
        
        await ASQL.execute("DELETE FROM Менеджеры WHERE id =?", (id_manager_to_delete[0][0]))
    except Exception as handler_exception:
        await message.reply(f"Произошла ошибка при обработке запроса `/del_manager {target} : {handler_exception} `", parse_mode=ParseMode.MARKDOWN)
    await message.reply(text=f"Менеджер с ID {id_manager_to_delete[0][0]} был удалён из списка менеджеров!")
    await message.bot.send_message(text=f"Вы были удалены из списка менеджеров", chat_id=id_manager_to_delete[0][0])
    
@router.message(Command("del_all_managers"))
async def delete_all_managers(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ? AND access = 1)", (message.from_user.id))
        if is_owner[0][0] != 1:
            return
        all_managers = await ASQL.execute("SELECT id FROM Менеджеры WHERE access = 0")
        await ASQL.execute("DELETE FROM Менеджеры WHERE access = 0")
        await message.reply("Все менеджеры были успешно удалены")
        for manager in all_managers:
            await message.bot.send_message(text = f"Вы были удалены из списка менеджеров", chat_id = manager[0])
    except Exception as handler_exception:
        await message.reply(f"Произошла ошибка при обработке запроса `/delete_all_managers : {handler_exception} `", parse_mode= ParseMode.MARKDOWN)

@router.message(Command("show_managers"))       
async def show_managers(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ? AND access = 1)", (message.from_user.id))
        if is_owner[0][0] != 1:
            return
        all_managers = await ASQL.execute("SELECT * FROM Менеджеры WHERE access = 0"                                  )
        text = "Список менеджеров [username|userid]:\n"
        print(all_managers)
        for manager in all_managers:
            text+= f"{manager[1]}|{manager[0]}\n\n"
        await message.answer(text = text)
    except Exception as handler_error:
        await message.reply(text = f"При обработке вашего запроса произошла ошибка : `{handler_error}`", parse_mode = ParseMode.MARKDOWN)
    
    

#@router.message(Command("op"))
#async def op(message: types.Message):
#    await ASQL.execute("INSERT INTO Менеджеры (id, username, access) VALUES (?,?, 1)",(message.from_user.id, f"@{message.from_user.username}"))
    
   

