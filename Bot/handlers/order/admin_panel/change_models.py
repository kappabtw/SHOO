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
    isnew = State()
    quantity = State()
    size_quantity = State()
    check = State()
    original_callback = State()
    model_info = State()
    ids = State()
    finish = State()
    
field_column:dict = {
    "brand" : "�����",
    "model" : "������",
    "size" : "������",
    "price" : "����",
    "color" : "���������",
    "discount" : "������",
    "discountprice" : "��������� ����",
    "isnew": "�������" 
    }

@router.callback_query(StateFilter(None), lambda callback: callback.data.startswith("redactmodels_"))
async def start_change(callback: types.CallbackQuery, state: FSMContext):
    if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
        return
    await state.set_state(ChangeModel.start)
    
    data = callback.data.split("_")[1:]
    brand, model, color = data
    print(brand,model,color)

    await state.update_data(original_callback = callback.data)
    model_info = (await ASQL.execute("SELECT DISTINCT ����,������,\"��������� ����\",������� FROM ��������� WHERE ����� = ? AND ������ = ? AND ��������� = ?", (brand, model, color)))[0]
    ids = (await ASQL.execute("""
SELECT GROUP_CONCAT(id) AS ids
FROM ���������
WHERE ����� = ? AND ������ = ? AND ��������� = ?""", (brand, model, color)))[0]
    ids = list(map(int, ids[0].split(",")))
    
    print(ids)
    await state.update_data(ids = ids)
    model_info = {
        "�����":brand,
        "������":model,
        "���������":color,
        "����":model_info[0],
        "������":model_info[1],
        "��������� ����":model_info[2],
        "�������":model_info[3],
    } 
    
    await state.update_data(model_info = model_info)

    message_text = ""
    for key,value in model_info.items():
        message_text+= f"{key} : {value}\n"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[types.InlineKeyboardButton(text ="��������", callback_data=f"change_start")]])
    
    await callback.message.answer(message_text, reply_markup=keyboard)
    
@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data.startswith("change_start"))
async def change_start(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����", callback_data="change_brand"),
                types.InlineKeyboardButton(text = "������", callback_data="change_model"),
                types.InlineKeyboardButton(text = "���������", callback_data="change_color")
            ],
            [
                types.InlineKeyboardButton(text = "�������", callback_data="change_isnew"),
                types.InlineKeyboardButton(text = "����", callback_data="change_price"),
                types.InlineKeyboardButton(text = "������", callback_data="change_discount"),
            ],
            [
                types.InlineKeyboardButton(text = "���������", callback_data = "finish_change"),
                types.InlineKeyboardButton(text = "�������� ��", callback_data = "all_cancel")
            ],
        ]
    )
    
    data = (await state.get_data())["model_info"]
    data_text = ""
    for key,value in data.items():
        data_text+=f'{key}: {value}\n'

    await callback.message.answer(f"""    
{data_text}

���� [������] = 1, �� � �������� ������������ ������ ��������� ����
�������� ���� ��� ���������:                                  
""", reply_markup=keyboard)
    

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_isnew")
async def change_discount(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.isnew)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text = "��������", callback_data = "on_isnew")
            ],
        [
            types.InlineKeyboardButton(text = "���������", callback_data = "off_isnew")
            ]
        ])    

    await callback.message.answer("�������� �����", reply_markup= keyboard)

@router.callback_query(StateFilter(ChangeModel.isnew), lambda callback: callback.data == "on_isnew")
async def change_discount_price_on(callback : types.CallbackQuery, state : FSMContext):
    await state.update_data(new_value = 1)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_isnew"),
                types.InlineKeyboardButton(text = "������", callback_data=f"cancel_isnew"),
            ],
        ]
    )
    await callback.message.answer(f"�� ������ �������� ������� �� 1?", reply_markup=keyboard)
    

@router.callback_query(StateFilter(ChangeModel.isnew), lambda callback: callback.data == "off_isnew")
async def change_discount_price_off(callback : types.CallbackQuery, state : FSMContext):
    await state.update_data(new_value = 0)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_isnew"),
                types.InlineKeyboardButton(text = "������", callback_data=f"cancel_isnew"),
            ],
        ]
    )
    await callback.message.answer(f"�� ������ �������� ������� �� 0?", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_brand")
async def change_brand(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.brand)
    await callback.message.answer("������� ����� �������� ��� ������")

@router.message(StateFilter(ChangeModel.brand))
async def change_brand_value(message: types.Message, state: FSMContext):
    new_value = message.text
    if not new_value.isalpha():
        await message.answer("����������, ������� ��������� �������� ��� ������.")
        return
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_brand"),
                types.InlineKeyboardButton(text = "������", callback_data=f"cancel_brand"),
            ],
        ]
    )
    await message.answer(f"�� ������ �������� ����� �� {new_value}?", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_model")
async def change_model_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.model)
    await callback.message.answer("������� ����� �������� ��� ������")

@router.message(StateFilter(ChangeModel.model))
async def change_model_value(message: types.Message, state: FSMContext):
    new_value = message.text
    if not new_value.isalpha():
        await message.answer("����������, ������� ��������� �������� ��� ������.")
        return
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_model"),
                types.InlineKeyboardButton(text = "������", callback_data=f"cancel_model"),
            ],
        ]
    )
    await message.answer(f"�� ������ �������� ������ �� {new_value}?", reply_markup=keyboard)

@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_color")
async def change_color(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.color)
    await callback.message.answer("������� ����� �������� ��� ���������")

