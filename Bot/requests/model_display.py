# -*- coding: windows-1251 -*-
from logging import INFO, Manager
from Bot import data
from asql import ASQL

async def convert_data_to_dict(data_list) -> dict:
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
        'url':data[10],
		'����������':data[11]
        }

async def textAboutModel(about_model:dict, current:int, count:int, enable_manager_info:bool = False)->str:
	if about_model['������'] == 1:  # ������ ����
		price_info = (
			f"��������� ����: {about_model['��������� ����']} BYN.\n"
		)
	else:
		price_info = (
			f"����: {about_model['����']} BYN\n"	
		)
		
	if enable_manager_info:
		info_for_managers = f'''
ID: {about_model['id']}
URL: {about_model['url']}
���������� �� ������: {about_model['����������']}
'''
	else:
		info_for_managers = ""
		

		# ������������ ���������� ��������
	return f'''
{"[�������]" if about_model['�������'] else ''} {about_model['�����']} {about_model['������']} --> {current}\{count}

����: {about_model['����������']}
������: {about_model['������']}
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
		option = "�������"
	elif data.Callback['model']['sales'] in callback_data:
		start_iter = 2
		option = "������"
	else:
		start_iter = 1
	callback_data = callback_data.split("_")
	brand = callback_data[start_iter]
	model = callback_data[start_iter + 1]
	request = f"SELECT id FROM ��������� WHERE ����� = \'{brand}\' AND ������ = \'{model}\' {'AND ���������� > 0' if positive_count else ''}" #����������� �������� ��� ����
	if option:
		request += f" AND {option} = 1"
	models_data = await ASQL.execute(request)
	return [model[0] for model in models_data]

async def get_text_about_model(id : int, current:int, count:int, enable_manager_info:bool = False):
	model_info_list = await ASQL.execute(f"SELECT * FROM ��������� WHERE id = {id}")
	model_info_dict = await convert_data_to_dict(model_info_list)
	return await textAboutModel(model_info_dict, current, count, enable_manager_info)


	
	