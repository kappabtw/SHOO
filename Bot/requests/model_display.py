# -*- coding: windows-1251 -*-
from logging import INFO, Manager
from Bot import data
from asql import ASQL

async def convert_data_to_dict(brand:str, model:str, sizes:list,color:str, model_info) -> dict:
	def_price,discount,discount_price,is_new = model_info
	print(def_price,discount,discount_price,is_new)
	return {
		'�����':brand,
		'������':model,
		'�������':list(map(int, sizes)),
		'����':def_price,
		'����������':color,           
		'������':discount,
		'��������� ����':discount_price,
		'�������':is_new
	}

async def textAboutModel(about_model:dict, current:int, count:int, more_info:bool = False, sizes_count = None)->str:
	if about_model['������'] == 1:  # ������ ����
		price_info = (
			f"��������� ����: {about_model['��������� ����']} BYN.\n"
		)
	else:
		price_info = (
			f"����: {about_model['����']} BYN\n"	
		)

		
	if more_info:
		sizes_info = f"�������|����������:"
		for current_size in sizes_count:
			sizes_info += f"\n{current_size[0]} | {current_size[1]}"
	else:
		sizes_info = f"�������: {about_model['�������']}"
		
	return f'''
[{current+1} �� {count}]

{"[�������]" if about_model['�������'] else ''} {about_model['�����']} {about_model['������']}

����: {about_model['����������']}

{sizes_info}

{price_info}
'''

async def get_models_id(callback_data:str, positive_count:bool = True):
	print(positive_count)
	start_iter:int = None
	option:str = None
	if data.Callback['model']['def'] in callback_data:
		start_iter = 1
	elif data.Callback['model']['new'] in callback_data:
		start_iter = 2
		option = "�������"
	elif data.Callback['model']['sales'] in callback_data:
		start_iter = 2
		option = "������"
	else:
		start_iter = 1
	callback_data = callback_data.split("_")
	brand = callback_data[start_iter]
	model = callback_data[start_iter + 1]
	request = f"""SELECT 
  ���������, 
  GROUP_CONCAT(������) AS Sizes
FROM 
  ���������
WHERE 
  ����� = '{brand}' 
  AND ������ = '{model}'
  AND ��������� IN (
	SELECT 
	  ���������
	FROM 
	  ���������
	WHERE 
	  ����� = '{brand}' 
	  AND ������ = '{model}' 
	  {"AND ���������� > 0" if positive_count else ""}
	  {f"AND {option} = 1" if option else ""}
  )
GROUP BY 
  ���������"""
	print(request)
	models_data = await ASQL.execute(request)
	print(models_data)
	return models_data

async def get_text_about_model(brand: str, model: str, list_colors_sizes: list, current: int, count: int, more_info:bool = False):
	sizes = [size for size in list_colors_sizes[current][1].split(",")]
	print(*sizes)
	print(model, brand)
	color = list_colors_sizes[current][0]
	signs = ",".join(["?"] * len(sizes))  # Create a string of placeholders
	print(sizes, signs)
	model_info = await ASQL.execute(f"SELECT DISTINCT ����,������,\"��������� ����\",������� FROM ��������� WHERE ������ = ? AND ����� = ? AND ��������� = ? AND ������ IN ({signs})", (model, brand,color, *sizes))
	if more_info:
		sizes_count = await ASQL.execute(f"SELECT ������, ���������� FROM ��������� WHERE ������ = ? AND ����� = ? AND ��������� = ? AND ������ IN ({signs})", (model, brand,color, *sizes))
		print("iefn    ", sizes_count)
	else: 
		sizes_count = None
	print(model_info)
	model_info_dict = await convert_data_to_dict(brand, model, sizes, color, model_info[0])
	return await textAboutModel(model_info_dict, current, count, more_info, sizes_count)


	
	