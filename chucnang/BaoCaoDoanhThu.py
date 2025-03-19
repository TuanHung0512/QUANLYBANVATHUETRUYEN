import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class BCDT(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Báo Cáo Doanh Thu")
        self.setGeometry(100, 100, 400, 250)

        self.layout = QVBoxLayout()

        # Các nhãn hiển thị doanh thu
        self.label_ban = QLabel("Doanh thu bán: Đang tải...")
        self.label_thue = QLabel("Doanh thu thuê: Đang tải...")
        self.label_tong = QLabel("Tổng doanh thu: Đang tải...")

        # Nút làm mới
        self.btn_capnhat = QPushButton("Làm mới")
        self.btn_capnhat.clicked.connect(self.load_doanh_thu)

        # Nút quay lại
        self.btn_quaylai5 = QPushButton("Quay lại")
        self.btn_quaylai5.clicked.connect(self.open_bc)

         

        # Thêm vào layout
        self.layout.addWidget(self.label_ban)
        self.layout.addWidget(self.label_thue)
        self.layout.addWidget(self.label_tong)
        self.layout.addWidget(self.btn_capnhat)
        self.layout.addWidget(self.btn_quaylai5)  # Nút quay lại nằm dưới cùng

        self.setLayout(self.layout)

        # Tải dữ liệu ngay khi mở giao diện
        self.load_doanh_thu()
    
    def open_bc(self):
           from main import Main_Ui
           self.hide()
           self.main_ui = Main_Ui()
           self.main_ui.show()

    def load_doanh_thu(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ql_truyen"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT SUM(thanhtien) FROM tbchitietdonban")
            doanhthu_ban = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(tongtien) FROM tbdonthue")
            doanhthu_thue = cursor.fetchone()[0] or 0

            doanhthu_tong = doanhthu_ban + doanhthu_thue

            self.label_ban.setText(f"Doanh thu bán: {doanhthu_ban:,} VNĐ")
            self.label_thue.setText(f"Doanh thu thuê: {doanhthu_thue:,} VNĐ")
            self.label_tong.setText(f"Tổng doanh thu: {doanhthu_tong:,} VNĐ")

            cursor.close()
            conn.close()
        except Exception as e:
            self.label_tong.setText(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BCDT()
    window.show()
    sys.exit(app.exec())
