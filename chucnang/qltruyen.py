import sys
import mysql.connector
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QLabel, QPushButton, QVBoxLayout

class FormTruyen(QtWidgets.QDialog):
    def __init__(self, parent=None, matruyen="", tentruyen="", theloai="", tacgia="", soluong="", dongia="", giathue="", ngayphathanh=""):
        super(FormTruyen, self).__init__(parent)
        self.setWindowTitle("Thông tin truyện")
        
        layout = QVBoxLayout()
        
        self.lineEditMaTruyen = QLineEdit(matruyen)
        self.lineEditTenTruyen = QLineEdit(tentruyen)
        self.lineEditTheLoai = QLineEdit(theloai)
        self.lineEditTacGia = QLineEdit(tacgia)
        self.lineEditSoLuong = QLineEdit(soluong)
        self.lineEditDongGia = QLineEdit(dongia)
        self.lineEditGiaThue = QLineEdit(giathue)
        self.lineEditNgayPhatHanh = QLineEdit(ngayphathanh)
        self.btnLuu = QPushButton("Lưu")
        self.btnHuy = QPushButton("Hủy")
        
        layout.addWidget(QLabel("Mã Truyện"))
        layout.addWidget(self.lineEditMaTruyen)
        layout.addWidget(QLabel("Tên Truyện"))
        layout.addWidget(self.lineEditTenTruyen)
        layout.addWidget(QLabel("Thể loại"))
        layout.addWidget(self.lineEditTheLoai)
        layout.addWidget(QLabel("Tác Giả"))
        layout.addWidget(self.lineEditTacGia)
        layout.addWidget(QLabel("Số Lượng"))
        layout.addWidget(self.lineEditSoLuong)
        layout.addWidget(QLabel("Đồng Giá"))
        layout.addWidget(self.lineEditDongGia)
        layout.addWidget(QLabel("Giá Thuê"))
        layout.addWidget(self.lineEditGiaThue)
        layout.addWidget(QLabel("Ngày Hành"))
        layout.addWidget(self.lineEditNgayPhatHanh)

        layout.addWidget(self.btnLuu)
        layout.addWidget(self.btnHuy)
        
        self.setLayout(layout)
        
        self.btnLuu.clicked.connect(self.accept)
        self.btnHuy.clicked.connect(self.reject)
    
    def get_data(self):
        return (
            self.lineEditMaTruyen.text(),
            self.lineEditTenTruyen.text(),
            self.lineEditTheLoai.text(),
            self.lineEditTacGia.text(),
            self.lineEditSoLuong.text(),
            self.lineEditDongGia.text(),
            self.lineEditGiaThue.text(),
            self.lineEditNgayPhatHanh.text(),
        )

class QLT(QtWidgets.QMainWindow):
    def __init__(self):
        super(QLT, self).__init__()
        uic.loadUi("giaodien/qlt.ui", self)
        
        self.connect_database()
        self.load_data()
        
        self.btn_themt.clicked.connect(self.them_truyen)
        self.btn_suat.clicked.connect(self.sua_truyen)
        self.btn_xoat.clicked.connect(self.xoa_truyen)
        self.btn_timkiemt.clicked.connect(self.tim_kiem_truyen)
        self.btn_quaylai1.clicked.connect(self.quay_lai1)

    def quay_lai1(self):
        from main import Main_Ui
        self.hide()
        self.main_ui = Main_Ui()
        self.main_ui.show()
        
    def connect_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ql_truyen"  # Sửa thành dbbanhang theo ảnh
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
    
    def load_data(self):
        query = "SELECT matruyen, tentruyen, theloai, tacgia, soluong, dongia, giathue, ngayphathanh FROM tbtruyen"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.fill_table(rows)
    
    def fill_table(self, rows):
        self.tableWidget.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(cell_data)))
    
    def them_truyen(self):
        form = FormTruyen(self)
        if not form.exec():  # Nếu form bị hủy, thoát khỏi hàm
            return
        
        if form.exec():
            matruyen, tentruyen, theloai, tacgia, soluong, dongia, giathue, ngayphathanh = form.get_data()
        
        # Kiểm tra trùng mã truyện
        self.cursor.execute("SELECT COUNT(*) FROM tbtruyen WHERE matruyen = %s", (matruyen,))
        if self.cursor.fetchone()[0] > 0:
            QMessageBox.warning(self, "Lỗi", "Mã truyện đã tồn tại!")
            return
        
        # Kiểm tra trùng tên truyện
        self.cursor.execute("SELECT COUNT(*) FROM tbtruyen WHERE tentruyen = %s", (tentruyen,))
        if self.cursor.fetchone()[0] > 0:
            QMessageBox.warning(self, "Lỗi", "Tên truyện đã tồn tại!")
            return
        
        query = "INSERT INTO tbtruyen (matruyen, tentruyen, theloai, tacgia, soluong, dongia, giathue, ngayphathanh) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (matruyen, tentruyen, theloai, tacgia, soluong, dongia, giathue, ngayphathanh))
        self.db.commit()
        self.load_data()
        QMessageBox.information(self, "Thành công", "Thêm truyện thành công!")

    def sua_truyen(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
           matruyen = self.tableWidget.item(selected_row, 0).text()
           tentruyen_cu = self.tableWidget.item(selected_row, 1).text()

        form = FormTruyen(self, matruyen, tentruyen_cu)
        if form.exec():
            tentruyen_moi, theloai, tacgia, soluong, dongia, giathue, ngayphathanh = form.get_data()[1:]

            # Kiểm tra trùng tên truyện (trừ chính nó)
            self.cursor.execute("SELECT COUNT(*) FROM tbtruyen WHERE tentruyen = %s AND matruyen != %s", (tentruyen_moi, matruyen))
            if self.cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Lỗi", "Tên truyện đã tồn tại!")
                return

            query = "UPDATE tbtruyen SET tentruyen=%s, theloai=%s, tacgia=%s, soluong=%s, dongia=%s, giathue=%s, ngayphathanh=%s WHERE matruyen=%s"
            self.cursor.execute(query, (tentruyen_moi, theloai, tacgia, soluong, dongia, giathue, ngayphathanh, matruyen))
            self.db.commit()
            self.load_data()
            QMessageBox.information(self, "Thành công", "Sửa truyện thành công!")


    def xoa_truyen(self):
        if not hasattr(self, "tableWidget"):
            return
        
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            mahang = self.tableWidget.item(selected_row, 0).text()
            confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa mặt hàng này?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                query = "DELETE FROM tbtruyen WHERE matruyen=%s"
                self.cursor.execute(query, (mahang,))
                self.db.commit()
                self.load_data()
                QMessageBox.information(self, "Thành công", "Xóa mặt hàng thành công!")

    def tim_kiem_truyen(self):
        if not hasattr(self, "lineEditTenTruyen"):
            return

        line_edit = self.findChild(QLineEdit, "lineEditTenTruyen")
        if line_edit is None:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy ô nhập liệu tìm kiếm!")
            return
        
        tentruyen = line_edit.text()
        query = "SELECT matruyen, tentruyen, theloai, tacgia, soluong, dongia, giathue, ngayphathanh FROM tbtruyen WHERE tentruyen LIKE %s"
        self.cursor.execute(query, ("%" + tentruyen + "%",))
        rows = self.cursor.fetchall()
        self.fill_table(rows)
        QMessageBox.information(self, "Kết quả", f"Tìm thấy {len(rows)} kết quả!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QLT()
    window.show()
    sys.exit(app.exec())