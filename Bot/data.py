# -*- coding: windows-1251 -*-

Message = {
    "upper_menu" : "�����",
    "upper_info" : "���������� � ���",
    "sales" : "������",		  #����� ���� ������� � JSON`�
    "new_items" : "�������",
    "catalog": "�������",
    "manager": "��������",
    "reviews": "������",
    "info":"����������",

    "brand" : {
           "def" : "������ �����",
           "sales" : "������ ����� �� ��������",
           "new" : "������ ����� � ���������"
        },
    
    "model" : {
           "def" : "������ ������",
           "sales" : "������ ������ �� �������",
           "new" : "������ ������ �� �������"
        },
    
    "back" : {
        "menu" : "����� � ����",
        "catalog" : "����� � �������",
        "brand" : {
           "def" : "����� � �������",
           "sales" : "����� � ������� [������]",
           "new" : "����� � ������� [�������]"
        },
        "model" : {
           "def" : "����� � �������",
           "sales" : "����� � ������� [������]",
           "models" : "����� � ������� [�������]"
            }
        }
    }

Callback = {
    
    "sales" : "sales",		  #����� ���� ������� � JSON`�
    "new_items" : "new_items",
    "catalog": "to_catalog_",
    "manager": "manager",
    "menu": "to_menu",
    "reviews": "reviews",
    "info":"info",

    "brand" : {
           "def" : "defbrand_",
           "sales" : "brand_sales_",
           "new" : "brand_new_"
        },
    
    "model" : {
           "def" : "defmodel_",
           "sales" : "model_sales_",
           "new" : "model_new_"
        }
    }

model_options = (
    Callback['model']['def'],
    Callback['model']['sales'],
    Callback['model']['new']
    )

time_photo = "AgACAgIAAxkBAAIWcWalyNHHCXDGIz6Go45oPY3ShLltAAKY6zEbb_opSYPWrqNeY8t9AQADAgADeQADNQQ"




