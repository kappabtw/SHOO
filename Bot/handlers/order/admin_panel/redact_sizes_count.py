# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asql import ASQL

router = Router()

class SizesEditor(StatesGroup):
    show_info = State()
    redact_sizes = State()
    redact_quantities = State()
    wait_for_new_quantity = State()
    confirm_quantity = State()
    wait_for_new_size = State()
    confirm_size = State()
    wait_for_add_size = State()
    confirm_addsize = State()

@router.callback_query(lambda callback_query: callback_query.data.startswith("redactsizes_"))
async def edit_sizes(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")   
    brand = data[1]
    model = data[2]
    color = data[3]
    
    await state.update_data(brand = brand , model = model , color = color)

    data = await ASQL.execute("SELECT ������, ����������, id FROM ��������� WHERE ����� = ? AND ������ = ? AND ��������� = ?", (brand, model, color))    
    print(data)
    
    model_data = {}
    sizes = ""
    
    for block in data:
        model_data[str(block[2])] = {"������" : block[0], "����������" : block[1]}
        sizes+=f"{block[0]} - {block[1]}\n"
        
    text = f"{brand} {model} {color}\n������ - ����������\n{sizes}"
    
    await state.update_data(model_data = model_data)
         
    print(model_data)
        

    await state.set_state(SizesEditor.show_info)
    await callback_query.message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text = "��������", callback_data= "sizeschange")]]))
    
@router.callback_query(lambda callback_query: callback_query.data == "sizeschange")
async def change_sizes(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    model_data = data["model_data"]

    sizes_list = ""
    for key, value in model_data.items():
        sizes_list += f"ID: {key}, ������: {value['������']}, ����������: {value['����������']}\n"

    inline_keyboard = [
        [types.InlineKeyboardButton(text="�������� ������", callback_data="add_size")],
    ]
    for key in model_data.keys():
        inline_keyboard.append([types.InlineKeyboardButton(text=f"������� {key}", callback_data=f"select_id_{key}")])

    inline_keyboard.append([
        types.InlineKeyboardButton(text = "���������", callback_data = "savesizes"),
        types.InlineKeyboardButton(text = "�������� ��", callback_data = "cancelsizes")
    ])

    await callback_query.message.answer(sizes_list, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
    
@router.callback_query(lambda callback_query: callback_query.data.startswith("select_id_"))
async def show_id_info(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    model_data = data["model_data"]
    id = callback_query.data.split("_")[2]

    size_info = model_data[id]
    text = f"ID: {id}\n������: {size_info['������']}\n����������: {size_info['����������']}"

    inline_keyboard = [
        [types.InlineKeyboardButton(text="�������� ������", callback_data=f"change_size_{id}")],
        [types.InlineKeyboardButton(text="�������� ����������", callback_data=f"change_quantity_{id}")],
        [types.InlineKeyboardButton(text="�������", callback_data=f"delete_size_{id}")],
        [types.InlineKeyboardButton(text="�����", callback_data="sizeschange")]
        
    ]

    await callback_query.message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
    
@router.callback_query(lambda callback_query: callback_query.data.startswith("change_quantity_"))
async def ask_for_new_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    model_data = data["model_data"]
    id = callback_query.data.split("_")[2]
    await state.update_data(id = id)

    # Set the current state to wait for new quantity input
    await state.set_state(SizesEditor.wait_for_new_quantity)
    await state.update_data(id=id)

    # Send a message to the user to enter the new quantity value
    await callback_query.message.answer("Enter new quantity:")

@router.message(lambda message: message.text.isdigit(), StateFilter(SizesEditor.wait_for_new_quantity))
async def confirm_new_quantity(message: types.Message, state: FSMContext):
    id = (await state.get_data())["id"]
    new_quantity = int(message.text)

    # Store the new quantity in the state, but don't save it yet
    await state.update_data(new_quantity=new_quantity)

    # Set the state to confirm_quantity
    await state.set_state(SizesEditor.confirm_quantity)

    # Send a confirmation message to the user with inline keyboard buttons
    text = f"�������� ���������� ��� id {id} �� {new_quantity}?"
    inline_keyboard = [
        [types.InlineKeyboardButton(text="�����������", callback_data="quantitysizesconfirm_yes"),
         types.InlineKeyboardButton(text="��������", callback_data="quantitysizesconfirm_no")]
    ]
    await message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard))

@router.callback_query(lambda callback_query: callback_query.data.startswith("quantitysizesconfirm_"), StateFilter(SizesEditor.confirm_quantity))
async def confirm_or_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    
    id = (await state.get_data())["id"]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text = "�����", callback_data = f"select_id_{id}")]])
    
    if callback_query.data == "quantitysizesconfirm_yes":
        # Get the new quantity from the state
        new_quantity = (await state.get_data())["new_quantity"]

        # Update the quantity value in the model data
        model_data = (await state.get_data())["model_data"]
        model_data[id]["����������"] = new_quantity

        # Save the updated model data
        await state.update_data(model_data=model_data)

        # Send a confirmation message to the user
        await callback_query.message.answer(f"���������� ��� id {id} �������� �� {new_quantity}", reply_markup=keyboard)
        await state.update_data(new_quantity = None)
        await state.set_state(SizesEditor.show_info)
    elif callback_query.data == "quantitysizesconfirm_no":
        await state.update_data(new_quantity = None)
        await state.set_state(SizesEditor.show_info)
        await callback_query.message.answer("��������� ��������", reply_markup=keyboard)
        
