import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from settings import SettingsOverlay
from drawers import DrawerButton, DrawerScrollArea

backgroundColour="#2F4F4F"
temp_id=0

class BoardLabel(QLabel):
    """Лейбл в виде доски"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        
        # Стиль для доски
        self.setStyleSheet("""
            QLabel {
                background-color: #FDF5E6;
                border: 12px solid #8B4513;
                border-radius: 10px;
                font-size: 48px;
                font-weight: bold;
                color: #2F4F4F;
                padding: 20px;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Доска")
        self.setGeometry(100, 100, 1000, 600)
        
        # Устанавливаем общий стиль приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2F4F4F;
            }
        """)
        
        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Основной горизонтальный layout
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        self.draw_left_panel(main_layout)
        self.draw_right_panel(main_layout)
        
        # Создаем оверлей для настроек (изначально скрыт)
        self.settings_overlay = SettingsOverlay(self.central_widget)
        self.settings_overlay.hide()
        
        # Добавляем несколько ящиков для примера
        self.update_drawers(10)  # Можно легко изменить количество ящиков
    
    def draw_right_panel(self, layout):
        right_panel = QWidget()
        right_panel.setMaximumWidth(250)
        right_panel.setMinimumWidth(200)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок для панели ящиков
        drawers_label = QLabel("Пользователи")
        drawers_label.setAlignment(Qt.AlignCenter)
        drawers_label.setStyleSheet("""
            QLabel {
                color: #DEB887;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #8B4513;
                border-radius: 5px;
                margin-bottom: 5px;
            }
        """)
        right_layout.addWidget(drawers_label)
        
        # Область прокрутки с ящиками
        self.drawer_scroll = DrawerScrollArea(temp_id)
        right_layout.addWidget(self.drawer_scroll)
        layout.addWidget(right_panel)
        
    def draw_left_panel(self, layout):
        
        # Левая часть (доска)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Верхняя панель с кнопками
        top_panel = QWidget()
        top_panel.setMaximumHeight(70)  # Максимальная высота 70 пикселей
        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setAlignment(Qt.AlignLeft)
        
        # Создаем кнопки
        settings_btn = QPushButton("⚙️")
        settings_btn.clicked.connect(self.open_settings)
        settings_btn.setToolTip("Настройки") #Подсказка при наведении
        settings_btn.setFixedSize(50, 50)
        
        plus_btn = QPushButton("➕")
        plus_btn.setToolTip("Добавить")
        plus_btn.setFixedSize(50, 50)
        
        menu_btn = QPushButton("☰")
        menu_btn.setToolTip("Меню")
        menu_btn.setFixedSize(50, 50)
        
        # Стиль для верхних кнопок
        button_style = """
            QPushButton {
                background-color: #DEB887;
                border: 2px solid #8B4513;
                border-radius: 25px;
                font-size: 24px;
                color: #2F4F4F;
            }
            QPushButton:hover {
                background-color: #FFE4C4;
                border-color: #654321;
            }
            QPushButton:pressed {
                background-color: #8B4513;
                color: #DEB887;
            }
        """
        
        settings_btn.setStyleSheet(button_style)
        plus_btn.setStyleSheet(button_style)
        menu_btn.setStyleSheet(button_style)
        
        top_layout.addWidget(settings_btn)
        top_layout.addWidget(plus_btn)
        top_layout.addWidget(menu_btn)
        
        left_layout.addWidget(top_panel)
        
        
        # Доска
        self.board = BoardLabel()
        left_layout.addWidget(self.board)
        
        layout.addWidget(left_panel, 1)  # stretch=1, чтобы занимал всё доступное пространство
    
    def open_settings(self):
        """Открыть окно настроек внутри главного окна"""
        # Обновляем размер оверлея под размер центрального виджета
        self.settings_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.settings_overlay.show()
        self.settings_overlay.raise_()
    
    def resizeEvent(self, event):
        """Обновляем размер оверлея при изменении размера окна"""
        super().resizeEvent(event)
        if hasattr(self, 'settings_overlay') and self.settings_overlay.isVisible():
            self.settings_overlay.setGeometry(0, 0,  self.central_widget.width(), self.central_widget.height())
    
    def update_drawers(self, count):
        """Обновить количество ящиков"""
        self.drawer_scroll.clear_drawers()
        
        
        # Названия ящиков для примера
        drawer_names = [
            "Глава",
            "Тимлид",
            "Вождь",
            "Офицер",
            "Чиновник",
            "Пролетарий",
            "Крестьянин",
            "Холоп",
            "Раб",
            "Программист"
        ]
        
        for i in range(min(count, len(drawer_names))):
            self.drawer_scroll.add_drawer(drawer_names[i])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Устанавливаем современный стиль
    app.setStyle('Fusion')
    
    # Создаём и показываем окно
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())