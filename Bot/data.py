# -*- coding: windows-1251 -*-

Message = {
    "upper_menu" : "Старт",
    "upper_info" : "Информация о нас",
    "sales" : "Скидки",		  #НУЖНО БЫЛО ХРАНИТЬ В JSON`Е
    "new_items" : "Новинки",
    "catalog": "Каталог",
    "manager": "Менеджер",
    "reviews": "Отзывы",
    "info":"Информация",

    "brand" : {
           "def" : "Выбери бренд",
           "sales" : "Выбери бренд со скидками",
           "new" : "Выбери бренд с новинками"
        },
    
    "model" : {
           "def" : "Выбери модель",
           "sales" : "Выбери модель со скидкой",
           "new" : "Выбери модель из новинок"
        },
    
    "back" : {
        "menu" : "Назад в меню",
        "catalog" : "Назад в каталог",
        "brand" : {
           "def" : "Назад к брендам",
           "sales" : "Назад к брендам [Скидки]",
           "new" : "Назад к брендам [Новинки]"
        },
        "model" : {
           "def" : "Назад к моделям",
           "sales" : "Назад к моделям [Скидки]",
           "models" : "Назад к моделям [Новинки]"
            }
        }
    }

Callback = {
    
    "sales" : "sales",		  #НУЖНО БЫЛО ХРАНИТЬ В JSON`Е
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




