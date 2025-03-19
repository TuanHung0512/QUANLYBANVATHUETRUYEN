import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QFormLayout, QTableWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate

class QLTT(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("giaodien/qltt.ui", self)
        self.connect_db()
        self.load_data()
        
        # Kết nối các nút với chức năng
        self.btn_taodt.clicked.connect(self.open_form_tao_don_thue)
        self.btn_tratruyen.clicked.connect(self.open_form_tra_truyen)
        self.btn_ctthue.clicked.connect(self.open_form_xem_chi_tiet)
        self.btn_suadt.clicked.connect(self.sua_don_thue)
        self.btn_xoadt.clicked.connect(self.xoa_donthue)
        self.btn_timkiemtt.clicked.connect(self.tim_kiem_donthue)
        self.btn_quaylai3.clicked.connect(self.quay_lai3)
    
    def quay_lai3(self):
        from main import Main_Ui
        self.hide()
        self.main_ui = Main_Ui()
        self.main_ui.show()

    def connect_db(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ql_truyen"
        )
        self.cursor = self.conn.cursor()

    def load_data(self):
        """ Load lại dữ liệu từ database vào tableWidget """
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen")
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT tbdonthue.madonthue, tbkhachhang.tenkhach, tbdonthue.ngaythue, tbdonthue.ngaytra, tbdonthue.tongtien, tbdonthue.tinhtrang 
            FROM tbdonthue 
            JOIN tbkhachhang ON tbdonthue.makhach = tbkhachhang.makhach
        """)
            rows = cursor.fetchall()
        
            self.tableWidget.clearContents()  # Xóa toàn bộ dữ liệu cũ
            self.tableWidget.setRowCount(0)   # Đặt lại số dòng về 0
            self.tableWidget.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        
            self.tableWidget.repaint()  # Cập nhật lại giao diện
        
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            cursor.close()
            conn.close()

    def xoa_donthue(self):
        try:
            # Lấy đơn thuê đang được chọn trên tableWidget
            selected_row = self.tableWidget.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đơn thuê để xóa.")
                return       
            madonthue = self.tableWidget.item(selected_row, 0).text()  # Cột 0 là mã đơn thuê       
            # Hỏi xác nhận trước khi xóa
            reply = QMessageBox.question(self, "Xác nhận xóa", "Bạn có chắc chắn muốn xóa đơn thuê này?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No) 
            if reply == QMessageBox.StandardButton.No:
                return  # Không xóa nếu người dùng chọn "No"
            # Kiểm tra kết nối trước khi thực hiện truy vấn
            if not self.conn.is_connected():
                self.connect_db()  # Kết nối lại nếu bị mất
            # Xóa đơn thuê khỏi database
            self.cursor.execute("DELETE FROM tbdonthue WHERE madonthue = %s", (madonthue,))
            self.conn.commit()
            # Xóa dòng trên tableWidget
            self.tableWidget.removeRow(selected_row)
            QMessageBox.information(self, "Thành công", "Đã xóa đơn thuê thành công!")   
        except Exception as e:
            QMessageBox.critical(self, "Lỗi khi xóa đơn thuê", str(e))
        
    def tim_kiem_donthue(self):
        tu_khoa = self.lineEditThueTruyen.text().strip()  # Lấy nội dung từ ô tìm kiếm
        if not tu_khoa:
            self.load_data()  # Gọi lại hàm load tất cả đơn thuê
            so_luong = self.tableWidget.rowCount()
            QMessageBox.information(self, "Kết quả tìm kiếm", f"Tìm thấy {so_luong} đơn thuê.")
            return
        try:
            self.connect_db()  # Kết nối database
            query = """SELECT tbdonthue.madonthue, tbkhachhang.tenkhach, tbdonthue.ngaythue, 
                              tbdonthue.ngaytra, tbdonthue.tongtien, tbdonthue.tinhtrang
                        FROM tbdonthue
                        JOIN tbkhachhang ON tbdonthue.makhach = tbkhachhang.makhach
                        WHERE tbdonthue.madonthue = %s"""         
            self.cursor.execute(query, (tu_khoa,))  # Truy vấn dữ liệu
            ket_qua = self.cursor.fetchall()
            self.tableWidget.setRowCount(0)  # Xóa dữ liệu cũ
            if ket_qua:
                for row_number, row_data in enumerate(ket_qua):
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            else:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy đơn thuê nào!")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tìm kiếm đơn thuê: {str(e)}")
        finally:
            self.cursor.close()
            self.conn.close()

    def open_form_tao_don_thue(self):
        """ Mở form nhập đơn thuê mới """
        form = FormTaoDonThue(self)
        form.exec()
    
    def sua_don_thue(self):
        """ Mở form sửa đơn thuê khi nhấn nút """
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một đơn thuê để sửa!")
            return
    
        madonthue = self.tableWidget.item(selected_row, 0).text()  # Lấy mã đơn thuê
        self.form_sua_don_thue = FormSuaDonThue(self, madonthue)
        self.form_sua_don_thue.exec()  # Hiển thị form sửa

    
    def open_form_tra_truyen(self):
        """ Mở form trả truyện khi chọn một đơn thuê """
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đơn thuê!")
            return
        madonthue = self.tableWidget.item(selected_row, 0).text()
        form = FormTraTruyen(self, madonthue)
        form.exec()
    
    def open_form_xem_chi_tiet(self):
        """ Mở form xem chi tiết đơn thuê """
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đơn thuê!")
            return
        madonthue = self.tableWidget.item(selected_row, 0).text()
        form = FormXemChiTiet(self, madonthue)
        form.exec()

class FormTaoDonThue(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Tạo Đơn Thuê")
        self.layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.madonthue = QLineEdit()
        self.makhach = QLineEdit()
        self.ngaythue = QDateEdit()
        self.ngaytra = QDateEdit()
        self.tongtien = QLineEdit()
        
        form_layout.addRow("Mã đơn thuê:", self.madonthue)
        form_layout.addRow("Mã khách:", self.makhach)
        form_layout.addRow("Ngày thuê:", self.ngaythue)
        form_layout.addRow("Ngày trả:", self.ngaytra)
        form_layout.addRow("Tổng tiền:", self.tongtien)

        self.btn_tao = QPushButton("Tạo")
        self.btn_tao.clicked.connect(self.tao_don_thue)

        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.btn_tao)
        self.setLayout(self.layout)

    def tao_don_thue(self):
        """ Xử lý tạo đơn thuê (kiểm tra trùng madonthue) """
        madonthue = self.madonthue.text()
        makhach = self.makhach.text()
        ngaythue = self.ngaythue.date().toString("yyyy-MM-dd")
        ngaytra = self.ngaytra.date().toString("yyyy-MM-dd")
        tongtien = self.tongtien.text()

        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen")
        cursor = conn.cursor()

        try:
            # Kiểm tra xem madonthue đã tồn tại chưa
            cursor.execute("SELECT COUNT(*) FROM tbdonthue WHERE madonthue = %s", (madonthue,))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Lỗi", "Mã đơn thuê đã tồn tại!")
                return

            # Nếu không trùng, thêm vào database
            cursor.execute("""
                INSERT INTO tbdonthue (madonthue, makhach, ngaythue, ngaytra, tongtien, tinhtrang) 
                VALUES (%s, %s, %s, %s, %s, 'Đang thuê')
            """, (madonthue, makhach, ngaythue, ngaytra, tongtien))
            conn.commit()
        
            QMessageBox.information(self, "Thành công", "Đã tạo đơn thuê thành công!")
            self.close()
        
            # Load lại dữ liệu ngay lập tức
            self.parent().load_data()
        
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tạo đơn thuê: {e}")
        finally:
            cursor.close()
            conn.close()

class FormSuaDonThue(QDialog):
    def __init__(self, parent, madonthue):
        super().__init__(parent)
        self.setWindowTitle("Sửa Đơn Thuê")
        self.setFixedSize(400, 300)
        self.madonthue = madonthue  # Lưu mã đơn thuê cần sửa
        self.initUI()
        self.load_data()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_makhach = QLabel("Mã Khách:")
        self.makhach = QLineEdit()
        layout.addWidget(self.label_makhach)
        layout.addWidget(self.makhach)

        self.label_ngaythue = QLabel("Ngày Thuê:")
        self.ngaythue = QDateEdit()
        self.ngaythue.setCalendarPopup(True)
        layout.addWidget(self.label_ngaythue)
        layout.addWidget(self.ngaythue)

        self.label_ngaytra = QLabel("Ngày Trả:")
        self.ngaytra = QDateEdit()
        self.ngaytra.setCalendarPopup(True)
        layout.addWidget(self.label_ngaytra)
        layout.addWidget(self.ngaytra)

        self.label_tongtien = QLabel("Tổng Tiền:")
        self.tongtien = QLineEdit()
        layout.addWidget(self.label_tongtien)
        layout.addWidget(self.tongtien)

        self.btn_luu = QPushButton("Lưu Thay Đổi")
        self.btn_luu.clicked.connect(self.luu_thay_doi)
        layout.addWidget(self.btn_luu)

        self.setLayout(layout)

    def load_data(self):
        """ Load thông tin đơn thuê từ database để sửa """
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT makhach, ngaythue, ngaytra, tongtien FROM tbdonthue WHERE madonthue = %s", (self.madonthue,))
            row = cursor.fetchone()
            if row:
                self.makhach.setText(str(row[0]))
                self.ngaythue.setDate(QDate.fromString(str(row[1]), "yyyy-MM-dd"))
                self.ngaytra.setDate(QDate.fromString(str(row[2]), "yyyy-MM-dd"))
                self.tongtien.setText(str(row[3]))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            cursor.close()
            conn.close()

    def luu_thay_doi(self):
        """ Lưu thông tin sửa đổi vào database """
        makhach = self.makhach.text()
        ngaythue = self.ngaythue.date().toString("yyyy-MM-dd")
        ngaytra = self.ngaytra.date().toString("yyyy-MM-dd")
        tongtien = self.tongtien.text()

        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE tbdonthue 
                SET makhach = %s, ngaythue = %s, ngaytra = %s, tongtien = %s
                WHERE madonthue = %s
            """, (makhach, ngaythue, ngaytra, tongtien, self.madonthue))
            conn.commit()

            QMessageBox.information(self, "Thành công", "Đã sửa đơn thuê thành công!")
            self.close()
            self.parent().load_data()  # Load lại danh sách đơn thuê
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi sửa đơn thuê: {e}")
        finally:
            cursor.close()
            conn.close()

