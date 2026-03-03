import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from base_overlay import BaseOverlay

class TaskWidget(QFrame):
    def __init__(self, title, description, scale_manager, parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.scale_manager = scale_manager
        self.scale_manager.scaleFactorChanged.connect(self.update_style)
        self.dragging = False
        self.drag_position = QPoint()
        self.setup_ui()
        self.update_style()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)

        # Пин
        self.pin = QLabel()
        self.pin.setFixedSize(20, 20)
        self.pin.setStyleSheet("""
            QLabel {
                background-color: #FF3B30;
                border-radius: 10px;
            }
        """)
        self.pin.setCursor(Qt.OpenHandCursor)
        layout.addWidget(self.pin, 0, Qt.AlignHCenter)

        # Текст (заголовок)
        self.title_edit = QTextEdit()
        self.title_edit.setPlainText(self.title)
        self.title_edit.setReadOnly(True)
        self.title_edit.setFrameStyle(QFrame.NoFrame)
        self.title_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.title_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.title_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.title_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.title_edit.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.title_edit)

        # Описание (скрыто)
        self.desc_label = QLabel(self.description)
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setVisible(False)
        layout.addWidget(self.desc_label)

        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)

        # Обработчики мыши
        self.pin.mousePressEvent = self.pin_mouse_press
        self.pin.mouseMoveEvent = self.pin_mouse_move
        self.pin.mouseReleaseEvent = self.pin_mouse_release
        self.mousePressEvent = self.widget_mouse_press

    def pin_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            # Запоминаем смещение курсора внутри виджета
            self.drag_offset = event.pos()
            self.pin.setCursor(Qt.ClosedHandCursor)
            event.accept()

    def pin_mouse_move(self, event):
        if self.dragging:
            parent = self.parent()
            if parent is None:
                return

            # Позиция курсора в координатах родителя
            parent_pos = self.mapToParent(event.pos())
            # Вычисляем новую позицию верхнего левого угла виджета
            new_pos = parent_pos - self.drag_offset

            # Ограничиваем перемещение в пределах родительского контейнера
            x = new_pos.x()
            y = new_pos.y()
            x = max(0, min(x, parent.width() - self.width()))
            y = max(0, min(y, parent.height() - self.height()))

            self.move(x, y)
            event.accept()

    def pin_mouse_release(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.pin.setCursor(Qt.OpenHandCursor)
            event.accept()

    def widget_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            main_window = self.window()
            if hasattr(main_window, 'open_view_task'):
                main_window.open_view_task(self.title, self.description)
            event.accept()
            
    def update_style(self):
        sf = self.scale_manager.factor

        # Общий стиль виджета
        self.setStyleSheet(f"""
            TaskWidget {{
                background-color: #f5f5f7;
                border: 1px solid #ccc;
                border-radius: {self.scale_manager.scale_value(3)}px;
            }}
        """)

        # Пин
        pin_size = self.scale_manager.scale_value(20)
        self.pin.setFixedSize(pin_size, pin_size)
        self.pin.setStyleSheet(f"""
            QLabel {{
                background-color: #FF3B30;
                border-radius: {pin_size//2}px;
            }}
        """)

        # Шрифт заголовка
        title_font = QFont()
        title_font.setPointSize(self.scale_manager.scale_value(14))
        title_font.setBold(True)
        self.title_edit.setFont(title_font)

        # Описание (стиль)
        desc_font_size = self.scale_manager.scale_value(12)
        self.desc_label.setStyleSheet(f"font-size: {desc_font_size}px; color: #666;")

        # Отступы внутри виджета
        margin = self.scale_manager.scale_value(5)
        self.layout().setContentsMargins(margin, margin, margin, margin)
        self.layout().setSpacing(self.scale_manager.scale_value(5))

        # Фиксированные размеры виджета
        self.setFixedWidth(self.scale_manager.scale_value(100))
        self.setFixedHeight(self.scale_manager.scale_value(140))

        # Доступная ширина для текста
        text_width = self.width() - 2 * margin
        self.title_edit.setFixedWidth(text_width)

        # Параметры скроллбара
        scroll_width = self.scale_manager.scale_value(6)
        scroll_radius = self.scale_manager.scale_value(3)
        min_height = self.scale_manager.scale_value(30)

        # Применяем стиль к самому QTextEdit (фон и отступы)
        self.title_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)

        # Стилизуем вертикальный скроллбар напрямую
        scrollbar = self.title_edit.verticalScrollBar()
        if scrollbar:
            scrollbar.setStyleSheet(f"""
                QScrollBar:vertical {{
                    background-color: transparent;
                    width: {scroll_width}px;
                    border-radius: {scroll_radius}px;
                    border: none;
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
            """)

class TaskFactory:
    @staticmethod
    def create_task(parent, title, description, scale_manager):
        return TaskWidget(title, description, scale_manager, parent)


class ViewTaskOverlay(BaseOverlay):
    def __init__(self, scale_manager, parent=None):
        super().__init__(scale_manager, parent)
        self.title.setText("Просмотр задачи")

    def setup_ui(self):
        super().setup_ui()
        self.save_btn.setText("Принять")
        self.cancel_btn.setText("Закрыть")

        self.view_title = QLabel()
        self.view_title.setWordWrap(True)
        # Стиль будет обновлён в update_style

        self.view_desc = QLabel()
        self.view_desc.setWordWrap(True)
        
        self.content_layout.insertWidget(0, self.view_title)
        self.content_layout.insertWidget(1, self.view_desc)
        self.content_layout.addStretch()

        self.update_style()  # принудительно применим стиль для новых элементов

    def set_task_data(self, title, description):
        self.view_title.setText(title)
        self.view_desc.setText(description)

    def update_style(self):
        super().update_style()
        sf = self.scale_manager.factor

        title_font_size = self.scale_manager.scale_value(18)
        desc_font_size = self.scale_manager.scale_value(16)
        self.view_title.setStyleSheet(f"font-weight: bold; font-size: {title_font_size}px;")
        self.view_desc.setStyleSheet(f"font-size: {desc_font_size}px;")

    def save_changes(self):
        self.close()