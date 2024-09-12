# -*- coding: windows-1251 -*-                              
from aiogram import Router,types
from aiogram.filters import Command
from asql import ASQL

router = Router()

@router.message(Command("del_model"))
async def del_model_from_bd(message: types.Message):
    try:
        is_manager = (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (message.from_user.id)))[0][0]
        if not is_manager:
            return
        
        text = message.text.split(" ")[1:]
        text = " ".join(text)
        

        if "," in text or text.isdigit():
            ids = [int(x) for x in text.split(",")]
            # ���������, ���������� �� ������ � ����� ����������������
            exist_ids = await ASQL.execute("SELECT 1 FROM ��������� WHERE id IN ({})".format(','.join(['?']*len(ids))), (ids))
            if exist_ids:
                # ���� ������ ����������, ������� ��
                await ASQL.execute(f"DELETE FROM ��������� WHERE id IN ({','.join(['?']*len(ids))})", (ids))
                await message.answer("������ �������")
            else:
                await message.answer("����� � ����� ���������������� �� �������")

        elif "_" in text:
            brand, model, color = text.split("_")[0:]
            print(brand,model,color)
            # ���������, ���������� �� ������ � ����� �����������
            exist_params = await ASQL.execute("SELECT 1 FROM ��������� WHERE ����� IN (?) AND ������ IN (?) AND ��������� IN (?)", (brand, model, color))
            if exist_params:
                # ���� ������ ����������, ������� ��
                await ASQL.execute("DELETE FROM ��������� WHERE ����� IN (?) AND ������ IN (?) AND ��������� IN (?)", (brand, model, color))
                await message.answer("������ �������")
            else:
                await message.answer("����� � ����� ����������� �� �������")
        

    except AttributeError and ValueError:
        await message.answer("�������� ����")
    except RuntimeError as asql_error:
        await message.answer(text=asql_error)   
