import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from base_overlay import BaseOverlay

class CreateTaskOverlay(BaseOverlay):
    """Оверлей создания задачи"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title.setText("Создать задачу")
        
    def setup_ui(self):
        super().setup_ui()
        
        # Поле для главного (однострочное)
        self.task_title_edit = QLineEdit()
        self.task_title_edit.setPlaceholderText("Главное")
        self.task_title_edit.setMaxLength(100)
        # Вставляем в начало content_layout, чтобы было сверху
        self.content_layout.insertWidget(0, self.task_title_edit)
        
        # Поле для пояснения (многострочное)
        self.task_desc_edit = QTextEdit()
        self.task_desc_edit.setPlaceholderText("Пояснение")
        self.content_layout.insertWidget(1, self.task_desc_edit)
        
    def change_scale(self):
        """Применить масштабирование ко всем элементам оверлея"""
        super().change_scale()
        
        main_window = self.window()
        sf = getattr(main_window, 'ui_scale_factor', 1.0)
        scroll_width = int(6 * sf)
        scroll_radius = int(3 * sf)
        min_height = int(30 * sf)
        # Базовый стиль для полей ввода
        base_input_style = f"""
            QLineEdit, QTextEdit {{
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: {int(8 * sf)}px;
                padding: {int(8 * sf)}px;
                font-size: {int(16 * sf)}px;
                font-weight: bold;
                color: #333333;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid #007AFF;
            }}
            /*Область прокрутки*/
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: transparent;
                width: {scroll_width}px;
                border-radius: {scroll_radius}px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: {scroll_radius}px;
                min-height: {min_height}px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: rgba(0, 0, 0, 0.3);
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """
        
        # Настройка однострочного поля
        self.task_title_edit.setFixedHeight(int(40 * sf))
        self.task_title_edit.setStyleSheet(base_input_style)
        
        # Настройка многострочного поля
        self.task_desc_edit.setMinimumHeight(int(80 * sf))
        self.task_desc_edit.setMaximumHeight(int(150 * sf))
        self.task_desc_edit.setStyleSheet(base_input_style)
        
    def save_changes(self):
        title = self.task_title_edit.text()
        description = self.task_desc_edit.toPlainText()
        if title.strip():  # Проверка, что заголовок не пустой
            main_window = self.window()
            if hasattr(main_window, 'create_task'):
                main_window.create_task(title, description)
        self.close()