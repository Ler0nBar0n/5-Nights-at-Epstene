import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from base_overlay import BaseOverlay

class CreateTaskOverlay(BaseOverlay):
    """Оверлей создания задачи"""
    
    def __init__(self, scale_manager, parent=None):
        super().__init__(scale_manager, parent)
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
        
    def update_style(self):
        """Применить масштабирование ко всем элементам оверлея"""
        super().update_style()
        
        sf = self.scale_manager.factor
        scroll_width = self.scale_manager.scale_value(6)
        scroll_radius = self.scale_manager.scale_value(3)
        min_height = self.scale_manager.scale_value(30)
        # Базовый стиль для полей ввода
        base_input_style = f"""
            QLineEdit, QTextEdit {{
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: {self.scale_manager.scale_value(8)}px;
                padding: {self.scale_manager.scale_value(8)}px;
                font-size: {self.scale_manager.scale_value(16)}px;
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
        self.task_title_edit.setFixedHeight(self.scale_manager.scale_value(40))
        self.task_title_edit.setStyleSheet(base_input_style)
        
        # Настройка многострочного поля
        self.task_desc_edit.setMinimumHeight(self.scale_manager.scale_value(80))
        self.task_desc_edit.setMaximumHeight(self.scale_manager.scale_value(150))
        self.task_desc_edit.setStyleSheet(base_input_style)
        
    def save_changes(self):
        title = self.task_title_edit.text()
        description = self.task_desc_edit.toPlainText()
        if title.strip():  # Проверка, что заголовок не пустой
            main_window = self.window()
            if hasattr(main_window, 'create_task'):
                main_window.create_task(title, description)
        self.close()