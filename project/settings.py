import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
     
class SettingsOverlay(QWidget):
    """Оверлей настроек"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        # Затемняющий слой (полупрозрачный фон)
        self.dark_overlay = QWidget(self)
        self.dark_overlay.setGeometry(0, 0, self.width(), self.height())
        self.dark_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 30); 
            }
        """)
        
        # Контейнер с настройками (центрированный)
        self.settings_container = QWidget(self)
        self.settings_container.setFixedSize(450, 350)
        self.settings_container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 20px;
            }
        """)
        self.setup_settings_ui()
        
        # Поднимаем контейнер над затемнением
        self.settings_container.raise_()
    
    def setup_settings_ui(self):
        
        # Тень для контейнера
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 10)
        self.settings_container.setGraphicsEffect(self.shadow)
        
        """Интерфейс настроек"""
        self.layout = QVBoxLayout(self.settings_container)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Заголовок
        self.title = QLabel("Настройки")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.title)
        
        # Контент настроек
        self.content = QWidget()
        self.content.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(15)
        
        # Создаём выпадающий список для разрешения
        self.combo_res = QComboBox()
        resolutions = ["800x600", "1024x768", "1280x720", "1920x1080"]
        self.combo_res.addItems(resolutions)
        self.combo_res.setCurrentIndex(1) #значение по умолчанию
        self.combo_res.setStyleSheet("""
            QComboBox {
                color: #333333;
                font-size: 12pt;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 8px;
            }
            QComboBox::item {
                color: #333333;
                background-color: white;
            }
            QComboBox::item:selected {
                background-color: #007AFF;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.content_layout.addWidget(self.combo_res)
        self.combo_res.currentIndexChanged.connect(self.change_resolution)
        
        # Масштаб интерфейса
        self.combo_size = QComboBox()
        size_options = ["Крошечный", "Маленький", "Средний", "Большой"]
        self.combo_size.addItems(size_options)
        self.combo_size.setCurrentIndex(1)  # Маленький по умолчанию
        self.combo_size.setStyleSheet("""
            QComboBox {
                color: #333333;
                font-size: 12pt;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 8px;
            }
            QComboBox::item {
                color: #333333;
                background-color: white;
            }
            QComboBox::item:selected {
                background-color: #007AFF;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        
        self.content_layout.addWidget(self.combo_size)
        self.combo_size.currentIndexChanged.connect(self.change_size)
        
        self.content_layout.addStretch()
        self.layout.addWidget(self.content)
        
        # Кнопки
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(10)
        
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005BBF;
            }
            QPushButton:pressed {
                background-color: #004999;
            }
        """)
        self.save_btn.clicked.connect(self.save_settings)
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,200);
                color: #333;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,255);
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        self.cancel_btn.clicked.connect(self.close)
        
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.save_btn)
        self.buttons_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(self.buttons_layout)
        
        # Устанавливаем начальные значения
        self.change_resolution()
        self.change_size()
        
    def change_size(self):
        """Обработка изменения размера интерфейса"""
        selected = self.combo_size.currentText()
        # Преобразуем выбор в коэффициент масштабирования
        if selected == "Крошечный":
            self.ui_scale = 0.8
            self.font_size = 16
        elif selected == "Маленький":
            self.ui_scale = 1
            self.font_size = 20
        elif selected == "Средний":
            self.ui_scale = 1.2
            self.font_size = 24
        else:  # "Большой"
            self.ui_scale = 1.5
            self.font_size = 30
    
    def change_resolution(self):
        """Обработка изменения разрешения"""
        selected = self.combo_res.currentText()
        self.res_width, self.res_height = map(int, selected.split('x'))
        
    def resizeEvent(self, event):
        """При изменении размера обновляем геометрию"""
        super().resizeEvent(event)
        # Обновляем размер затемнения
        self.dark_overlay.setGeometry(0, 0, self.width(), self.height())
        # Центрируем контейнер
        self.settings_container.move(
            (self.width() - self.settings_container.width()) // 2,
            (self.height() - self.settings_container.height()) // 2
        )
    
    def showEvent(self, event):
        """При показе поднимаем наверх"""
        super().showEvent(event)
        self.apply_scale()
        self.raise_()
        self.settings_container.raise_()
        
    def apply_scale(self):
        """Применить текущий масштаб ко всем элементам оверлея"""
        sf = self.ui_scale

        # Размер контейнера
        container_width = int(450 * sf)
        container_height = int(350 * sf)
        self.settings_container.setFixedSize(container_width, container_height)

        # Радиус скругления контейнера
        radius = int(20 * sf)
        self.settings_container.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 220);
                border-radius: {radius}px;
            }}
        """)

        # Тень
        self.shadow.setBlurRadius(int(30 * sf))
        self.shadow.setOffset(0, int(10 * sf))

        # Отступы в layout
        margin = int(20 * sf)
        spacing = int(15 * sf)
        layout = self.settings_container.layout()
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)

        # Заголовок
        title_font_size = int(20 * sf)
        title_padding = int(10 * sf)
        self.title.setStyleSheet(f"""
            QLabel {{
                color: #333;
                font-size: {title_font_size}px;
                font-weight: bold;
                padding: {title_padding}px;
            }}
        """)


        # Комбобоксы (общий стиль)
        combo_font_size = int(16 * sf)  # базовый 16px
        combo_padding = int(8 * sf)
        combo_radius = int(8 * sf)
        combo_style = f"""
            QComboBox {{
                color: #333333;
                font-size: {combo_font_size}px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid #cccccc;
                border-radius: {combo_radius}px;
                padding: {combo_padding}px;
            }}
            QComboBox::item {{
                color: #333333;
                background-color: white;
            }}
            QComboBox::item:selected {{
                background-color: #007AFF;
                color: white;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """
        self.combo_res.setStyleSheet(combo_style)
        self.combo_size.setStyleSheet(combo_style)

        # Кнопки
        btn_font_size = int(14 * sf)
        btn_padding_y = int(10 * sf)
        btn_padding_x = int(20 * sf)
        btn_radius = int(8 * sf)

        # Кнопка "Сохранить"
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: {btn_radius}px;
                padding: {btn_padding_y}px {btn_padding_x}px;
                font-size: {btn_font_size}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #005BBF;
            }}
            QPushButton:pressed {{
                background-color: #004999;
            }}
        """)

        # Кнопка "Отмена"
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255,255,255,200);
                color: #333;
                border: 1px solid #ccc;
                border-radius: {btn_radius}px;
                padding: {btn_padding_y}px {btn_padding_x}px;
                font-size: {btn_font_size}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,255);
            }}
            QPushButton:pressed {{
                background-color: #e0e0e0;
            }}
        """)
        self.resizeEvent(None)

    def save_settings(self):
        """Сохранение настроек"""
        main_window = self.window()  # это MainWindow
        
        # Изменяем размер окна
        main_window.resize(self.res_width, self.res_height)
        
        # Изменяем размер интерфейса
        main_window.base_font_size = self.font_size
        main_window.ui_scale_factor = self.ui_scale
        main_window.apply_ui_scale()
        
        
        self.close()