@router.callback_query(lambda callback_query: callback_query.data.startswith("change_size_"). StateFilter(SizesEditor))
async def ask_for_new_size(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    model_data = data["model_data"]
    id = callback_query.data.split("_")[2]
    await state.update_data(id = id)

    # Set the current state to wait for new size input
    await state.set_state(SizesEditor.wait_for_new_size)
    await state.update_data(id=id)

    # Send a message to the user to enter the new size value
    await callback_query.message.answer("Enter new size:")

@router.message(lambda message: message.text, StateFilter(SizesEditor.wait_for_new_size))
async def confirm_new_size(message: types.Message, state: FSMContext):
    id = (await state.get_data())["id"]
    new_size = message.text

    # Store the new size in the state, but don't save it yet
    await state.update_data(new_size=new_size)

    # Set the state to confirm_size
    await state.set_state(SizesEditor.confirm_size)

    # Send a confirmation message to the user with inline keyboard buttons
    text = f"�������� ������ ��� id {id} �� {new_size}?"
    inline_keyboard = [
        [types.InlineKeyboardButton(text="�����������", callback_data="sizesconfirm_yes"),
         types.InlineKeyboardButton(text="��������", callback_data="sizesconfirm_no")]
    ]
    await message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard))

@router.callback_query(lambda callback_query: callback_query.data.startswith("sizesconfirm_"), StateFilter(SizesEditor.confirm_size))
async def confirm_or_cancel_size(callback_query: types.CallbackQuery, state: FSMContext):
    
    id = (await state.get_data())["id"]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text = "�����", callback_data = f"select_id_{id}")]])
    
    if callback_query.data == "sizesconfirm_yes":
        # Get the new size from the state
        new_size = (await state.get_data())["new_size"]
        id = (await state.get_data())["id"]

        # Update the size value in the model data
        model_data = (await state.get_data())["model_data"]

        # Check if the new size already exists
        if any(item["������"] == new_size for item in model_data.values() if item["������"] != model_data[id]["������"]):
            await callback_query.message.answer("������ ��� ����������", reply_markup=keyboard)
            await state.update_data(new_size = None)
            await state.set_state(SizesEditor.show_info)
        else:
            model_data[id]["������"] = new_size

            # Save the updated model data
            await state.update_data(model_data=model_data)

            # Send a confirmation message to the user
            await callback_query.message.answer(f"������ ��� id {id} ������� �� {new_size}", reply_markup=keyboard)
            await state.update_data(new_size = None)
            await state.set_state(SizesEditor.show_info)
    elif callback_query.data == "sizesconfirm_no":
        await state.update_data(new_size = None)
        await state.set_state(SizesEditor.show_info)
        await callback_query.message.answer("��������� ��������", reply_markup=keyboard)
        
