# -*- coding: windows-1251 -*-
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asql import ASQL


router = Router()

add_model_clear_state = types.InlineKeyboardButton(text = "��������", callback_data="add_model_clear_state")

class AddModelForm(StatesGroup):
    brand = State()
    model = State()
    size = State()
    price = State()
    color = State()
    discount = State()
    discount_price = State()
    is_new = State()
    quantity = State()
    size_quantity = State()
    check = State()
    
        
@router.message(Command("add_model"), StateFilter(None))
async def add_model_start(message: types.Message, state: FSMContext):
    
    if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (message.from_user.id)))[0][0] != 1:
        return
    
    await message.answer(text="���������� ����� ������ � �������.\n������� ����� ���������:",
                         reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                            types.InlineKeyboardButton(text="���������", callback_data = "retry_state_brand")]]))
    await state.set_state(AddModelForm.brand)

@router.message(AddModelForm.brand)
async def add_model_brand(message: types.Message, state: FSMContext):
    brand = message.text
    if len(brand) > 50:
        await message.answer("����� ������ ���� �� ����� 50 ��������.")
        return
    await state.update_data(brand=brand)
    await message.answer("������� ������ ���������:",
                         reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                            types.InlineKeyboardButton(text="���������", callback_data = "retry_state_model")]]))
    await state.set_state(AddModelForm.model)

@router.message(AddModelForm.model)
async def add_model_model(message: types.Message, state: FSMContext):
    model = message.text
    if len(model) > 50:
        await message.answer("������ ������ ���� �� ����� 50 ��������.")
        return
    await state.update_data(model=model)
    await message.answer("������� ������ ��������� (����� ������� ����� ��������� ����� �������):",
                         reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                            types.InlineKeyboardButton(text="���������", callback_data = "retry_state_size")]]))
    await state.set_state(AddModelForm.size)

@router.message(AddModelForm.size)
async def add_model_size(message: types.Message, state: FSMContext):
    size = message.text
    INT_SIZE:list = []
    try:
        if "," in size:
            if " " in size:
                size = size.translate(str.maketrans("",""," "))
                print(size)
            parts = size.split(",")
            for part in parts:
                if not part.isdigit() or not int(part) >= 0 or not int(part) <= 100:
                    await message.answer("������������ ������. ��������� ����.")
                    return
                INT_SIZE.append(int(part))         
        else:
                
            if not size.isdigit() and int(size) >= 0 and int(size) <= 100:
                await message.answer("������������ ������. ��������� ����.")
                return
            INT_SIZE.append(int(size))
        await state.update_data(size=INT_SIZE)
    except ValueError:
        await message.answer("������������ ������. ��������� ������")
        return
    await message.answer("������� ���� ���������:",
                         reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                            types.InlineKeyboardButton(text="���������", callback_data = "retry_state_price")]]))
    await state.set_state(AddModelForm.price)

@router.message(AddModelForm.price)
async def add_model_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("���� ������ ���� ������.")
        return
    await state.update_data(price=int(price))
    await message.answer("������� ��������� ���������:",
                         reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                            types.InlineKeyboardButton(text="���������", callback_data = "retry_state_color")]]))
    await state.set_state(AddModelForm.color)

@router.message(AddModelForm.color)
async def add_model_color(message: types.Message, state: FSMContext):
    color = message.text
    if len(color) > 50:
        await message.answer("��������� ������ ���� �� ����� 50 ��������.")
        return
    await state.update_data(color=color)
    await message.answer("����� �� ������? (1 - ��, 0 - ���):",
                            reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                                types.InlineKeyboardButton(text="���������", callback_data = "retry_state_discount")]]))
    await state.set_state(AddModelForm.discount)

@router.message(AddModelForm.discount)
async def add_model_discount(message: types.Message, state: FSMContext):
    discount = message.text
    if not discount.isdigit():
        await message.answer("������� �����.")
        return
    await state.update_data(discount=int(discount))
    if int(discount) == 1:
        await message.answer("������� ��������� ���� ���������:",
                            reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                                types.InlineKeyboardButton(text="���������", callback_data = "retry_state_discount_price")]]))
        await state.set_state(AddModelForm.discount_price)
    elif int(discount) == 0:
        await message.answer("�������� �� ��������� ��� �������? (1 - ��, 0 - ���):",
                            reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                                types.InlineKeyboardButton(text="���������", callback_data = "retry_state_is_new")]]))
        await state.set_state(AddModelForm.is_new)
    else:
        await message.answer("������������ ����.")
        return
    await state.update_data(discount=int(discount))

@router.message(AddModelForm.discount_price)
async def add_model_discount_price(message: types.Message, state: FSMContext):
    discount_price = message.text
    if not discount_price.isdigit():
        await message.answer("��������� ���� ������ ���� ������.")
        return
    await state.update_data(discount_price=int(discount_price))
    await message.answer("�������� �� ��������� ��� �������? (1 - ��, 0 - ���):",
                            reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                                types.InlineKeyboardButton(text="���������", callback_data = "retry_state_is_new")]]))
    await state.set_state(AddModelForm.is_new)

