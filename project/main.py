import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from settings import SettingsOverlay
from create_task import CreateTaskOverlay
from drawers import DrawerButton, DrawerScrollArea

temp_id=0

class BoardLabel(QLabel):
    """Лейбл в виде доски"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        
        # Стиль для доски
        self.setStyleSheet("""
            QLabel {
            background-color: rgba(255, 255, 255, 200);
            border: none;
            border-radius: 20px;
            color: #333;
            padding: 20px;
        }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
                
        self.base_font_size = 20  # базовый размер в пикселях
        self.ui_scale_factor = 1.0  # коэффициент масштабирования интерфейса

        self.setWindowTitle("Доска")
        self.setGeometry(100, 100, 1024, 768)
        
        # Устанавливаем общий стиль приложения
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #ffd1dc, stop: 1 #add8e6);
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
        # оверлей создания задачи
        self.create_task_overlay = CreateTaskOverlay(self.central_widget)
        self.create_task_overlay.hide()
        
        # Добавляем несколько ящиков для примера
        self.update_drawers(10)
    
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

        # Тень для глубины
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        self.right_panel.setGraphicsEffect(shadow)

        # Layout с отступами
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(12, 12, 12, 12)
        self.right_layout.setSpacing(8)

        # Заголовок "Пользователи"
        self.drawers_label = QLabel("Пользователи")
        self.drawers_label.setAlignment(Qt.AlignCenter)
        self.update_drawers_label_style()
        self.right_layout.addWidget(self.drawers_label)

        # Область прокрутки с ящиками
        self.drawer_scroll = DrawerScrollArea(temp_id)
        self.right_layout.addWidget(self.drawer_scroll)
        layout.addWidget(self.right_panel)
        
    def draw_left_panel(self, layout):
        # Тень
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)
        
        # Левая часть (доска)
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)
        
        # Верхняя панель с кнопками
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
        
        # Создаем кнопки
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.clicked.connect(self.open_settings)
        self.settings_btn.setToolTip("Настройки")
        
        self.plus_btn = QPushButton("➕")
        self.plus_btn.clicked.connect(self.open_create_task)
        self.plus_btn.setToolTip("Добавить задачу")
        
        self.menu_btn = QPushButton("☰")
        self.menu_btn.setToolTip("Изменить вид")
        
        # Устанавливаем стиль для кнопок
        self.update_top_buttons_style()
        
        self.top_layout.addWidget(self.settings_btn)
        self.top_layout.addWidget(self.plus_btn)
        self.top_layout.addWidget(self.menu_btn)
        
        self.left_layout.addWidget(self.top_panel)
        
        # Доска
        self.board = BoardLabel()
        self.left_layout.addWidget(self.board)
        
        layout.addWidget(self.left_panel, 1)
    
    def update_top_buttons_style(self):
        """Обновить стиль верхних кнопок с учетом масштаба"""
        size = int(50 * self.ui_scale_factor)
        font_size = int(24 * self.ui_scale_factor)
        
        self.settings_btn.setFixedSize(size, size)
        self.plus_btn.setFixedSize(size, size)
        self.menu_btn.setFixedSize(size, size)
        
        button_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {size//2}px;
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
    
    def update_drawers_label_style(self):
        """Обновить стиль заголовка пользователей"""
        font_size = int(18 * self.ui_scale_factor)
        padding = int(8 * self.ui_scale_factor)
        
        self.drawers_label.setStyleSheet(f"""
            QLabel {{
                color: #1e1e2f;
                font-size: {font_size}px;
                font-weight: 600;
                padding: {padding}px 0 {padding*1.5}px 0;
                background-color: transparent;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }}
        """)
    
    def update_right_panel_size(self):
        """Обновить размеры правой панели"""
        max_width = int(250 * self.ui_scale_factor)
        min_width = int(200 * self.ui_scale_factor)
        self.right_panel.setMaximumWidth(max_width)
        self.right_panel.setMinimumWidth(min_width)
        
        # Обновляем отступы
        margin = int(12 * self.ui_scale_factor)
        self.right_layout.setContentsMargins(margin, margin, margin, margin)
        self.right_layout.setSpacing(int(8 * self.ui_scale_factor))
    
    def update_left_panel_spacing(self):
        """Обновить отступы в левой панели"""
        self.left_layout.setSpacing(int(10 * self.ui_scale_factor))
        
        # Обновляем высоту верхней панели
        self.top_panel.setMaximumHeight(int(70 * self.ui_scale_factor))
        
        # Обновляем радиус скругления
        radius = int(15 * self.ui_scale_factor)
        self.top_panel.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 180);
                border-radius: {radius}px;
            }}
        """)
    
    def apply_ui_scale(self):
        """Применить масштабирование интерфейса"""
        # Обновляем правую панель
        self.update_right_panel_size()
        
        # Обновляем заголовок
        self.update_drawers_label_style()
        
        # Обновляем верхние кнопки
        self.update_top_buttons_style()
        
        # Обновляем отступы в левой панели
        self.update_left_panel_spacing()
        
        # Обновляем шрифты в кнопках ящиков через DrawerButton
        DrawerButton.update_scale_factor(self.ui_scale_factor)
        
        # Перерисовываем все кнопки в drawer_scroll
        if hasattr(self, 'drawer_scroll'): #проверка что этот атрибут есть
            for i in range(self.drawer_scroll.layout.count()):
                item = self.drawer_scroll.layout.itemAt(i)
                if item and item.widget():
                    button = item.widget()
                    button.update_style()
    
    def open_settings(self):
        """Открыть окно настроек внутри главного окна"""
        self.settings_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.settings_overlay.show()
        self.settings_overlay.raise_()
    
    def open_create_task(self):
        """Открыть окно создания задачи"""
        self.create_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.create_task_overlay.show()
        self.create_task_overlay.raise_()
        
    def resizeEvent(self, event):
        """Обновляем размер оверлея при изменении размера окна"""
        super().resizeEvent(event)
        if hasattr(self, 'settings_overlay') and self.settings_overlay.isVisible():
            self.settings_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        if hasattr(self, 'create_task_overlay') and self.create_task_overlay.isVisible():
            self.create_task_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
    
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