# -*- coding: windows-1251 -*-
from Bot import data
from asql import ASQL

async def data_to_dict(data_list) -> dict:
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
        'url':data[10]        
        }

async def textAboutModel(about_model:dict, current:int, count:int)->str:
	if about_model['Скидка'] == 1:  # Скидка есть
		price_info = (
			f"Скидочная цена: {about_model['Скидочная цена']} BYN.\n"
		)
	else:
		price_info = (
			f"Цена: {about_model['Цена']} BYN\n"	
		)

		# Формирование текстового описания
	return f'''
{"/[Новинка/]" if about_model['Новинка'] else ''} {about_model['Бренд']} {about_model['Модель']} [{current}\{count}]

Цвет: {about_model['Рассцветка']}
Размер: {about_model['Размер']}
{price_info}
ID: {about_model['id']}
URL: {about_model['url']}
'''

async def get_models_id(callback_data:str):
	if data.Callback['model']['def'] in callback_data:
		start_iter = 1
		option = None
	elif data.Callback['model']['new'] in callback_data:
		start_iter = 2
		option = "Новинка"
	else:
		start_iter = 2
		option = "Скидка"
	callback_data = callback_data.split("_")
	print(start_iter, callback_data)
	brand = callback_data[start_iter]
	model = callback_data[start_iter + 1]
	request = f"SELECT id FROM Кроссовки WHERE Бренд = \'{brand}\' AND Модель = \'{model}\'" #попробовать забирать все айди
	if option:
		request += f"AND {option} = 1"
	models_data = await ASQL.execute(request)
	return [model[0] for model in models_data]

async def show_model(id : int, current:int, count:int):
	model_info_list = await ASQL.execute(f"SELECT * FROM Кроссовки WHERE id = {id}")
	model_info_dict = await data_to_dict(model_info_list)
	return await textAboutModel(model_info_dict, current, count)


	
	