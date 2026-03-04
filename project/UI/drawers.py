import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DrawerButton(QPushButton):
    def __init__(self, text, id, scale_manager, parent=None):
        super().__init__(text, parent)
        self.id = id
        self.scale_manager = scale_manager
        self.scale_manager.scaleFactorChanged.connect(self.update_style)
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()
    
    def update_shadow(self):
        """Обновить тень с учетом масштаба"""
        shadow = QGraphicsDropShadowEffect()
        blur = self.scale_manager.scale_value(12)
        offset = self.scale_manager.scale_value(2)
        shadow.setBlurRadius(blur)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, offset)
        self.setGraphicsEffect(shadow)
    
    def update_style(self):
        """Обновить стиль кнопки с учетом масштаба"""
        sf = self.scale_manager.factor
        font_size = self.scale_manager.scale_value(15)
        padding_x = self.scale_manager.scale_value(16)
        padding_y = self.scale_manager.scale_value(8)
        margin = self.scale_manager.scale_value(4)
        radius = self.scale_manager.scale_value(12)
        
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
        self.setMinimumHeight(self.scale_manager.scale_value(60))
        self.setMaximumHeight(self.scale_manager.scale_value(80))
        
        # Обновляем тень
        self.update_shadow()

class DrawerScrollArea(QScrollArea):
    """Область прокрутки для ящиков"""
    def __init__(self, temp_id, scale_manager, parent=None):
        super().__init__(parent)
        self.temp_id = temp_id
        self.scale_manager = scale_manager
        self.scale_manager.scaleFactorChanged.connect(self.update_scroll_style)
        
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
        scale = self.scale_manager.factor
        scroll_width = self.scale_manager.scale_value(6)
        scroll_radius = self.scale_manager.scale_value(3)
        min_height = self.scale_manager.scale_value(30)
        
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
        button = DrawerButton(text, self.temp_id, self.scale_manager)
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