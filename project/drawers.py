import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DrawerButton(QPushButton):
    """Кнопка в виде ящика в шкафу"""
    def __init__(self, text, id,  parent=None):
        super().__init__(parent)
        self.setText(text)
        self.id=id
        self.setMinimumHeight(60)
        self.setMaximumHeight(80)
        
        # Стиль для кнопок-ящиков
        self.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #DEB887;
                border: 2px solid #654321;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                text-align: left;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #A0522D;
                border-color: #8B4513;
                color: #FFE4C4;
            }
            QPushButton:pressed {
                background-color: #654321;
            }
        """)

class DrawerScrollArea(QScrollArea):
    """Область прокрутки для ящиков"""
    def __init__(self, temp_id, parent=None):
        super().__init__(parent)
        self.temp_id=temp_id
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #Отключает горизонтальную прокрутку. Ящики должны идти только сверху вниз
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded) #Включает вертикальную прокрутку только когда она нужна (когда ящиков больше, чем помещается на экране)
        
        # Контейнер для кнопок
        self.container = QWidget()
        self.container.setStyleSheet("background-color: #2F4F4F")
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop) #Выравнивает все кнопки по верхнему краю
        self.layout.setSpacing(2) #Расстояние между кнопками в пикселях
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.setWidget(self.container)
        
        # Стиль для области прокрутки
        self.setStyleSheet("""
            QScrollArea {
                background-color: #2F4F4F;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2F4F4F;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #DEB887;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #FFE4C4;
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
