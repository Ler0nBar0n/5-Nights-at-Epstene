import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from settings import SettingsOverlay
from create_task import CreateTaskOverlay
from task import ViewTaskOverlay
from managers import ScaleManager
from main_ui import MainUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scale_manager = ScaleManager()

        self.setWindowTitle("Доска")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #ffd1dc, stop: 1 #add8e6);
            }
        """)

        self.central_widget = MainUI(self.scale_manager)
        self.setCentralWidget(self.central_widget)

        # Подключение сигнала изменения масштаба
        self.scale_manager.scaleFactorChanged.connect(self.central_widget.update_ui_scale)
        # Подключение сигналов от MainUI для кнопок
        self.central_widget.settingsClicked.connect(self.open_settings)
        self.central_widget.createTaskClicked.connect(self.open_create_task)
        
        self.central_widget.viewTaskRequested.connect(self.open_view_task)

        # Создание оверлеев
        self.settings_overlay = SettingsOverlay(self.scale_manager, self.central_widget)
        self.settings_overlay.hide()
        self.create_task_overlay = CreateTaskOverlay(self.scale_manager, self.central_widget)
        self.create_task_overlay.hide()
        self.view_task_overlay = ViewTaskOverlay(self.scale_manager, self.central_widget)
        self.view_task_overlay.hide()
        
        self.create_task_overlay.taskCreated.connect(self.create_task)

        self.tasks = []  # для хранения созданных задач

    def open_settings(self):
        self.settings_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.settings_overlay.show()
        self.settings_overlay.raise_()

    def open_create_task(self):
        self.create_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.create_task_overlay.show()
        self.create_task_overlay.raise_()

    def create_task(self, title, description):
        """Вызывается из CreateTaskOverlay"""
        task = self.central_widget.add_task(title, description)
        self.tasks.append(task)

    def open_view_task(self, title, description):
        """Вызывается из TaskWidget"""
        self.view_task_overlay.set_task_data(title, description)
        self.view_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.view_task_overlay.show()
        self.view_task_overlay.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Обновляем размеры видимых оверлеев
        w, h = self.central_widget.width(), self.central_widget.height()
        if self.settings_overlay.isVisible():
            self.settings_overlay.setGeometry(0, 0, w, h)
        if self.create_task_overlay.isVisible():
            self.create_task_overlay.setGeometry(0, 0, w, h)
        if self.view_task_overlay.isVisible():
            self.view_task_overlay.setGeometry(0, 0, w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())