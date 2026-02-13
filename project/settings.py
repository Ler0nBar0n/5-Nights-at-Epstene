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
                background-color: rgba(47, 79, 79, 200);  /* Полупрозрачный фон */
            }
        """)
        
        # Контейнер с настройками (центрированный)
        self.settings_container = QWidget(self)
        self.settings_container.setFixedSize(450, 350)
        self.setup_settings_ui()
        
        # Поднимаем контейнер над затемнением
        self.settings_container.raise_()
    
    def setup_settings_ui(self):
        """Интерфейс настроек"""
        layout = QVBoxLayout(self.settings_container)
        layout.setContentsMargins(20, 20, 20, 20) # Отступы от краёв
        layout.setSpacing(15) # Расстояние между элементами
        
        # Заголовок
        title = QLabel("Настройки")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #DEB887;
                font-size: 20px;
                font-weight: bold;
                padding: 10px; 
                background-color: #8B4513;
                border-radius: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Контент настроек (в него упаковывать сами функции)
        content = QWidget()
        content.setStyleSheet("""
            QWidget {
                background-color: #FDF5E6;
                border-radius: 10px; /*скругленные углы*/
            }
        """)
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        
        content_layout.addStretch()
        layout.addWidget(content)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        save_btn = QPushButton("Сохранить")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #DEB887;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
                color: #FFE4C4;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #DEB887;
                color: #2F4F4F;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFE4C4;
            }
        """)
        cancel_btn.clicked.connect(self.close)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        # Стиль контейнера
        self.settings_container.setStyleSheet("""
            QWidget {
                background-color: #2F4F4F;
                border: 3px solid #8B4513;
                border-radius: 15px;
            }
        """)
    
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
        """Сохранение настроек"""
        if self.parent() and hasattr(self.parent(), 'update_drawers'):
            self.parent().update_drawers(self.drawers_spinbox.value())
        self.close()
    
    def keyPressEvent(self, event):
        """Закрытие по Escape"""
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)
    