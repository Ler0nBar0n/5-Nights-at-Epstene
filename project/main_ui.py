from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from drawers import DrawerScrollArea
from board import Board
from task import TaskFactory

temp_id = 0

class MainUI(QWidget):
    settingsClicked = pyqtSignal()
    createTaskClicked = pyqtSignal()

    def __init__(self, scale_manager):
        super().__init__()
        
        self.scale_manager = scale_manager
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.draw_left_panel(self.main_layout)
        self.draw_right_panel(self.main_layout)
        
        self.update_drawers(10)
        
        # Начальное применение стилей
        self.update_ui_scale()
        
    def draw_right_panel(self, layout):
        self.right_panel = QWidget()
        self.right_panel.setMaximumWidth(250)
        self.right_panel.setMinimumWidth(200)
        self.right_panel.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 20px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        self.right_panel.setGraphicsEffect(shadow)

        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(12, 12, 12, 12)
        self.right_layout.setSpacing(8)

        self.drawers_label = QLabel("Пользователи")
        self.drawers_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.drawers_label)

        self.drawer_scroll = DrawerScrollArea(temp_id, self.scale_manager)
        self.right_layout.addWidget(self.drawer_scroll)
        layout.addWidget(self.right_panel)

    def draw_left_panel(self, layout):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)

        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)

        self.top_panel = QWidget()
        self.top_panel.setMaximumHeight(70)
        self.top_panel.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 15px;")
        self.top_panel.setGraphicsEffect(shadow)
        self.top_layout = QHBoxLayout(self.top_panel)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setAlignment(Qt.AlignLeft)

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setToolTip("Настройки")
        self.settings_btn.clicked.connect(self.settingsClicked.emit)

        self.plus_btn = QPushButton("➕")
        self.plus_btn.setToolTip("Добавить задачу")
        self.plus_btn.clicked.connect(self.createTaskClicked.emit)

        self.menu_btn = QPushButton("☰")
        self.menu_btn.setToolTip("Изменить вид")

        self.top_layout.addWidget(self.settings_btn)
        self.top_layout.addWidget(self.plus_btn)
        self.top_layout.addWidget(self.menu_btn)

        self.left_layout.addWidget(self.top_panel)

        self.board = Board(self.scale_manager)
        self.left_layout.addWidget(self.board)

        layout.addWidget(self.left_panel, 1)
    
    def update_drawers(self, count):
        self.drawer_scroll.clear_drawers()
        drawer_names = [
            "Глава", "Тимлид", "Вождь", "Офицер", "Чиновник",
            "Пролетарий", "Крестьянин", "Холоп", "Раб", "Программист"
        ]
        for i in range(min(count, len(drawer_names))):
            self.drawer_scroll.add_drawer(drawer_names[i])
    
    def add_task(self, title, description):
        """Создать задачу и добавить на доску"""
        task = TaskFactory.create_task(self.board.tasks_container, title, description, self.scale_manager)
        task.move(50, 50)
        self.board.add_task(task)
        return task

    def update_ui_scale(self):
        """Обновить элементы интерфейса при изменении масштаба"""
        # Кнопки верхней панели
        size = self.scale_manager.scale_value(50)
        font_size = self.scale_manager.scale_value(24)
        for btn in (self.settings_btn, self.plus_btn, self.menu_btn):
            btn.setFixedSize(size, size)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: {size // 2}px;
                    font-size: {font_size}px;
                    color: #333;
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 0, 0, 0.05);
                }}
                QPushButton:pressed {{
                    background-color: rgba(0, 0, 0, 0.1);
                }}
            """)

        # Заголовок правой панели
        font_size_label = self.scale_manager.scale_value(18)
        padding = self.scale_manager.scale_value(8)
        self.drawers_label.setStyleSheet(f"""
            QLabel {{
                color: #1e1e2f;
                font-size: {font_size_label}px;
                font-weight: 600;
                padding: {padding}px 0 {padding * 1.5}px 0;
                background-color: transparent;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }}
        """)

        # Размеры правой панели
        max_width = self.scale_manager.scale_value(250)
        min_width = self.scale_manager.scale_value(200)
        self.right_panel.setMaximumWidth(max_width)
        self.right_panel.setMinimumWidth(min_width)
        margin = self.scale_manager.scale_value(12)
        self.right_layout.setContentsMargins(margin, margin, margin, margin)
        self.right_layout.setSpacing(self.scale_manager.scale_value(8))

        # Левая панель
        self.left_layout.setSpacing(self.scale_manager.scale_value(10))
        self.top_panel.setMaximumHeight(self.scale_manager.scale_value(70))
        radius = self.scale_manager.scale_value(15)
        self.top_panel.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 180);
                border-radius: {radius}px;
            }}
        """)
        
