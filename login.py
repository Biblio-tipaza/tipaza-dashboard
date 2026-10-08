import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QLineEdit, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPainterPath

# استيراد واجهة لوحة التحكم من ملف app.py
from app import CentralDashboard

BG_IMAGE_FILE = "logo.png"

class BackgroundWidget(QWidget):
    """خلفية مخصصة لملء الجوانب بلون الأزرق وعرض الشعار في المنتصف"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bg_pixmap = QPixmap(BG_IMAGE_FILE)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#225c68"))
        
        if not self.bg_pixmap.isNull():
            window_width = self.width()
            window_height = self.height()
            
            scaled_pixmap = self.bg_pixmap.scaled(
                window_width, window_height, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            x = (window_width - scaled_pixmap.width()) // 2
            y = (window_height - scaled_pixmap.height()) // 2
            
            painter.setOpacity(0.35)
            painter.drawPixmap(x, y, scaled_pixmap)
            
        super().paintEvent(event)

class CircularLabel(QLabel):
    """مكون مخصص لرسم الصورة بشكل دائري مثالي"""
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.pixmap_image = QPixmap(image_path)
        self.setFixedSize(90, 90)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, self.width(), self.height()))
        painter.setClipPath(path)
        
        if not self.pixmap_image.isNull():
            scaled = self.pixmap_image.scaled(
                self.width(), self.height(), 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)
        else:
            painter.fillRect(self.rect(), QColor("#2c3e50"))

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل الدخول - لوحة التحكم المركزية")
        self.resize(550, 650)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.dashboard = None  # مرجع لتخزين نافذة اللوحة الرئيسية
        self.init_ui()

    def init_ui(self):
        central_widget = BackgroundWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        card = QWidget(central_widget)
        card.setFixedSize(440, 490)
        card.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 80))
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        card_layout.setContentsMargins(30, 20, 30, 20)
        card_layout.setSpacing(12)
        
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        circular_logo = CircularLabel(BG_IMAGE_FILE, card)
        logo_layout.addWidget(circular_logo)
        card_layout.addLayout(logo_layout)
        
        title_label = QLabel("لوحة التحكم المركزية للأنظمة والمنصات", card)
        title_label.setFont(QFont("Cairo", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; background: transparent; border: none;")
        card_layout.addWidget(title_label)
        
        subtitle_label = QLabel("جامعة تيبازة", card)
        subtitle_label.setFont(QFont("Cairo", 9))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; background: transparent; border: none;")
        card_layout.addWidget(subtitle_label)
        
        card_layout.addSpacing(5)
        
        user_label = QLabel("👤 اسم المستخدم:", card)
        user_label.setFont(QFont("Cairo", 10, QFont.Weight.Bold))
        user_label.setStyleSheet("color: #2c3e50; background: transparent; border: none;")
        card_layout.addWidget(user_label)
        
        self.username_input = QLineEdit(card)
        self.username_input.setPlaceholderText("أدخل اسم المستخدم...")
        self.username_input.setFont(QFont("Cairo", 10))
        self.username_input.setFixedHeight(38)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 5px 10px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        card_layout.addWidget(self.username_input)
        
        pass_label = QLabel("🔒 كلمة المرور:", card)
        pass_label.setFont(QFont("Cairo", 10, QFont.Weight.Bold))
        pass_label.setStyleSheet("color: #2c3e50; background: transparent; border: none;")
        card_layout.addWidget(pass_label)
        
        self.password_input = QLineEdit(card)
        self.password_input.setPlaceholderText("أدخل كلمة المرور...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Cairo", 10))
        self.password_input.setFixedHeight(38)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 5px 10px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #27ae60;
            }
        """)
        card_layout.addWidget(self.password_input)
        
        login_btn = QPushButton("تسجيل الدخول", card)
        login_btn.setFont(QFont("Cairo", 11, QFont.Weight.Bold))
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setFixedHeight(40)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 8px;
                border-bottom: 3px solid #1e8449;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                border-bottom: 1px solid #1e8449;
                padding-top: 2px;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)
        
        footer_card = QLabel("© 2026 جميع الحقوق محفوظة", card)
        footer_card.setFont(QFont("Cairo", 8))
        footer_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_card.setStyleSheet("color: #bdc3c7; background: transparent; border: none;")
        card_layout.addWidget(footer_card)
        
        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        
        exit_btn = QPushButton("🚪 الخروج", central_widget)
        exit_btn.setFont(QFont("Cairo", 11, QFont.Weight.Bold))
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.setFixedSize(180, 45)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4757;
                color: white;
                border-radius: 22px;
                border-bottom: 4px solid #ff6b81;
            }
            QPushButton:hover {
                background-color: #ff6b81;
            }
            QPushButton:pressed {
                border-bottom: 1px solid #ff4757;
                padding-top: 3px;
            }
        """)
        exit_btn.clicked.connect(self.close)
        
        main_layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        correct_user = "admin"
        correct_pass = "biblio/001"
        
        if not username or not password:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم المستخدم وكلمة المرور!")
            return
            
        if username == correct_user and password == correct_pass:
            QMessageBox.information(self, "نجاح", "مرحباً بك، تم تسجيل الدخول بنجاح!")
            
            # فتح واجهة لوحة التحكم الرئيسية
            self.dashboard = CentralDashboard()
            self.dashboard.show()
            
            # إغلاق نافذة تسجيل الدخول
            self.close()
        else:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
