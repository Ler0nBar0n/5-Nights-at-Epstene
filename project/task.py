import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from base_overlay import BaseOverlay


class TaskWidget(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
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
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.pin.setCursor(Qt.ClosedHandCursor)
            event.accept()

    def pin_mouse_move(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
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
        main_window = self.window()
        sf = getattr(main_window, 'ui_scale_factor', 1.0)

        # Общий стиль виджета
        self.setStyleSheet(f"""
            TaskWidget {{
                background-color: #f5f5f7;
                border: 1px solid #ccc;
                border-radius: {int(3 * sf)}px;
            }}
        """)

        # Пин
        pin_size = int(20 * sf)
        self.pin.setFixedSize(pin_size, pin_size)
        self.pin.setStyleSheet(f"""
            QLabel {{
                background-color: #FF3B30;
                border-radius: {pin_size//2}px;
            }}
        """)

        # Шрифт заголовка
        title_font = QFont()
        title_font.setPointSize(int(14 * sf))
        title_font.setBold(True)
        self.title_edit.setFont(title_font)

        # Описание (стиль)
        desc_font_size = int(12 * sf)
        self.desc_label.setStyleSheet(f"font-size: {desc_font_size}px; color: #666;")

        # Отступы внутри виджета
        margin = int(5 * sf)
        self.layout().setContentsMargins(margin, margin, margin, margin)
        self.layout().setSpacing(int(5 * sf))

        # Фиксированные размеры виджета
        self.setFixedWidth(int(100 * sf))
        self.setFixedHeight(int(140 * sf))

        # Доступная ширина для текста
        text_width = self.width() - 2 * margin
        self.title_edit.setFixedWidth(text_width)

        # Параметры скроллбара (как в DrawerScrollArea)
        scroll_width = int(6 * sf)
        scroll_radius = int(3 * sf)
        min_height = int(30 * sf)

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
    def create_task(parent, title, description):
        return TaskWidget(title, description, parent)


class ViewTaskOverlay(BaseOverlay):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title.setText("Просмотр задачи")
        self.setup_content()

    def setup_content(self):
        main_window = self.window()
        sf = getattr(main_window, 'ui_sf_factor', 1.0)
        self.save_btn.setText("Принять")
        self.cancel_btn.setText("Закрыть")

        self.view_title = QLabel()
        self.view_title.setWordWrap(True)
        self.view_title.setStyleSheet(f"font-weight: bold; font-size: {int(18*sf)}px;")

        self.view_desc = QLabel()
        self.view_desc.setWordWrap(True)
        self.view_desc.setStyleSheet(f"font-size: {int(16*sf)}px;")

        self.content_layout.insertWidget(0, self.view_title)
        self.content_layout.insertWidget(1, self.view_desc)
        self.content_layout.addStretch()

    def set_task_data(self, title, description):
        self.view_title.setText(title)
        self.view_desc.setText(description)

    def change_sf(self):
        super().change_sf()
        main_window = self.window()
        sf = getattr(main_window, 'ui_sf_factor', 1.0)

        title_font_size = int(18 * sf)
        desc_font_size = int(16 * sf)
        self.view_title.setStyleSheet(f"font-weight: bold; font-size: {title_font_size}px;")
        self.view_desc.setStyleSheet(f"font-size: {desc_font_size}px;")

    def save_changes(self):
        self.close()