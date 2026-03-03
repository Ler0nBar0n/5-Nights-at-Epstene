import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from base_overlay import BaseOverlay

class SettingsOverlay(BaseOverlay):
    """Оверлей настроек"""
    
    def __init__(self, scale_manager, parent=None):
        super().__init__(scale_manager, parent)
        self.title.setText("Настройки")
        self.new_scale = 1.0  # будет установлено при показе
        
    def setup_ui(self):
        # Базовый интерфейс
        super().setup_ui()
        
        # Добавляем виджеты в content_layout
        self.combo_res = QComboBox()
        resolutions = ["800x600", "1024x768", "1280x720", "1920x1080"]
        self.combo_res.addItems(resolutions)
        self.combo_res.setCurrentIndex(1)  # 1024x768 по умолчанию
        self.combo_res.currentIndexChanged.connect(self.change_resolution)
        self.content_layout.addWidget(self.combo_res)
        
        self.combo_size = QComboBox()
        size_options = ["Крошечный", "Маленький", "Средний", "Большой"]
        self.combo_size.addItems(size_options)
        self.combo_size.setCurrentIndex(1)  # Маленький по умолчанию
        self.combo_size.currentIndexChanged.connect(self.change_size)
        self.content_layout.addWidget(self.combo_size)
        
        self.content_layout.addStretch()
        
        # Инициализация переменных из текущего выбора
        self.change_resolution()
        self.change_size()
        
    def update_style(self):
        """Применить масштаб из менеджера ко всем элементам оверлея"""
        super().update_style()
        
        sf = self.scale_manager.factor
        
        # Масштабируем комбобоксы
        combo_font_size = self.scale_manager.scale_value(16)
        combo_padding = self.scale_manager.scale_value(8)
        combo_radius = self.scale_manager.scale_value(8)
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
        
    def showEvent(self, event):
        super().showEvent(event)
        # Синхронизируем комбобокс размера с текущим масштабом
        current_scale = self.scale_manager.factor
        
        # Определяем индекс по значению scale
        if current_scale <= 0.9:
            idx = 0  # Крошечный
        elif current_scale <= 1.1:
            idx = 1  # Маленький
        elif current_scale <= 1.4:
            idx = 2  # Средний
        else:
            idx = 3  # Большой
        self.combo_size.setCurrentIndex(idx)
        # change_size() будет вызван автоматически сигналом currentIndexChanged
        
    def change_size(self):
        """Обработка изменения размера интерфейса"""
        selected = self.combo_size.currentText()
        if selected == "Крошечный":
            self.new_scale = 0.8
        elif selected == "Маленький":
            self.new_scale = 1.0
        elif selected == "Средний":
            self.new_scale = 1.2
        elif selected == "Большой":
            self.new_scale = 1.5
        else:  # "Маленький" по умолчанию
            self.new_scale = 1.0
            
    def change_resolution(self):
        """Обработка изменения разрешения"""
        selected = self.combo_res.currentText()
        self.res_width, self.res_height = map(int, selected.split('x'))
        
    def save_changes(self):
        """Сохранение настроек в главное окно"""
        main_window = self.window()
        # Изменяем размер окна
        main_window.resize(self.res_width, self.res_height)
        # Изменяем масштаб интерфейса через менеджер
        self.scale_manager.factor = self.new_scale
        self.close()