# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asql import ASQL


router = Router()

class ChangeModel(StatesGroup):
    start = State()
    brand = State()
    model = State()
    size = State()
    price = State()
    color = State()
    discount = State()
    discountprice = State()
    is_new = State()
    quantity = State()
    size_quantity = State()
    check = State()
    original_callback = State()
    model_info = State()
    finish = State()
    
field_column:dict = {
    "brand" : "Бренд",
    "model" : "Модель",
    "size" : "Размер",
    "price" : "Цена",
    "color" : "Расцветка",
    "discount" : "Скидка",
    "discountprice" : "Скидочная цена",
    "is_new": "Новинка" 
    }

@router.callback_query(StateFilter(None), lambda callback: callback.data.startswith("redactmodels_"))
async def start_change(callback: types.CallbackQuery, state: FSMContext):
    if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM Менеджеры WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
        return
    id = list(map(int, callback.data.split("_")[1].split(",")))[0]
    await state.set_state(ChangeModel.start)
    await state.update_data(original_callback = callback.data)
    model_info = (await ASQL.execute("SELECT Бренд,Модель,Расцветка,Цена,Скидка,\"Скидочная цена\",Новинка FROM Кроссовки WHERE id = ?", (id)))[0]
    
    model_info = {
        "Бренд":model_info[0],
        "Модель":model_info[1],
        "Расцветка":model_info[2],
        "Цена":model_info[3],
        "Скидка":model_info[4],
        "Скидочная цена":model_info[5],
        "Новинка":model_info[6],
    } 
    
    await state.update_data(model_info = model_info)

    message_text = ""
    for key,value in model_info.items():
        message_text+= f"{key} : {value}\n"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[types.InlineKeyboardButton(text ="Изменить", callback_data=f"change_start")]])
    
    await callback.message.answer(message_text, reply_markup=keyboard)
    
@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data.startswith("change_start"))
async def change_start(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "Бренд", callback_data="change_brand"),
                types.InlineKeyboardButton(text = "Модель", callback_data="change_model"),
            ],
            [
                types.InlineKeyboardButton(text = "Расцветка", callback_data="change_color"),
                types.InlineKeyboardButton(text = "Цена", callback_data="change_price"),
                types.InlineKeyboardButton(text = "Скидка", callback_data="change_discount"),
            ],
            [
                types.InlineKeyboardButton(text = "Сохранить", callback_data = "finish_change"),
                types.InlineKeyboardButton(text = "Отменить всё", callback_data = "all_cancel")
            ],
        ]
    )
    await callback.message.answer("Выберите поле для изменения:", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_brand")
async def change_brand(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.brand)
    await callback.message.answer("Введите новое значение для Бренда")

@router.message(StateFilter(ChangeModel.brand))
async def change_brand_value(message: types.Message, state: FSMContext):
    new_value = message.text
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "Подтвердить", callback_data=f"confirm_brand"),
                types.InlineKeyboardButton(text = "Отмена", callback_data=f"cancel_brand"),
            ],
        ]
    )
    await message.answer(f"Вы хотите изменить Бренд на {new_value}?", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_model")
async def change_model_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.model)
    await callback.message.answer("Введите новое значение для Модели")

@router.message(StateFilter(ChangeModel.model))
async def change_model_value(message: types.Message, state: FSMContext):
    new_value = message.text
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "Подтвердить", callback_data=f"confirm_model"),
                types.InlineKeyboardButton(text = "Отмена", callback_data=f"cancel_model"),
            ],
        ]
    )
    await message.answer(f"Вы хотите изменить Модель на {new_value}?", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_color")
async def change_color(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.color)
    await callback.message.answer("Введите новое значение для Расцветки")

@router.message(StateFilter(ChangeModel.color))
async def change_color_value(message: types.Message, state: FSMContext):
    new_value = message.text
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "Подтвердить", callback_data=f"confirm_color"),
                types.InlineKeyboardButton(text = "Отмена", callback_data=f"cancel_color"),
            ],
        ]
    )
    await message.answer(f"Вы хотите изменить Расцветку на {new_value}?", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_price")
async def change_price(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.price)
    await callback.message.answer("Введите новое значение для Цены")

@router.message(StateFilter(ChangeModel.price))
async def change_price_value(message: types.Message, state: FSMContext):
    new_value = message.text
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "Подтвердить", callback_data=f"confirm_price"),
                types.InlineKeyboardButton(text = "Отмена", callback_data=f"cancel_price"),
            ],
        ]
    )
    await message.answer(f"Вы хотите изменить Цену на {new_value}?", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_discount")
async def change_discount(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.discount)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text = "Включить", callback_data = "on_discount")
            ],
        [
            types.InlineKeyboardButton(text = "Выключить", callback_data = "off_discount")
            ]
        ])    

    await callback.message.answer("Выберите опцию", reply_markup= keyboard)

