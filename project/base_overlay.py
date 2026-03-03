import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class BaseOverlay(QWidget):
    """Родительский класс для остальных оверлеев"""
    def __init__(self, scale_manager, parent=None):
        super().__init__(parent)
        self.scale_manager = scale_manager
        self.scale_manager.scaleFactorChanged.connect(self.update_style)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.base_width = 450
        self.base_height = 350
        
        # Затемняющий слой (полупрозрачный фон)
        self.dark_overlay = QWidget(self)
        self.dark_overlay.setGeometry(0, 0, self.width(), self.height())
        self.dark_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 30); 
            }
        """)
        
        # Контейнер для содержимого (центрированный)
        self.content_container = QWidget(self)
        self.content_container.setFixedSize(self.base_width, self.base_height)
        self.content_container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 20px;
            }
        """)
        self.setup_ui()
        
        # Поднимаем контейнер над затемнением
        self.content_container.raise_()
        
        # Начальное применение стиля
        self.update_style()
        
    def setup_ui(self):
        # Тень для контейнера
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 10)
        self.content_container.setGraphicsEffect(self.shadow)
        
        """Интерфейс"""
        self.layout = QVBoxLayout(self.content_container)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Заголовок
        self.title = QLabel("Заголовок")
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
        
        # Контент 
        self.content = QWidget()
        self.content.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(15)
        
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
        self.save_btn.clicked.connect(self.save_changes)
        
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
    
    def resizeEvent(self, event):
        """При изменении размера обновляем геометрию"""
        super().resizeEvent(event)
        # Обновляем размер затемнения
        self.dark_overlay.setGeometry(0, 0, self.width(), self.height())
        # Центрируем контейнер
        self.content_container.move(
            (self.width() - self.content_container.width()) // 2,
            (self.height() - self.content_container.height()) // 2
        )
        
    def showEvent(self, event):
        """При показе поднимаем наверх"""
        super().showEvent(event)
        self.raise_()
        self.content_container.raise_()
        
    def update_style(self):
        """Применить текущий масштаб ко всем элементам оверлея"""
        sf = self.scale_manager.factor

        # Размер контейнера
        container_width = self.scale_manager.scale_value(self.base_width)
        container_height = self.scale_manager.scale_value(self.base_height)
        self.content_container.setFixedSize(container_width, container_height)

        # Радиус скругления контейнера
        radius = self.scale_manager.scale_value(20)
        self.content_container.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 220);
                border-radius: {radius}px;
            }}
        """)

        # Тень
        self.shadow.setBlurRadius(self.scale_manager.scale_value(30))
        self.shadow.setOffset(0, self.scale_manager.scale_value(10))

        # Отступы в layout
        margin = self.scale_manager.scale_value(20)
        spacing = self.scale_manager.scale_value(15)
        layout = self.content_container.layout()
        if layout:
            layout.setContentsMargins(margin, margin, margin, margin)
            layout.setSpacing(spacing)

        # Заголовок
        title_font_size = self.scale_manager.scale_value(20)
        title_padding = self.scale_manager.scale_value(10)
        self.title.setStyleSheet(f"""
            QLabel {{
                color: #333;
                font-size: {title_font_size}px;
                font-weight: bold;
                padding: {title_padding}px;
            }}
        """)

        # Кнопки
        btn_font_size = self.scale_manager.scale_value(14)
        btn_padding_y = self.scale_manager.scale_value(10)
        btn_padding_x = self.scale_manager.scale_value(20)
        btn_radius = self.scale_manager.scale_value(8)

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

        self.resizeEvent(None)  # обновить центровку
    
    # def save_changes(self):  # будет переопределён в наследниках