import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DrawerButton(QPushButton):
    def __init__(self, text, id, parent=None):
        super().__init__(text, parent)
        self.id = id
        self.setMinimumHeight(60)
        self.setMaximumHeight(80)
        self.setCursor(Qt.PointingHandCursor)

        # Основной стиль кнопки
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: none;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 500;
                color: #333;
                padding: 8px 16px;
                text-align: left;
                margin: 4px 0px;
            }
            QPushButton:hover {
                background-color: #f5f5f7;
            }
            QPushButton:pressed {
                background-color: #e5e5ea;
            }
        """)

        # Тень для кнопки
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

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
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(0, 0, 0, 0.3);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def add_drawer(self, text):
        """Добавить новый ящик"""
        self.temp_id
        button = DrawerButton(text, self.temp_id)
        self.temp_id+=1
        self.layout.addWidget(button)

    def remove_drawer_by_id(self, id): #протестируй
        """
        Удаляет ящик по его ID
        Args:
            id: ID ящика, который нужно удалить
        """
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item and item.widget():
                button = item.widget()
                # Предполагаем, что у кнопки есть атрибут id
                if hasattr(button, 'id') and button.id == id:
                    button.deleteLater()
                    return True  # Успешно удалили
        return False  # Ящик с таким ID не найден
    
    def clear_drawers(self):
        """Очистить все ящики"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
