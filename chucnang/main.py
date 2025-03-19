import sys
import mysql.connector
from PyQt6 import QtWidgets, uic
from qltruyen import QLT
from qlkhachhang import QLKH
from qlthuetruyen import QLTT
from qlbantruyen import QLBT
from BaoCaoDoanhThu import BCDT

class Main_Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main_Ui, self).__init__()
        uic.loadUi('giaodien/home.ui', self)
         # Kết nối với MySQL++++++
        self.connect_database()
        self.parent = parent
        self.show()
        self.btn_qlt.clicked.connect(self.open_qlt)
        self.btn_qlkh.clicked.connect(self.open_qlkh)
        self.btn_qltt.clicked.connect(self.open_qltt)
        self.btn_qlbt.clicked.connect(self.open_qlbt)
        self.btn_bcdt.clicked.connect(self.open_bcdt)

    
    def connect_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",       # Thay bằng user của bạn nếu khác
                password="",       # Nếu có mật khẩu thì điền vào
                database="ql_truyen"
            )
        except mysql.connector.Error:
            pass  


    def open_qlt(self):
        self.qlt = QLT()
        self.qlt.show()
        self.close()
    
    def open_qlkh(self):
        self.qlkh = QLKH()
        self.qlkh.show()
        self.close()
    
    def open_qltt(self):
        self.qltt = QLTT()
        self.qltt.show()
        self.close()
    
    def open_qlbt(self):
        self.qlbt = QLBT()
        self.qlbt.show()
        self.close()
    
    def open_bcdt(self):
        self.qlbcdt = BCDT()
        self.qlbcdt.show()
        self.close()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main_Ui()
    window.show()
    sys.exit(app.exec())
