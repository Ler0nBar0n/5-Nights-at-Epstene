import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from settings import SettingsOverlay
from create_task import CreateTaskOverlay
from drawers import DrawerButton, DrawerScrollArea
from task import TaskWidget, TaskFactory, ViewTaskOverlay
from board import Board
from managers import ScaleManager

temp_id = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scale_manager = ScaleManager()
        self.scale_manager.scaleFactorChanged.connect(self._update_ui_scale)

        self.setWindowTitle("Доска")
        self.setGeometry(100, 100, 1024, 768)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #ffd1dc, stop: 1 #add8e6);
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.draw_left_panel(main_layout)
        self.draw_right_panel(main_layout)

        # Создаем оверлеи с передачей scale_manager
        self.settings_overlay = SettingsOverlay(self.scale_manager, self.central_widget)
        self.settings_overlay.hide()
        self.create_task_overlay = CreateTaskOverlay(self.scale_manager, self.central_widget)
        self.create_task_overlay.hide()
        self.view_task_overlay = ViewTaskOverlay(self.scale_manager, self.central_widget)
        self.view_task_overlay.hide()

        self.tasks = []
        self.update_drawers(10)
        
        # Начальное применение стилей для элементов главного окна
        self._update_ui_scale()

    def draw_right_panel(self, layout):
        self.right_panel = QWidget()
        self.right_panel.setMaximumWidth(250)
        self.right_panel.setMinimumWidth(200)

        self.right_panel.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 20px;
            }
        """)

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
        self.top_panel.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        self.top_panel.setGraphicsEffect(shadow)
        self.top_layout = QHBoxLayout(self.top_panel)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setAlignment(Qt.AlignLeft)

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.clicked.connect(self.open_settings)
        self.settings_btn.setToolTip("Настройки")

        self.plus_btn = QPushButton("➕")
        self.plus_btn.clicked.connect(self.open_create_task)
        self.plus_btn.setToolTip("Добавить задачу")

        self.menu_btn = QPushButton("☰")
        self.menu_btn.setToolTip("Изменить вид")

        self.top_layout.addWidget(self.settings_btn)
        self.top_layout.addWidget(self.plus_btn)
        self.top_layout.addWidget(self.menu_btn)

        self.left_layout.addWidget(self.top_panel)

        self.board = Board(self.scale_manager)
        self.left_layout.addWidget(self.board)

        layout.addWidget(self.left_panel, 1)

    def _update_ui_scale(self):
        """Обновить элементы интерфейса главного окна при изменении масштаба"""
        # Обновляем кнопки верхней панели
        size = self.scale_manager.scale_value(50)
        font_size = self.scale_manager.scale_value(24)
        self.settings_btn.setFixedSize(size, size)
        self.plus_btn.setFixedSize(size, size)
        self.menu_btn.setFixedSize(size, size)
        button_style = f"""
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
        """
        self.settings_btn.setStyleSheet(button_style)
        self.plus_btn.setStyleSheet(button_style)
        self.menu_btn.setStyleSheet(button_style)

        # Обновляем заголовок правой панели
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

        # Обновляем размеры правой панели
        max_width = self.scale_manager.scale_value(250)
        min_width = self.scale_manager.scale_value(200)
        self.right_panel.setMaximumWidth(max_width)
        self.right_panel.setMinimumWidth(min_width)
        margin = self.scale_manager.scale_value(12)
        self.right_layout.setContentsMargins(margin, margin, margin, margin)
        self.right_layout.setSpacing(self.scale_manager.scale_value(8))

        # Обновляем отступы в левой панели
        self.left_layout.setSpacing(self.scale_manager.scale_value(10))
        self.top_panel.setMaximumHeight(self.scale_manager.scale_value(70))
        radius = self.scale_manager.scale_value(15)
        self.top_panel.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 180);
                border-radius: {radius}px;
            }}
        """)

    def open_settings(self):
        self.settings_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.settings_overlay.show()
        self.settings_overlay.raise_()

    def open_create_task(self):
        self.create_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.create_task_overlay.show()
        self.create_task_overlay.raise_()

    def create_task(self, title, description):
        task = TaskFactory.create_task(self.board.tasks_container, title, description, self.scale_manager)
        task.move(50, 50)
        self.board.add_task(task)
        self.tasks.append(task)

    def open_view_task(self, title, description):
        self.view_task_overlay.set_task_data(title, description)
        self.view_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.view_task_overlay.show()
        self.view_task_overlay.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'settings_overlay') and self.settings_overlay.isVisible():
            self.settings_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        if hasattr(self, 'create_task_overlay') and self.create_task_overlay.isVisible():
            self.create_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        if hasattr(self, 'view_task_overlay') and self.view_task_overlay.isVisible():
            self.view_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())

    def update_drawers(self, count):
        self.drawer_scroll.clear_drawers()
        drawer_names = [
            "Глава", "Тимлид", "Вождь", "Офицер", "Чиновник",
            "Пролетарий", "Крестьянин", "Холоп", "Раб", "Программист"
        ]
        for i in range(min(count, len(drawer_names))):
            self.drawer_scroll.add_drawer(drawer_names[i])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())