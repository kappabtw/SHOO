# -*- coding: windows-1251 -*-
from logging import INFO, Manager
from Bot import data
from asql import ASQL

async def convert_data_to_dict(brand:str, model:str, sizes:list,color:str, model_info) -> dict:
	def_price,discount,discount_price,is_new = model_info
	print(def_price,discount,discount_price,is_new)
	return {
		'Бренд':brand,
		'Модель':model,
		'Размеры':list(map(int, sizes)),
		'Цена':def_price,
		'Рассцветка':color,           
		'Скидка':discount,
		'Скидочная цена':discount_price,
		'Новинка':is_new
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
[{current+1} из {count}]

{"[Новинка]" if about_model['Новинка'] else ''} {about_model['Бренд']} {about_model['Модель']}

Цвет: {about_model['Рассцветка']}

Размеры: {about_model['Размеры']}

{price_info}
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
	request = f"""SELECT 
  Расцветка, 
  GROUP_CONCAT(CASE WHEN Количество > 0 THEN Размер ELSE NULL END) AS Sizes
FROM 
  Кроссовки
WHERE 
  Бренд = '{brand}' 
  AND Модель = '{model}'
  AND Расцветка IN (
	SELECT 
	  Расцветка
	FROM 
	  Кроссовки
	WHERE 
	  Бренд = '{brand}' 
	  AND Модель = '{model}' 
	  {"AND Количество > 0" if positive_count else ""}
	  {f"AND {option} = 1" if option else ""}
  )
  AND Количество > 0
GROUP BY 
  Расцветка"""
	print(request)
	models_data = await ASQL.execute(request)
	print(models_data)
	return models_data

async def get_text_about_model(brand: str, model: str, list_colors_sizes: list, current: int, count: int):
	sizes = [size for size in list_colors_sizes[current][1].split(",")]
	print(*sizes)
	print(model, brand)
	color = list_colors_sizes[current][0]
	signs = ",".join(["?"] * len(sizes))  # Create a string of placeholders
	print(sizes, signs)
	model_info = await ASQL.execute(f"SELECT DISTINCT Цена,Скидка,\"Скидочная цена\",Новинка FROM Кроссовки WHERE Модель = ? AND Бренд = ? AND Расцветка = ? AND Размер IN ({signs})", (model, brand,color, *sizes))
	print(model_info)
	model_info_dict = await convert_data_to_dict(brand, model, sizes, color, model_info[0])
	return await textAboutModel(model_info_dict, current, count)


	
	