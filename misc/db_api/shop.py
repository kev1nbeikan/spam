
from .sessions import DBBaseObject
from .product_handle import Product


class ShopDB(DBBaseObject):
    NAME_OF_TABLE = 'products'
    PRICE_LINE_NAME = 'price'
    NAME_PRODUCT_LINE_NAME = 'name'
    DAYS_LINE_NAME = 'days'
    IDENTIFIER_LINE = 'id'

    def making_table_shop(self, ):
        products = f'''CREATE TABLE IF NOT EXISTS {self.NAME_OF_TABLE}(
        {self.IDENTIFIER_LINE} INTEGER PRIMARY KEY AUTOINCREMENT,
        {self.NAME_PRODUCT_LINE_NAME} str NOT NULL,
        {self.DAYS_LINE_NAME} int NOT NULL,
        {self.PRICE_LINE_NAME} int NOT NULL);'''

        self.execute(products, commit=True)

    def add_product(self, id_: int = None, name: str = '', days: int = 0, price: int = 100):
        command = f'''INSERT INTO {self.NAME_OF_TABLE} VALUES(?, ?, ?, ?)'''

        self.execute(command, (id_, name, days, price), commit=True)

    def update_product(self, indentifier: int, name:str=None, price: int =None, days:int= None):
        command = f'UPDATE {self.NAME_OF_TABLE} SET {{}} WHERE {self.IDENTIFIER_LINE} = ?'
        lst_chang = []
        lst_values = []
        if name is not None:
            lst_chang.append(f'{self.NAME_PRODUCT_LINE_NAME} = ?')
            lst_values.append(name)

        if price is not None:
            lst_chang.append(f'{self.PRICE_LINE_NAME} = ?')
            lst_values.append(price)

        if days is not None:
            lst_chang.append(f'{self.DAYS_LINE_NAME} = ?')
            lst_values.append(days)

        if not lst_chang:
            return
        lst_values.append(indentifier)
        # print(command.format(', '.join(lst_chang)))
        self.execute(command.format(', '.join(lst_chang)), tuple(lst_values), commit=True)


    def get_product(self, id_: int):
        command = f'''SELECT * FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE} = ?;'''
        f = self.execute(command, (id_, ), fetch_one=True)

        return Product(*f)

    def get_products(self) -> list[Product]:
        command = f'''
                SELECT * FROM {self.NAME_OF_TABLE};
                        '''
        f = self.execute(command, fetch_all=True)

        return map(lambda x: Product(*x), f)

    def delete_product(self, id_: int):
        command = f'DELETE FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE} = ?'

        self.execute(command, (id_,), commit=True)


