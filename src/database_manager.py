import sqlite3
import typing
from enum import Enum
from datetime import datetime, timezone
from src.logger_conf import logger

class DatabaseNames(str, Enum):
    products = 'products'
    shopping_cart = 'shopping_cart'

class DatabaseManager:
    def __init__(self):
        self._conn = sqlite3.connect('products.db')
        self._cur = self._conn.cursor()
    
    def load_products_from_db(self) -> list:
        '''
            Loads prodcuts from the database,
            returns list of of dictionaries of records.
        '''
        self._cur.execute(f'SELECT product_name, product_description, product_price FROM products')
        products = self._cur.fetchall()
        finalized_list = list()

        for product in products:
            product_dict = {
                product[0] : (product[1], product[2],)
            }
            finalized_list.append(product_dict)
        return finalized_list

    def insert_shopping_cart(self, product_instance: tuple) -> None:
        '''
            Executed once the user presses 'Add to Cart' button on a selected product.
        '''
        with self._conn:
            try:
                self._cur.execute(f'INSERT INTO shopping_cart (product_name, product_description, product_prive, added_at) VALUES(?, ?, ?, ?)', 
                                (*product_instance, datetime.now(timezone.utc)))
            except Exception as ex:
                logger.critical(f'Exception has been found: {ex}')

    def load_shopping_cart_db(self) -> list:
        '''
            Returns all products from shopping_cart table.
        '''
        self._cur.execute('SELECT product_name, product_description, product_prive FROM shopping_cart')
        products = self._cur.fetchall()
        return products

    def delete_from_cart(self, product_data: tuple) -> None:
        try:
            with self._conn:
                self._cur.execute('DELETE FROM shopping_cart WHERE product_name = ? AND product_description = ? AND product_prive = ?',
                                product_data)
        except Exception as ex:
            logger.critical(f'Exception has been found: {ex}')
            
    def empty_shopping_cart(self) -> None:
        '''
            Will be executed one the user checks out.
        '''
        try:
            with self._conn:
                self._cur.execute(f'DELETE FROM shopping_cart')
        except Exception as ex:
            logger.critical(f'Exception has found: {ex}')
        
manager = DatabaseManager()