class FormTraTruyen(QDialog):
    def __init__(self, parent, madonthue):
        super().__init__(parent)
        self.setWindowTitle("Trả Truyện")
        self.madonthue = madonthue
        self.layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.machitiet = QLineEdit()
        self.matruyen = QLineEdit()
        self.soluong = QLineEdit()
        self.ngaythue = QDateEdit()
        self.ngaytra = QDateEdit()

        form_layout.addRow("Mã chi tiết:", self.machitiet)
        form_layout.addRow("Mã truyện:", self.matruyen)
        form_layout.addRow("Số lượng:", self.soluong)
        form_layout.addRow("Ngày thuê:", self.ngaythue)
        form_layout.addRow("Ngày trả:", self.ngaytra)

        self.btn_tra = QPushButton("Xác nhận trả")
        self.btn_tra.clicked.connect(self.tra_truyen)

        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.btn_tra)
        self.setLayout(self.layout)

    def tra_truyen(self):
        """ Xử lý trả truyện """
        machitiet = self.machitiet.text()
        matruyen = self.matruyen.text()
        soluong = self.soluong.text()
        ngaythue = self.ngaythue.date().toString("yyyy-MM-dd")
        ngaytra = self.ngaytra.date().toString("yyyy-MM-dd")

        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen")
        cursor = conn.cursor()
        try:
            # Thêm vào bảng tbchitietdonthue
            cursor.execute("""
                INSERT INTO tbchitietdonthue (machitiet, madonthue, matruyen, soluong, ngaythue, ngaytra, tinhtrang)
                VALUES (%s, %s, %s, %s, %s, %s, 'Đã trả')
            """, (machitiet, self.madonthue, matruyen, soluong, ngaythue, ngaytra))

            # Cập nhật trạng thái đơn thuê thành "Đã trả" nếu tất cả truyện đã trả
            cursor.execute("""
                UPDATE tbdonthue 
                SET tinhtrang = 'Đã trả' 
                WHERE madonthue = %s
            """, (self.madonthue,))
            
            conn.commit()
            QMessageBox.information(self, "Thành công", "Đã trả truyện thành công!")
            self.close()
            self.parent().load_data()  # Cập nhật lại tableWidget trên giao diện chính
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi trả truyện: {e}")
        finally:
            cursor.close()
            conn.close()

class FormXemChiTiet(QDialog):
    def __init__(self, parent, madonthue):
        super().__init__(parent)
        self.setWindowTitle("Chi Tiết Đơn Thuê")
        self.madonthue = madonthue
        self.layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["Mã chi tiết", "Mã đơn thuê", "Tên truyện", "Số lượng", "Ngày thuê", "Ngày trả", "Tình trạng"])

        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.load_data()

    def load_data(self):
        """ Load dữ liệu chi tiết đơn thuê """
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT ct.machitiet, ct.madonthue, t.tentruyen, ct.soluong, ct.ngaythue, ct.ngaytra, ct.tinhtrang
                FROM tbchitietdonthue ct
                JOIN tbtruyen t ON ct.matruyen = t.matruyen
                WHERE ct.madonthue = %s
            """, (self.madonthue,))
            rows = cursor.fetchall()
            self.tableWidget.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QLTT()
    window.show()
    sys.exit(app.exec())