@router.message(StateFilter(ChangeModel.color))
async def change_color_value(message: types.Message, state: FSMContext):
    new_value = message.text
    if not new_value.isalpha():
        await message.answer("����������, ������� ��������� �������� ��� ���������.")
        return
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_color"),
                types.InlineKeyboardButton(text = "������", callback_data=f"cancel_color"),
            ],
        ]
    )
    await message.answer(f"�� ������ �������� ��������� �� {new_value}?", reply_markup=keyboard)


@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_price")
async def change_price(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.price)
    await callback.message.answer("������� ����� �������� ��� ����")

@router.message(StateFilter(ChangeModel.price))
async def change_price_value(message: types.Message, state: FSMContext):
    new_value = message.text
    if not new_value.replace('.', '', 1).replace(',', '', 1).isdigit():
        await message.answer("����������, ������� �������� �������� ��� ����.")
        return
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_price"),
                types.InlineKeyboardButton(text = "������", callback_data=f"cancel_price"),
            ],
        ]
    )
    await message.answer(f"�� ������ �������� ���� �� {new_value}?", reply_markup=keyboard)


@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data == "change_discount")
async def change_discount(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.discount)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text = "��������", callback_data = "on_discount")
            ],
        [
            types.InlineKeyboardButton(text = "���������", callback_data = "off_discount")
            ]
        ])    

    await callback.message.answer("�������� �����", reply_markup= keyboard)

@router.callback_query(StateFilter(ChangeModel.discount), lambda callback: callback.data == "on_discount")
async def change_discount_price_on(callback : types.CallbackQuery, state : FSMContext):
    await state.set_state(ChangeModel.discountprice)
    await callback.message.answer("������� ����� ��������� ����:")

@router.callback_query(StateFilter(ChangeModel.discount), lambda callback: callback.data == "off_discount")
async def change_discount_price_off(callback : types.CallbackQuery, state : FSMContext):
    await state.update_data(new_value = 0)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_discount"),
                    types.InlineKeyboardButton(text = "������", callback_data=f"cancel_discount"),
                ],
            ]
        )
    await callback.message.answer(f"�� ������ ������ ������?", reply_markup=keyboard)
    

@router.message(StateFilter(ChangeModel.discountprice))
async def change_discount_value(message: types.Message, state: FSMContext):
    new_value = message.text
    if not new_value.replace('.', '', 1).replace(',', '', 1).isdigit():
        await message.answer("����������, ������� �������� �������� ��� ��������� ����.")
        return
    await state.update_data(new_value=new_value)
    await state.set_state(ChangeModel.check)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = "�����������", callback_data=f"confirm_discountprice"),
                types.InlineKeyboardButton(text = "������", callback_data=f"cancel_discountprice"),
            ],
        ]
    )
    await message.answer(f"�� ������ �������� ��������� ���� �� {new_value}?", reply_markup=keyboard)
    
@router.callback_query(StateFilter(ChangeModel.check), lambda callback: callback.data.startswith("confirm_"))
async def confirm_change(callback: types.CallbackQuery, state: FSMContext):
    field = "_".join(callback.data.split("_")[1:])
    state_data = await state.get_data()
    new_value = state_data["new_value"]
    model_info = state_data["model_info"]
    print(field)
    if field == "discountprice":
        model_info["������"] = 1
    field = field_column[field]  
    model_info[field] = new_value
    await state.update_data(model_info=model_info)
    await state.set_state(ChangeModel.start)
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text = "����������", callback_data = "change_start")
            ],
        [
            types.InlineKeyboardButton(text = "���������", callback_data= "finish_change"),
            types.InlineKeyboardButton(text = "�������� ��", callback_data = "all_cancel")
            ]
        ])

    await callback.message.answer(f"���� {field} ������� �������� (��������) �� {new_value}!",
                                  reply_markup= keyboard)
    print(await state.get_data())

@router.callback_query(StateFilter(ChangeModel.check), lambda callback: callback.data.startswith("cancel_"))
async def cancel_change(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChangeModel.start)
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text = "����������", callback_data = "change_start")
            ]])
    await callback.message.answer("��������� ��������!", reply_markup=keyboard)
    
@router.callback_query(StateFilter(ChangeModel.start), lambda callback: callback.data == "finish_change")
async def finish_change(callback: types.CallbackQuery, state: FSMContext):
    if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
        return
    change_info = await state.get_data()
    model_info = change_info["model_info"]
    
    ids = change_info["ids"]
    print(ids)        
    # ��������� ������ � ���� ������ � ������� �� SQL-��������
    columns = ", ".join([f'\"{key}\" = ?' for key in model_info.keys()])
    values = list(model_info.values())  # Create a list of values
    placeholders = ', '.join(['?'] * len(ids))  # Create a string of ? placeholders for each ID
    await ASQL.execute(f"UPDATE ��������� SET {columns} WHERE id IN ({placeholders}) RETURNING ID", (*values, *ids))
    
    # ���������� ������������� ������������
    brand = model_info["�����"]
    model = model_info["������"]
    
    await state.clear()

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text = "�����", callback_data=f"modeladminpanel_{brand}_{model}")]])

    await callback.message.answer("��������� ������� ���������!", reply_markup= keyboard)
     
    
@router.callback_query(StateFilter(ChangeModel), lambda callback: callback.data.startswith("all_cancel"))
async def cancel_change(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    model_info = data['original_callback']
    data = model_info.split("_")[1:-1]
    brand, model = data
    print(brand,model)
    
    await state.clear()    

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text = "�����", callback_data=f"modeladminpanel_{brand}_{model}")]])
    
    await callback.message.answer("��������� ��������!", reply_markup=keyboard)                     
    