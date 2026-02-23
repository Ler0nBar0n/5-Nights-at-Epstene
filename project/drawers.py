import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DrawerButton(QPushButton):
    # Классовая переменная для хранения коэффициента масштабирования
    scale_factor = 1.0
    
    def __init__(self, text, id, parent=None):
        super().__init__(text, parent)
        self.id = id
        self.setMinimumHeight(int(60 * DrawerButton.scale_factor))
        self.setMaximumHeight(int(80 * DrawerButton.scale_factor))
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()
        
        # Тень для кнопки
        self.update_shadow()
    
    @classmethod
    def update_scale_factor(cls, factor):
        """Обновить коэффициент масштабирования для всех кнопок"""
        cls.scale_factor = factor
    
    def update_shadow(self):
        """Обновить тень с учетом масштаба"""
        shadow = QGraphicsDropShadowEffect()
        blur = int(12 * DrawerButton.scale_factor)
        offset = int(2 * DrawerButton.scale_factor)
        shadow.setBlurRadius(blur)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, offset)
        self.setGraphicsEffect(shadow)
    
    def update_style(self):
        """Обновить стиль кнопки с учетом масштаба"""
        font_size = int(15 * DrawerButton.scale_factor)
        padding_x = int(16 * DrawerButton.scale_factor)
        padding_y = int(8 * DrawerButton.scale_factor)
        margin = int(4 * DrawerButton.scale_factor)
        radius = int(12 * DrawerButton.scale_factor)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: none;
                border-radius: {radius}px;
                font-size: {font_size}px;
                font-weight: 500;
                color: #333;
                padding: {padding_y}px {padding_x}px;
                text-align: left;
                margin: {margin}px 0px;
            }}
            QPushButton:hover {{
                background-color: #f5f5f7;
            }}
            QPushButton:pressed {{
                background-color: #e5e5ea;
            }}
        """)
        
        # Обновляем минимальную и максимальную высоту
        self.setMinimumHeight(int(60 * DrawerButton.scale_factor))
        self.setMaximumHeight(int(80 * DrawerButton.scale_factor))
        
        # Обновляем тень
        self.update_shadow()

class DrawerScrollArea(QScrollArea):
    """Область прокрутки для ящиков"""
    def __init__(self, temp_id, parent=None):
        super().__init__(parent)
        self.temp_id = temp_id
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Контейнер для кнопок
        self.container = QWidget()
        self.container.setStyleSheet("background-color: transparent;")
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setWidget(self.container)

        # Стиль для области прокрутки и скроллбара
        self.update_scroll_style()
    
    def update_scroll_style(self):
        """Обновить стиль скроллбара с учетом масштаба"""
        scale = DrawerButton.scale_factor
        scroll_width = int(6 * scale)
        scroll_radius = int(3 * scale)
        min_height = int(30 * scale)
        
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: transparent;
                width: {scroll_width}px;
                border-radius: {scroll_radius}px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: {scroll_radius}px;
                min-height: {min_height}px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: rgba(0, 0, 0, 0.3);
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

    def add_drawer(self, text):
        """Добавить новый ящик"""
        button = DrawerButton(text, self.temp_id)
        self.temp_id += 1
        self.layout.addWidget(button)
        return button

    def remove_drawer_by_id(self, id):
        """Удаляет ящик по его ID"""
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item and item.widget():
                button = item.widget()
                if hasattr(button, 'id') and button.id == id:
                    button.deleteLater()
                    return True
        return False
    
    def clear_drawers(self):
        """Очистить все ящики"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()