# -*- coding: windows-1251 -*-
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Router, types
from asql import ASQL
from sqlite3 import IntegrityError


router = Router(name = 'admin')

@router.message(Command('load'))
async def load_photo(message: types.Message):
    try:
        is_manager = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (message.from_user.id))
        assert is_manager[0][0] == 1
        shoes_id = message.caption.split(" ")[1]
        photo_id = message.photo[-1].file_id
        await ASQL.execute("UPDATE ��������� SET ���� = ? WHERE id = ?", (photo_id,shoes_id))

        # ��������� ����������� ����������
        await message.answer('���������� ������� ���������.')
    except AssertionError:
        pass
    except RuntimeError as handler_error:
       await message.answer(text = handler_error)
    
@router.message(Command('add_manager'))
async def add_manager(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ? AND access = 1)", (message.from_user.id))
        assert is_owner[0][0] == 1
        text:list = message.text.split(" ")
        if len(text) != 2:
            await message.reply(text = "�������� ��������")
            return
        new_username:str = text[1]
        new_id = await ASQL.execute("SELECT id FROM ������������ WHERE username = ?",(new_username))
        if not new_id:                              
            await message.reply("������������ �� ������. ��������, ��� �� ��� �� ��������������� � ���� ������ ������ ����")
            return
        new_id = new_id[0][0]
        try:
            await ASQL.execute("INSERT INTO ��������� (id, username) VALUES (?,?)", (new_id, new_username))
        except IntegrityError:      
            await message.reply(f"{new_username} ��� �������� ����������")
            return
        await message.reply(f"������� �������� ����� �������� {new_username}")
        await message.bot.send_message(text = f"{new_username}, �� ���� ��������� �� ���� ���������", chat_id = new_id)
    except AssertionError:
        pass
    except Exception as handler_exception:
        await message.reply(f"��������� ������ ��� ��������� ������� `/add_manager {new_username} : {handler_exception} `", parse_mode= ParseMode.MARKDOWN)
    
@router.message(Command("del_manager"))
async def del_manager(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id =? AND access = 1)", (message.from_user.id))
        assert is_owner[0][0] == 1
        text: list = message.text.split(" ")
        target = text[1]
        if target.startswith("@"):
            username_to_delete = target
            id_manager_to_delete = await ASQL.execute("SELECT id FROM ��������� WHERE username =?", (username_to_delete))
        else:
            try:
                id_manager_to_delete = int(target)
            except ValueError:
                await message.reply(text="�������� ��������")
                return
        if not id_manager_to_delete:
            await message.reply(text=f"�������� �� ������")
            return
        if username_to_delete == f"@{message.from_user.username}" or id_manager_to_delete == message.from_user.id:
            await message.reply(text="�� �� ������ ������� ������ ����!")
            return
        
        await ASQL.execute("DELETE FROM ��������� WHERE id =?", (id_manager_to_delete[0][0]))
    except Exception as handler_exception:
        await message.reply(f"��������� ������ ��� ��������� ������� `/del_manager {target} : {handler_exception} `", parse_mode=ParseMode.MARKDOWN)
    await message.reply(text=f"�������� � ID {id_manager_to_delete[0][0]} ��� ����� �� ������ ����������!")
    await message.bot.send_message(text=f"�� ���� ������� �� ������ ����������", chat_id=id_manager_to_delete[0][0])
    
@router.message(Command("del_all_managers"))
async def delete_all_managers(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ? AND access = 1)", (message.from_user.id))
        assert is_owner[0][0] == 1
        all_managers = await ASQL.execute("SELECT id FROM ��������� WHERE access = 0")
        await ASQL.execute("DELETE FROM ��������� WHERE access = 0")
        await message.reply("��� ��������� ���� ������� �������")
        for manager in all_managers:
            await message.bot.send_message(text = f"�� ���� ������� �� ������ ����������", chat_id = manager[0])
    except AssertionError:
        pass
    except Exception as handler_exception:
        await message.reply(f"��������� ������ ��� ��������� ������� `/delete_all_managers : {handler_exception} `", parse_mode= ParseMode.MARKDOWN)

@router.message(Command("show_managers"))       
async def show_managers(message: types.Message):
    try:
        is_owner = await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ? AND access = 1)", (message.from_user.id))
        assert is_owner[0][0] == 1
        all_managers = await ASQL.execute("SELECT * FROM ��������� WHERE access = 0")
        text = "������ ���������� [username|userid]:\n"
        print(all_managers)
        for manager in all_managers:
            text+= f"{manager[1]}|{manager[0]}\n\n"
        await message.answer(text = text)
    except AssertionError:
        pass
    except Exception as handler_error:
        await message.reply(text = f"��� ��������� ������ ������� ��������� ������ : `{handler_error}`", parse_mode = ParseMode.MARKDOWN)
    
    

#@router.message(Command("op"))
async def op(message: types.Message):
    await ASQL.execute("INSERT INTO ��������� (id, username, access) VALUES (?,?, 1)",(message.from_user.id, f"@{message.from_user.username}"))
    
    
