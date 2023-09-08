"""
0x -> Код ошибка

"""


errors = {
    "0x000000": "Данные не найдены" ,
}


def raise_error(err_code: str):
    if err_code not in errors:
        print('Ошибка не найдена или еще не обрабатывается')
    else:
        print(errors[err_code])
    exit(1)
