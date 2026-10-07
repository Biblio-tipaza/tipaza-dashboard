import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
import webbrowser

CONFIG_FILE = "systems.json"
BG_IMAGE_FILE = "logo.png"


class CentralDashboard(QMainWindow):

  def __init__(self):
    super().__init__()
    self.setWindowTitle("لوحة التحكم المركزية للأنظمة والمنصات")
    self.resize(1100, 750)

    self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    self.systems = []
    self.load_systems()

    # تحميل الشعار للخلفية
    self.bg_pixmap = QPixmap(BG_IMAGE_FILE)

    self.init_ui()

  def load_systems(self):
    if os.path.exists(CONFIG_FILE):
      try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
          self.systems = json.load(f)
      except Exception:
        self.systems = []
    else:
      self.systems = []
      self.save_systems()

  def save_systems(self):
    try:
      with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(self.systems, f, ensure_ascii=False, indent=4)
    except Exception as e:
      QMessageBox.critical(self, "خطأ", f"تعذر حفظ التغييرات: {e}")

  def paintEvent(self, event):
    """رسم خلفية زرقاء موحدة مع عرض الشعار في المنتصف بشفافية"""
    painter = QPainter(self)
    painter.fillRect(self.rect(), QColor("#1b3b42"))  # لون خلفية متناسق

    if not self.bg_pixmap.isNull():
      window_width = self.width()
      window_height = self.height()

      scaled_pixmap = self.bg_pixmap.scaled(
          int(window_width * 0.55),
          int(window_height * 0.55),
          Qt.AspectRatioMode.KeepAspectRatio,
          Qt.TransformationMode.SmoothTransformation,
      )

      x = (window_width - scaled_pixmap.width()) // 2
      y = (window_height - scaled_pixmap.height()) // 2

      painter.setOpacity(
          0.2
      )  # جعل الشعار خفيفاً في الخلفية لكي يظهر المحتوى فوقه بوضوح
      painter.drawPixmap(x, y, scaled_pixmap)

    super().paintEvent(event)

  def init_ui(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)

    # تخطيط رئيسي لتموضع النافذة المنبثقة في المنتصف تماماً
    outer_layout = QVBoxLayout(central_widget)
    outer_layout.setContentsMargins(50, 40, 50, 40)

    # إنشاء النافذة المنبثقة المركزية (Modal/Card)
    modal_card = QWidget()
    modal_card.setStyleSheet("""
            QWidget {
                background-color: rgba(27, 59, 66, 0.88);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }
        """)

    modal_layout = QVBoxLayout(modal_card)
    modal_layout.setContentsMargins(30, 30, 30, 30)
    modal_layout.setSpacing(20)

    # --- الشريط العلوي داخل النافذة المنبثقة ---
    header_layout = QHBoxLayout()

    add_btn = QPushButton("➕ إضافة نظام جديد")
    add_btn.setFont(QFont("Cairo", 10, QFont.Weight.Bold))
    add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    add_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1c40f;
                color: #2c3e50;
                padding: 8px 16px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #f39c12;
            }
        """)
    add_btn.clicked.connect(self.add_new_system)

    title_label = QLabel("لوحة التحكم المركزية للأنظمة والمنصات")
    title_label.setFont(QFont("Cairo", 13, QFont.Weight.Bold))
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet("color: #ffffff; border: none; background: none;")

    header_layout.addWidget(add_btn)
    header_layout.addStretch()
    header_layout.addWidget(title_label)
    header_layout.addStretch()

    # إضافة عنصر وهمي لتوازن المسافات
    dummy_widget = QWidget()
    dummy_widget.setFixedWidth(130)
    dummy_widget.setStyleSheet("background: none; border: none;")
    header_layout.addWidget(dummy_widget)

    modal_layout.addLayout(header_layout)

    # --- منطقة التمرير للأنظمة داخل النافذة المنبثقة ---
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("background: transparent; border: none;")

    scroll_content = QWidget()
    scroll_content.setStyleSheet("background: transparent; border: none;")
    self.grid_layout = QGridLayout(scroll_content)
    self.grid_layout.setSpacing(15)
    self.grid_layout.setContentsMargins(10, 10, 10, 10)

    scroll_area.setWidget(scroll_content)
    modal_layout.addWidget(scroll_area)

    # وضع النافذة المنبثقة في منتصف الشاشة الخارجية
    outer_layout.addStretch()
    outer_layout.addWidget(modal_card)
    outer_layout.addStretch()

    self.populate_grid()

  def populate_grid(self):
    for i in reversed(range(self.grid_layout.count())):
      widget = self.grid_layout.itemAt(i).widget()
      if widget:
        widget.setParent(None)

    row, col = 0, 0
    max_columns = 4

    color_themes = [
        {"bg": "#a593e0", "border": "#8573c0", "text": "#ffffff"},
        {"bg": "#27ae60", "border": "#1e8449", "text": "#ffffff"},
        {"bg": "#3498db", "border": "#2980b9", "text": "#ffffff"},
        {"bg": "#e67e22", "border": "#d35400", "text": "#ffffff"},
        {"bg": "#1abc9c", "border": "#16a085", "text": "#ffffff"},
        {"bg": "#e74c3c", "border": "#c0392b", "text": "#ffffff"},
        {"bg": "#f1c40f", "border": "#d4ac0d", "text": "#2c3e50"},
        {"bg": "#7f8c8d", "border": "#616a6b", "text": "#ffffff"},
    ]

    for index, sys_info in enumerate(self.systems):
      btn = QPushButton(f"{sys_info.get('icon', '💻')}\n\n{sys_info['name']}")
      btn.setFont(QFont("Cairo", 10, QFont.Weight.Bold))
      btn.setFixedSize(200, 110)
      btn.setCursor(Qt.CursorShape.PointingHandCursor)

      theme = color_themes[index % len(color_themes)]
      style = (
          "QPushButton {"
          f"    background-color: {theme['bg']};"
          f"    color: {theme['text']};"
          "    border: 2px solid rgba(255, 255, 255, 0.4);"
          f"    border-bottom: 4px solid {theme['border']};"
          "    border-radius: 10px;"
          "    text-align: center;"
          "    padding: 10px;"
          "}"
          "QPushButton:hover {"
          "    border-color: #ffffff;"
          "}"
      )
      btn.setStyleSheet(style)

      url = sys_info["url"]
      btn.clicked.connect(lambda checked, u=url: webbrowser.open(u))

      self.grid_layout.addWidget(btn, row, col)
      col += 1
      col %= max_columns
      if col == 0:
        row += 1

  def add_new_system(self):
    name, ok1 = QInputDialog.getText(self, "إضافة نظام جديد", "أدخل اسم النظام:")
    if not ok1 or not name.strip():
      return

    url, ok2 = QInputDialog.getText(
        self, "إضافة نظام جديد", "أدخل رابط النظام (URL):"
    )
    if not ok2 or not url.strip():
      return

    icon, ok3 = QInputDialog.getText(
        self, "إضافة نظام جديد", "أدخل رمز تعبيري (Emoji) للأيقونة:", text="📁"
    )
    if not ok3:
      icon = "📁"

    new_sys = {
        "name": name.strip(),
        "url": url.strip(),
        "icon": icon.strip() if icon.strip() else "📁",
    }

    self.systems.append(new_sys)
    self.save_systems()
    self.populate_grid()

    QMessageBox.information(self, "نجاح", "تمت إضافة النظام وتحديث اللوحة بنجاح!")


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = CentralDashboard()
  window.show()
  sys.exit(app.exec())
