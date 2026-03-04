import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class BoardLabel(QLabel):
    """Лейбл в виде доски (фон)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 150);
                border: none;
                border-radius: 20px;
                color: #333;
                padding: 20px;
            }
        """)

class Board(QWidget):
    """Доска с фоновым лейблом и контейнером задач поверх"""
    def __init__(self, scale_manager, parent=None):
        super().__init__(parent)
        self.scale_manager = scale_manager
        self.scale_manager.scaleFactorChanged.connect(self.update_label_style)
        
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        self.tasks = []
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Фоновый лейбл (занимает всю область)
        self.board_label = BoardLabel(self)
        self.board_label.lower()  # на задний план

        # Контейнер для задач (прозрачный, поверх лейбла)
        self.tasks_container = QWidget(self)
        self.tasks_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tasks_container.setStyleSheet("background-color: transparent;")

        # Устанавливаем геометрию для обоих виджетов
        self.update_geometry()
        
        # Начальное применение стиля
        self.update_label_style()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_geometry()

    def update_geometry(self):
        """Обновить размеры фонового лейбла и контейнера задач"""
        rect = self.rect()
        self.board_label.setGeometry(rect)
        self.tasks_container.setGeometry(rect)

    def add_task(self, task):
        """Добавить задачу в контейнер задач"""
        task.setParent(self.tasks_container)
        self.tasks.append(task)
        task.show()
        task.raise_()  # поднимаем над другими задачами (но они и так в контейнере)

    def update_label_style(self):
        """Обновить стиль фонового лейбла с учётом масштаба"""
        sf = self.scale_manager.factor
        font_size = self.scale_manager.scale_value(18)
        padding = self.scale_manager.scale_value(20)
        radius = self.scale_manager.scale_value(20)
        self.board_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(255, 255, 255, 150);
                border: none;
                border-radius: {radius}px;
                color: #333;
                padding: {padding}px;
                font-size: {font_size}px;
            }}
        """)