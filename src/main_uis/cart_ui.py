from src.base_uis.shopping_cart import Ui_MainWindow
from src.database_manager import manager
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from .product_ui import ProductUiWindow 
from src.logger_conf import logger

class ShoppingCartUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_shopping_cart()
        self.ui.returnButton.clicked.connect(self.remove_product_button)
        self.ui.purchaseButton.clicked.connect(self.purchase)
        self.ui.backButton.clicked.connect(self.show_product_page)

    def show_message(self, message: str, level) -> None:
        msg = QMessageBox()
        msg.setIcon(level) 
        msg.setWindowTitle("Success")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def load_shopping_cart(self) -> None:
        self.products = manager.load_shopping_cart_db()
        for product in self.products:
            self.ui.cartList.addItem(str(product[0]))

    def remove_product_button(self) -> None:
        current_row = self.ui.cartList.currentRow()
        manager.delete_from_cart(self.products[current_row])
        self.ui.cartList.clear()
        self.load_shopping_cart()
        self.show_message(message = 'Successfully removed product!', level = QMessageBox.Information)


    def purchase(self) -> None:
        try:
            manager.empty_shopping_cart()
        except Exception as ex:
            logger.critical(f'Problem occured while emptying: {ex}')
        self.ui.cartList.clear()
        self.load_shopping_cart()
        self.show_message(message = 'Successfully checked out!', level = QMessageBox.Information)
        
        
    def show_product_page(self) -> None:
        self.product_window = ProductUiWindow()
        self.product_window.show()
        self.close()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ShoppingCartUi()
    window.show()
    sys.exit(app.exec_())
