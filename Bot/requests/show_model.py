# -*- coding: windows-1251 -*-
from Bot import data
from asql import ASQL

async def data_to_dict(data_list) -> dict:
    data = data_list[0]
    return {
        '�����':data[0],
        '������':data[1],
        '������':data[2],
        '����':data[3],
        '����������':data[5],           
        '������':data[6],
        '��������� ����':data[7],
        '�������':data[8],
        'id':data[9],
        'url':data[10]        
        }

async def textAboutModel(about_model:dict, current:int, count:int)->str:
	if about_model['������'] == 1:  # ������ ����
		price_info = (
			f"��������� ����: {about_model['��������� ����']} BYN.\n"
		)
	else:
		price_info = (
			f"����: {about_model['����']} BYN\n"	
		)

		# ������������ ���������� ��������
	return f'''
{"/[�������/]" if about_model['�������'] else ''} {about_model['�����']} {about_model['������']} [{current}\{count}]

����: {about_model['����������']}
������: {about_model['������']}
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
		option = "�������"
	else:
		start_iter = 2
		option = "������"
	callback_data = callback_data.split("_")
	print(start_iter, callback_data)
	brand = callback_data[start_iter]
	model = callback_data[start_iter + 1]
	request = f"SELECT id FROM ��������� WHERE ����� = \'{brand}\' AND ������ = \'{model}\'" #����������� �������� ��� ����
	if option:
		request += f"AND {option} = 1"
	models_data = await ASQL.execute(request)
	return [model[0] for model in models_data]

async def show_model(id : int, current:int, count:int):
	model_info_list = await ASQL.execute(f"SELECT * FROM ��������� WHERE id = {id}")
	model_info_dict = await data_to_dict(model_info_list)
	return await textAboutModel(model_info_dict, current, count)


	
	