@router.callback_query(StateFilter(ChangeModel.discount), lambda callback: callback.data == "on_discount")
async def change_discount_price_on(callback : types.CallbackQuery, state : FSMContext):
    await state.set_state(ChangeModel.discountprice)
    await callback.message.answer("Введите новую скидочную цену:")

@router.callback_query(StateFilter(ChangeModel.discount), lambda callback: callback.data == "off_discount")
async def change_discount_price_off(callback : types.CallbackQuery, state : FSMContext):
    await state.update_data(new_value = 0)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text = "Подтвердить", callback_data=f"confirm_discount"),
                    types.InlineKeyboardButton(text = "Отмена", callback_data=f"cancel_discount"),
                ],
            ]
        )
    await callback.message.answer(f"Вы хотите убрать скидку?", reply_markup=keyboard)
    

@router.message(StateFilter(ChangeModel.discountprice))
async def change_discount_value(message: types.Message, state: FSMContext):
    new_value = message.text
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "Подтвердить", callback_data=f"confirm_discountprice"),
                types.InlineKeyboardButton(text = "Отмена", callback_data=f"cancel_discountprice"),
            ],
        ]
    )
    await message.answer(f"Вы хотите изменить Скидочную цену на {new_value}?", reply_markup=keyboard)
    
@router.callback_query(StateFilter(ChangeModel.check), lambda callback: callback.data.startswith("confirm_"))
async def confirm_change(callback: types.CallbackQuery, state: FSMContext):
    field = "_".join(callback.data.split("_")[1:])
    state_data = await state.get_data()
    new_value = state_data["new_value"]
    model_info = state_data["model_info"]
    print(field)
    if field == "discountprice":
        print("OIEFOWEINFOINEWOFINFOWIENF")
        model_info["Скидка"] = 1
    field = field_column[field]  
    model_info[field] = new_value
    await state.update_data(model_info=model_info)
    await state.set_state(ChangeModel.start)
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text = "Продолжить", callback_data = "change_start")
            ],
        [
            types.InlineKeyboardButton(text = "Сохранить", callback_data= "finish_change"),
            types.InlineKeyboardButton(text = "Отменить всё", callback_data = "all_cancel")
            ]
        ])

    await callback.message.answer(f"Поле {field} успешно изменено (локально) на {new_value}!",
                                  reply_markup= keyboard)
    print(await state.get_data())

@router.callback_query(StateFilter(ChangeModel.check), lambda callback: callback.data.startswith("cancel_"))
async def cancel_change(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.start)
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text = "Продолжить", callback_data = "change_start")
            ]])
    await callback.message.answer("Изменение отменено!", reply_markup=keyboard)
    
@router.callback_query(StateFilter(ChangeModel.start), lambda callback: callback.data == "finish_change")
async def finish_change(callback: types.CallbackQuery, state: FSMContext):
    change_info = await state.get_data()
    model_info = change_info["model_info"]
    original_callback = change_info["original_callback"]
    ids = list(map(int, original_callback.split("_")[1].split(",")))
    
    # Обновляем данные в базе данных с защитой от SQL-инъекций
    columns = ", ".join([f'\"{key}\" = ?' for key in model_info.keys()])
    values = list(model_info.values())  # Create a list of values
    placeholders = ', '.join(['?'] * len(ids))  # Create a string of ? placeholders for each ID
    await ASQL.execute(f"UPDATE Кроссовки SET {columns} WHERE id IN ({placeholders}) RETURNING ID", (*values, *ids))
    print(ids)
    
    # Отправляем подтверждение пользователю
    await callback.message.answer("Изменения успешно сохранены!")
    
    # Очищаем состояние
    await state.update_data()
    await state.clear()   
                       
    