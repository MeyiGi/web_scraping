from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
import re

def replace_none_with_zero(value):
    return 0 if value is None else value

def extract_digits_with_decimal(value):
    # Используем регулярное выражение для извлечения цифр и точек из строки
    digits_with_decimal = re.sub(r'[^0-9.]', '', value)
    return digits_with_decimal

class ProductLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    default_input_processor  = MapCompose(lambda x : x.strip(), replace_none_with_zero)
    price_in = MapCompose(extract_digits_with_decimal)