@router.callback_query(lambda callback_query: callback_query.data == "add_size")
async def add_size(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(SizesEditor.wait_for_add_size)
    await callback_query.message.answer("������� ����� ������:")
    
@router.message(lambda message: message.text, StateFilter(SizesEditor.wait_for_add_size))
async def confirm_new_size(message: types.Message, state: FSMContext):
    new_size = message.text

    # Store the new size in the state, but don't save it yet
    await state.update_data(new_size=new_size)

    # Set the state to confirm_size
    await state.set_state(SizesEditor.confirm_addsize)

    # Send a confirmation message to the user with inline keyboard buttons
    text = f"�������� ������ {new_size}?"
    inline_keyboard = [
        [types.InlineKeyboardButton(text="�����������", callback_data="sizesconfirmadd_yes"),
         types.InlineKeyboardButton(text="��������", callback_data="sizesconfirmadd_no")]
    ]
    await message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
    
@router.callback_query(lambda callback_query: callback_query.data.startswith("sizesconfirmadd_"), StateFilter(SizesEditor.confirm_addsize))
async def confirm_or_cancel_size(callback_query: types.CallbackQuery, state: FSMContext):
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text = "�����", callback_data = f"sizeschange")]])

    if callback_query.data == "sizesconfirmadd_yes":
        # Get the new size from the state
        new_size = (await state.get_data())["new_size"]

        # Update the model data
        model_data = (await state.get_data())["model_data"]

        # Check if the size already exists
        if any(item["������"] == new_size for item in model_data.values()):
            await callback_query.message.answer("������ ��� ����������", reply_markup=keyboard)
            await state.update_data(new_size = None)
            await state.set_state(SizesEditor.show_info)
        else:
            new_id = f"new{str(len(model_data))}"
            model_data[new_id] = {"������": new_size, "����������": 0}

            # Save the updated model data
            await state.update_data(model_data=model_data)

            # Send a confirmation message to the user
            await callback_query.message.answer(f"������ {new_size} ��������", reply_markup=keyboard)
            await state.update_data(new_size = None)
            await state.set_state(SizesEditor.show_info)
    elif callback_query.data == "sizesconfirmadd_no":
        await state.update_data(new_size = None)
        await state.set_state(SizesEditor.show_info)
        await callback_query.message.answer("���������� ������� ��������", reply_markup=keyboard)
        
@router.callback_query(lambda callback: callback.data == "savesizes", StateFilter(SizesEditor))
async def save_all(callback : types.CallbackQuery, state : FSMContext):
    if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
        return    
    data = await state.get_data()
    model_data = data['model_data']
    brand = data['brand']
    model = data['model']
    color = data['color']
    
    print(model_data)
    
    for key,value in model_data.items():
        if key.startswith("new"):
            await ASQL.execute("""
            INSERT INTO ��������� (
              `�����`,
              `������`,
              `������`,
              `���������`,
              `����������`,
              `����`,
              `����`,
              `������`,
              `��������� ����`,
              `�������`,
              `url`
            )
            SELECT 
              ?,
              ?,
              ?,
              ?,
              ?,
              k.`����`,
              k.`����`,
              k.`������`,
              k.`��������� ����`,
              k.`�������`,
              k.`url`
            FROM ��������� k
            WHERE k.`�����` = ? AND k.`������` = ? AND k.`���������` = ?
        """, (brand, model, int(value['������']), color, int(value['����������']), brand, model, color))
        else:
          
            await ASQL.execute(f"UPDATE ��������� SET ���������� = ?, ������ = ? WHERE id = ?", (int(value['����������']), int(value['������']), int(key)))
            print(int(value['����������']), int(value['������']), int(key))  
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=
                                          [
                                              [types.InlineKeyboardButton(text="����� � �������", callback_data=f"modeladminpanel_{brand}_{model}")]
                                              ]) 
    await state.clear()
    
    await callback.message.answer("��������� ������� ���������!", reply_markup=keyboard)
               
@router.callback_query(lambda callback: callback.data == "cancelsizes")
async def cancelall(callback: types.CallbackQuery, state:FSMContext):
    
    data = await state.get_data()
    model_data = data['model_data']
    brand = data['brand']
    model = data['model']


    keyboard = types.InlineKeyboardMarkup(inline_keyboard=
                                          [
                                              [types.InlineKeyboardButton(text="����� � �������", callback_data=f"modeladminpanel_{brand}_{model}")]
                                              ]) 
    await state.clear()
    
    await callback.message.answer("��� ����������� ��������!", reply_markup=keyboard)