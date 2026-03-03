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
    def __init__(self, parent=None):
        super().__init__(parent)
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

    def update_tasks_style(self):
        """Обновить стиль всех задач (при изменении масштаба)"""
        for task in self.tasks:
            task.update_style()

    def update_label_style(self, sf):
        """Обновить стиль фонового лейбла с учётом масштаба"""
        font_size = int(18 * sf)
        padding = int(20 * sf)
        radius = int(20 * sf)
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
