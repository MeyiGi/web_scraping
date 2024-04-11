# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

rating = {
    "One"   : 1,
    "Two"   : 2,
    "Three" : 3,
    "Four"  : 4,
    "Five"  : 5,
}

class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        # Strip all whitespaces from strings (<-- Хуй пойми что за функция)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                if isinstance(value, tuple):
                    adapter[field_name] = value[0].strip()
                else:
                    adapter[field_name] = value.strip()
                
        # Category & Product-Type --> lowercase (<-- Хуй понял что за функция)
        lower_keys = ["category", "product_type"]
        for lower_key in lower_keys:
            value = adapter.get(lower_key)
            adapter[lower_key] = value.lower()
        
        # Price --> float   
        
        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)
            
        # Avaibiluty replace to only number (<-- Поймешь если зайдешь в file.json)
        avaibality_string = adapter.get("availability")
        split_string_array = avaibality_string.split("(")
        if len(split_string_array) < 2:
            adapter["availability"] = 0
        else:
            availability_string = split_string_array[1].split(" ")
            adapter["availability"] = int(availability_string[0])
            
        # Reviews replace to only number
        num_reviews_string = adapter.get("num_reviews")
        adapter["num_reviews"] = int(num_reviews_string)
        
        # Stars replace to onlu number
        adapter["stars"] = rating[adapter.get("stars").split(" ")[1]]
                
        return item


class MySpider:
    name = 'myspider'

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        
        self.connection = psycopg2.connect(
            database='', # Your database
            user='', # Your user
            password='', # Your passwrod
            host='', # Your host
            port='', # Your port
        )
        # Create cursor, used to execute commands
        self.cursor = self.connection.cursor()
        
        # Create books table if not exists
        
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                url VARCHAR(255),
                title TEXT,
                upc VARCHAR(255),
                product_type VARCHAR(255),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                availability INTEGER,
                num_reviews INTEGER,
                stars INTEGER,
                category VARCHAR(255),
                description TEXT,
                price DECIMAL
            )
        """)
        
        
        self.connection.commit()
        self.cursor.close()
    
    def process_item(self, item, spider):
        self.cursor.execute("""INSERT INTO books (
            url,
            title,
            upc,
            product_type,
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"][0])
        ))

        self.connection.commit()
        return item
    
    def process_item(self, item, spider):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("""INSERT INTO books (
                    url,
                    title,
                    upc,
                    product_type,
                    price_excl_tax,
                    price_incl_tax,
                    tax,
                    price,
                    availability,
                    num_reviews,
                    stars,
                    category,
                    description
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                    item["url"],
                    item["title"],
                    item["upc"],
                    item["product_type"],
                    item["price_excl_tax"],
                    item["price_incl_tax"],
                    item["tax"],
                    item["price"],
                    item["availability"],
                    item["num_reviews"],
                    item["stars"],
                    item["category"],
                    str(item["description"][0])
                ))

        return item
    
    def close_spider(self, spider):
        
        # Close cursor & connection of database
        self.cursor.close()
        self.connection.close()