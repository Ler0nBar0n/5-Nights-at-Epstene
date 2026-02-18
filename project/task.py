import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
     
class NewTaskOverlay(QWidget):
    """Оверлей создания листочка"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget) #делаем виджет безрамным и дочерним (а не отдельным окном)
        self.setAttribute(Qt.WA_StyledBackground, True) # Разрешает применять стили CSS к фону
        self.setAttribute(Qt.WA_TranslucentBackground, False) #делаем не прозрачным (чтобы потом сделать полупрозрачным)
        
        # Основной layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Затемняющий слой (полупрозрачный фон)
        self.dark_overlay = QWidget(self)
        self.dark_overlay.setGeometry(0, 0, self.width(), self.height())
        self.dark_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(47, 79, 79, 200);  /* Полупрозрачный фон */
            }
        """)
        
        # Контейнер с настройками (центрированный)
        self.task_container = QWidget(self)
        self.task_container.setFixedSize(450, 350)
        self.setup_task_ui()
        
        # Поднимаем контейнер над затемнением
        self.task_container.raise_()
    def setup_task_ui():