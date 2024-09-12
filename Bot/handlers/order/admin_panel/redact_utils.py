# -*- coding: windows-1251 -*-                              
from aiogram import Router,types
from aiogram.filters import Command
from asql import ASQL

router = Router()

@router.message(Command("del_model"))
async def del_model_from_bd(message: types.Message):
    try:
        is_manager = (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (message.from_user.id)))[0][0]
        if not is_manager:
            return
        
        text = message.text.split(" ")[1:]
        text = " ".join(text)
        

        if "," in text or text.isdigit():
            ids = [int(x) for x in text.split(",")]
            # Проверяем, существуют ли строки с этими идентификаторами
            exist_ids = await ASQL.execute("SELECT 1 FROM Кроссовки WHERE id IN ({})".format(','.join(['?']*len(ids))), (ids))
            if exist_ids:
                # Если строки существуют, удаляем их
                await ASQL.execute(f"DELETE FROM Кроссовки WHERE id IN ({','.join(['?']*len(ids))})", (ids))
                await message.answer("Строки удалены")
            else:
                await message.answer("Строк с этими идентификаторами не найдено")

        elif "_" in text:
            brand, model, color = text.split("_")[0:]
            print(brand,model,color)
            # Проверяем, существуют ли строки с этими параметрами
            exist_params = await ASQL.execute("SELECT 1 FROM Кроссовки WHERE Бренд IN (?) AND Модель IN (?) AND Расцветка IN (?)", (brand, model, color))
            if exist_params:
                # Если строки существуют, удаляем их
                await ASQL.execute("DELETE FROM Кроссовки WHERE Бренд IN (?) AND Модель IN (?) AND Расцветка IN (?)", (brand, model, color))
                await message.answer("Строки удалены")
            else:
                await message.answer("Строк с этими параметрами не найдено")
        

    except AttributeError and ValueError:
        await message.answer("Неверный ввод")
    except RuntimeError as asql_error:
        await message.answer(text=asql_error)   
