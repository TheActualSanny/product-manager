from src.base_uis.product_window import Ui_MainWindow
from src.database_manager import manager
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from src.logger_conf import logger

class ProductUiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.productDescription.setWordWrap(True)
        self.ui.productDescription.setMinimumHeight(200)
        self.load_products()

        self.ui.gotoCart.clicked.connect(self.go_to_cart)
        self.ui.addtoCart.clicked.connect(self.add_to_cart)

    def load_products(self) -> None:
        '''
            Loads the products using the DatabaseManager instance
            directly into the UI.
        '''
        self.products = manager.load_products_from_db()

        for product in self.products:
            self.ui.productList.addItem(tuple(product.keys())[0])
        self.ui.productList.currentRowChanged.connect(self.display_product)

    def display_product(self, product_index: int) -> None:
        '''
            Loads the actual product data based on the
            changed row index.
        '''
        if product_index >= 0 and product_index < len(self.products):
            product = self.products[product_index]
            product_values = tuple(product.values())
            self.ui.productName .setText(tuple(product.keys())[0])
            self.ui.productDescription.setText(product_values[0][0])
            self.ui.productPrice.setText(str(product_values[0][1]))
    
    def add_to_cart(self) -> None:
        curr_index = self.ui.productList.currentRow()

        if curr_index >= 0:
            logger.debug(f'The data of the product added to cart is: {self.ui.productName.text()}, {self.ui.productDescription.text()}, {self.ui.productPrice.text()}')
            manager.insert_shopping_cart((self.ui.productName.text(), self.ui.productDescription.text(), int(self.ui.productPrice.text())))

    def go_to_cart(self) -> None:
        from src.main_uis.cart_ui import ShoppingCartUi
        self.shopping_cart = ShoppingCartUi()
        self.shopping_cart.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ProductUiWindow()
    window.show()
    sys.exit(app.exec_())
