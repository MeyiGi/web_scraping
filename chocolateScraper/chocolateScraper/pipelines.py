# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gbpToUsd = 1.3
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter.get('price'):
            
            floatPrice = float(adapter['price'])
            
            adapter['price'] = floatPrice * self.gbpToUsd
            
            return item
        
        else:
            raise DropItem(f"Missing price in {item}")
        
class DuplicatesPipeline:
    
    def __init__(self):
        self.names_seen = set()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter['name'] in self.names_seen:
            raise DropItem(f"duplicated item found {item!r}")
        else:
            self.names_seen.add(adapter["name"])
            return item
        
class SavingToPostgreSQLPipelines(object):
    
    def __init__(self):
        self.create_connection()
        
    def create_connection(self):
        self.connection = psycopg2.connect(
            host = '', #Your host
            user = '', # Your user
            password = '', # Your password
            database = '', # Your database
            port = '', # Your port
        )
        self.curr = self.connection.cursor()
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        try:
            self.curr.execute(""" insert into chocolate_product (name, price, url) values (%s, %s, %s)""", (
                item['name'],
                item['price'],
                item['url'],
            ))
            
            self.connection.commit()
        except Exception as e:
            print(f"Error storing data in database {e}")
            self.connection.rollback()