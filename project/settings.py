import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
     
class SettingsOverlay(QWidget):
    """Оверлей настроек - ВНУТРИ главного окна, поверх контента"""
    
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
                background-color: rgba(0, 0, 0, 30); 
            }
        """)
        
        # Контейнер с настройками (центрированный)
        self.settings_container = QWidget(self)
        self.settings_container.setFixedSize(450, 350)
        # Стиль контейнера
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
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.settings_container.setGraphicsEffect(shadow)
        
        """Интерфейс настроек"""
        layout = QVBoxLayout(self.settings_container)
        layout.setContentsMargins(20, 20, 20, 20) # Отступы от краёв
        layout.setSpacing(15) # Расстояние между элементами
        
        # Заголовок
        title = QLabel("Настройки")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Контент настроек (в него упаковывать сами настройки)
        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(15)
        
        
        
        # Создаём выпадающий список (QComboBox)
        self.combo_res = QComboBox()
        resolutions = ["800x600", "1024x768", "1280x720", "1920x1080"]
        self.combo_res.addItems(resolutions)
        self.combo_res.setStyleSheet("""
            QComboBox {
                color: #333333;              /* цвет текста в поле */
                font-size: 12pt;              /* размер шрифта */
                font-weight: bold;             /* жирность (опционально) */
                background-color: rgba(255, 255, 255, 200);     /* фон поля */
                border: 1px solid #cccccc;     /* рамка */
                border-radius: 8px;            /* скругление */
                padding: 8px;                  /* внутренние отступы */
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
        content_layout.addWidget(self.combo_res)
        self.change_resolution()
        self.combo_res.currentIndexChanged.connect(self.change_resolution)
        
        content_layout.addStretch()
        layout.addWidget(content)
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        save_btn = QPushButton("Сохранить")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save_settings)
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet("""
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
        cancel_btn.clicked.connect(self.close)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
    def change_resolution(self):
        # Получаем выбранную строку
        selected = self.combo_res.currentText()
        # Разделяем по символу 'x' и преобразуем в целые числа
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
        self.raise_()
        self.settings_container.raise_()
        
    def save_settings(self):
        main_window = self.window()  # это MainWindow
        main_window.resize(self.res_width, self.res_height)
        self.close()
        