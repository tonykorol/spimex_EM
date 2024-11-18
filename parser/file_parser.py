import os
from datetime import datetime

import xlrd
from xlrd.sheet import Sheet

from parser.data_classes import Product

download_directory = os.path.join(os.getcwd(), "parser")
download_folder = os.path.join(download_directory, "downloaded_files")
products = []


def get_filename() -> str:
    """
    Генераторная функция, которая возвращает имена файлов из папки загрузок.

    Эта функция перебирает все файлы в указанной папке загрузок (download_folder)
    и возвращает их по одному. Каждый вызов функции вернет следующее имя файла
    в папке, пока не будут перечислены все файлы.
    """
    for filename in os.listdir(download_folder):
        yield filename


def parse_files() -> None:
    """
    Парсит Excel файлы из указанной папки загрузок.

    Эта функция перебирает все файлы в папке загрузок, которые ожидаются как
    Excel файлы. Для каждого файла она открывает рабочую книгу, получает
    доступ к первому листу и вызывает функцию parse_sheet, чтобы обработать
    данные, содержащиеся на этом листе.
    """
    for filename in get_filename():
        workbook = xlrd.open_workbook(os.path.join(download_folder, filename))
        sheet = workbook.sheet_by_index(0)
        parse_sheet(sheet)


def parse_sheet(sheet: Sheet) -> None:
    """
    Функция для построчного чтения данных из листа таблицы и добавления продуктов в список.

    Сначала считывается дата продукта из второй ячейки третьей строки и сохраняется в переменную product_date.
    Затем происходит перебор строк, начиная с пятой, до предпоследней строки листа.

    Для каждой строки:
    - Обновляется флаг записи на основе значения во второй ячейке текущей строки с помощью функции update_write_flag.
    - Если флаг записи равен True и строка проходит проверку на валидность (is_valid_row),
      продукт создается с помощью функции create_product и добавляется в список products.
    """
    write_flag = False
    product_date = extract_product_date(sheet.row_values(3)[1])
    for row_num in range(5, sheet.nrows-2):
        row_values = sheet.row_values(row_num)
        write_flag = update_write_flag(row_values[1], write_flag)

        if write_flag and is_valid_row(row_values):
            products.append(create_product(row_values, product_date))


def extract_product_date(date_string: str) -> str:
    """
    Из строки date_string возвращает дату продукта
    """
    return date_string.split()[2]


def update_write_flag(current_string: str, current_write_flag: bool) -> bool:
    """
    Обновляет флаг записи на основе значения current_string.

    Если current_string равно 'Единица измерения: Метрическая тонна',
    возвращает True.

    Если current_string равно 'Единица измерения: Килограмм',
    возвращает False.

    Если current_string не соответствует ни одному из этих значений,
    возвращает текущее значение current_write_flag.
    """
    if current_string == 'Единица измерения: Метрическая тонна':
        return True
    elif current_string == 'Единица измерения: Килограмм':
        return False
    else: return current_write_flag


def is_valid_row(row_values: list[str]) -> bool:
    """
    Функция проверяет валидность переданной строки.

    Если значение в первой ячейке строки равно 'Итого' или ячейка пустая,
    строка не является валидной.

    Если значение в последней ячейке строки не является целым положительным числом,
    строка не является валидной.

    В противном случае строка является валидной.
    """
    if not row_values[1] or row_values[1].startswith("Итого"):
        return False
    try:
        return int(row_values[-1]) > 0
    except ValueError:
        return False


def create_product(row_values: list[str], product_date: str) -> Product:
    """
    Функция для создания продукта на основе переданной строки.

    В переменные считываются значения из строки, которые
    далее используются при создании экземпляра класса Product.
    """
    exchange_product_id = row_values[1]
    exchange_product_name = row_values[2].split(',')[0]
    oil_id = exchange_product_id[:4]
    delivery_basis_id = exchange_product_id[4:7]
    delivery_basis_name = row_values[3]
    delivery_type_id = exchange_product_id[-1]
    volume = int(row_values[4])
    total = int(row_values[5])
    count = int(row_values[-1])
    date = datetime.strptime(product_date, "%d.%m.%Y")
    product = Product(
        exchange_product_id,
        exchange_product_name,
        oil_id,
        delivery_basis_id,
        delivery_basis_name,
        delivery_type_id,
        volume,
        total,
        count,
        date
    )
    return product


def get_products() -> list[Product]:
    """
    Функция для получения списка продуктов.

    Сначала вызывается функция parse_files для парсинга файлов.
    Затем возвращается список продуктов.
    """
    parse_files()
    return products