@router.message(AddModelForm.is_new)
async def add_model_is_new(message: types.Message, state: FSMContext):
    is_new = message.text
    if not is_new.isdigit:
        await message.answer("������� ������ ���� 0 ��� 1.")
        return
    if int(is_new) == 1 or int(is_new) == 0:
        await state.update_data(is_new=int(is_new))
        await message.answer("���������� ���������� ��� ������/�������. ����� ������� ����� ������� � ����������� � �������� ������(��� ������ ���� ����� - ����� ����������� ��� ���� �������)",
                            reply_markup= types.InlineKeyboardMarkup(inline_keyboard=[[add_model_clear_state,
                                types.InlineKeyboardButton(text="���������", callback_data = "retry_state_quantity")]]))
        await state.set_state(AddModelForm.quantity)
        
@router.message(AddModelForm.quantity)
async def add_model_quantity(message: types.Message, state: FSMContext):
    
    if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (message.from_user.id)))[0][0] != 1:
        return

    quantity = message.text
    INT_QUANTITY:list = []
    stack_incorrect:list = []
    
    if "," in quantity:
        if " " in quantity:
            quantity.translate(str.maketrans("",""," "))
        quantity = quantity.split(",")
        for part in quantity:
            try:
                print(part)
                part = int(part)
                print(part)
                
                if part >= 0 and part <= 100:
                    INT_QUANTITY.append(part)
                else:
                    stack_incorrect.append(part)
            except TypeError:
                stack_incorrect.append(part)
        try:
            sizes = (await state.get_data())['size']
        except Exception as e:
            await message.answer("����������, ������� ����������� � ����������� ��������� ���������")
            return
    
        if len(sizes) != len(INT_QUANTITY):
            await message.answer("����������, ������� ����������� � ����������� ��������� ���������")
            return
    else:
        try:
            quantity = int(quantity)
            if quantity >= 0 and quantity <= 100:
                INT_QUANTITY.append(quantity)
            else: 
                stack_incorrect.append(quantity)
        except TypeError:
            stack_incorrect.append(quantity)
            
    if len(stack_incorrect) != 0:
        await message.answer(f"`{stack_incorrect}` - ������������ ����������. ����������, ��������� ����", parse_mode = ParseMode.MARKDOWN)
        return
    
    
    await state.update_data(quantity = INT_QUANTITY)
    await check_result(message, state)
    print(await state.get_data())
 
    
async def check_result(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    size = list(data['size'])
    quantity = list(data['quantity'])
    
    size_quantity = []
    if len(size) == 1:
        size_quantity.append([size[0], quantity[0]])
    else:
        if len(quantity) == 1:
            for part in size:
                size_quantity.append([part,quantity[0]])
        else:
            for i in range(len(size)):
                size_quantity.append([size[i], quantity[i]])
    print(size_quantity)
    
    await state.update_data(size_quantity = size_quantity)
    await state.set_state(AddModelForm.check)
        
    await message.answer(
        f'''
����� - {data['brand']}
������ - {data['model']}
���� - {data['color']}

������(�) - {data['size']}

������� ���� - {data['price']}
��������� ������ - {"��" if data['discount'] == 1 else "���"}
��������� ���� - {data['discount_price'] if data['discount'] == 1 else "..."}

�������� �������� - {"��" if data['is_new'] == 1 else "���"}

���� [������ - ����������] : {size_quantity}
''',
        reply_markup= types.InlineKeyboardMarkup(inline_keyboard= [[types.InlineKeyboardButton(text = "�����������", callback_data = "add_model_confirm")],
                                                                   [add_model_clear_state]]))
    
@router.callback_query(AddModelForm.check, lambda callback: callback.data == "add_model_confirm")
async def add_to_catalog(callback: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    
    added_models_id = []
    
    discount_pice = -1 if data['discount'] != 1 else data['discount_price']
    
    for i in range(len(data['size_quantity'])):
        result = await ASQL.execute("INSERT INTO ��������� (�����,������,���������,������,����,������,\"��������� ����\",�������,����������) VALUES(?,?,?,?,?,?,?,?,?) RETURNING id",
                            (data['brand'],data['model'],data['color'],
                            data['size_quantity'][i][0],data['price'],data['discount'],
                            discount_pice,data['is_new'],data['size_quantity'][i][1]))
        added_models_id.append(int(result[0][0]))
        
    await callback.message.answer(f"������� ���������.\n��������� ���������� ����� � ������� �������� ������� `/load_image {data['brand']}_{data['model']}_{data['color']}` � ������������ �����������",
                                  parse_mode=ParseMode.MARKDOWN)
    await state.clear()

@router.callback_query(lambda callback: callback.data == "add_model_clear_state")
async def clear_state(callback:types.CallbackQuery, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.clear()
    await callback.answer("���������� ������ �����������.")
    
@router.callback_query(lambda callback: callback.data.startswith("retry_state_"))
async def retry_state(callback: types.CallbackQuery, state: FSMContext):
    
    if (await ASQL.execute("SELECT EXISTS (SELECT 1 FROM ��������� WHERE id = ?)", (callback.from_user.id)))[0][0] != 1:
        return
    
    if await state.get_state() is None:
        await callback.answer(text = "����������, ������� /add_model", show_alert=True)
        return

    state_name = callback.data.split("_")[-1]
    states = {
        "brand": AddModelForm.brand,
        "model": AddModelForm.model,
        "size": AddModelForm.size,
        "price": AddModelForm.price,
        "color": AddModelForm.color,
        "discount": AddModelForm.discount,
        "discount_price": AddModelForm.discount_price,
        "new": AddModelForm.is_new,
        "quantity": AddModelForm.quantity,
    }
    
    await state.set_state(states[state_name])
    await callback.answer("��������� ����.")
                
                
                
    
        

    
    
