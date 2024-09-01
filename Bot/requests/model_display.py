# -*- coding: windows-1251 -*-
from logging import INFO, Manager
from Bot import data
from asql import ASQL

async def convert_data_to_dict(data_list) -> dict:
    data = data_list[0]
    return {
        'Бренд':data[0],
        'Модель':data[1],
        'Размер':data[2],
        'Цена':data[3],
        'Рассцветка':data[5],           
        'Скидка':data[6],
        'Скидочная цена':data[7],
        'Новинка':data[8],
        'id':data[9],
        'url':data[10],
		'Количество':data[11]
        }

async def textAboutModel(about_model:dict, current:int, count:int, enable_manager_info:bool = False)->str:
	if about_model['Скидка'] == 1:  # Скидка есть
		price_info = (
			f"Скидочная цена: {about_model['Скидочная цена']} BYN.\n"
		)
	else:
		price_info = (
			f"Цена: {about_model['Цена']} BYN\n"	
		)
		
	if enable_manager_info:
		info_for_managers = f'''
ID: {about_model['id']}
URL: {about_model['url']}
Количество на складе: {about_model['Количество']}
'''
	else:
		info_for_managers = ""
		

		# Формирование текстового описания
	return f'''
{"[Новинка]" if about_model['Новинка'] else ''} {about_model['Бренд']} {about_model['Модель']} --> {current}\{count}

Цвет: {about_model['Рассцветка']}
Размер: {about_model['Размер']}
{price_info}
{info_for_managers}
'''

async def get_models_id(callback_data:str, positive_count:bool = True):
	start_iter:int = None
	option:str = None
	if data.Callback['model']['def'] in callback_data:
		start_iter = 1
	elif data.Callback['model']['new'] in callback_data:
		start_iter = 2
		option = "Новинка"
	elif data.Callback['model']['sales'] in callback_data:
		start_iter = 2
		option = "Скидка"
	else:
		start_iter = 1
	callback_data = callback_data.split("_")
	brand = callback_data[start_iter]
	model = callback_data[start_iter + 1]
	request = f"SELECT id FROM Кроссовки WHERE Бренд = \'{brand}\' AND Модель = \'{model}\' {'AND Количество > 0' if positive_count else ''}" #попробовать забирать все айди
	if option:
		request += f" AND {option} = 1"
	models_data = await ASQL.execute(request)
	return [model[0] for model in models_data]

async def get_text_about_model(id : int, current:int, count:int, enable_manager_info:bool = False):
	model_info_list = await ASQL.execute(f"SELECT * FROM Кроссовки WHERE id = {id}")
	model_info_dict = await convert_data_to_dict(model_info_list)
	return await textAboutModel(model_info_dict, current, count, enable_manager_info)


	
	