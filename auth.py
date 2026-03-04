import sys
from PyQt5.QtWidgets import QApplication,QMessageBox, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget

class TavernaApp(QWidget):
    def __init__(self):
        super().__init__()

        # Настройки главного окна
        self.setWindowTitle("Таверна - Вход") 
        self.resize(300, 200)

        # Создаем "стопку" для экранов
        self.stacked_widget = QStackedWidget()

        # Создаем два наших экрана
        self.login_screen = self.setup_login_screen()
        self.register_screen = self.setup_register_screen()

        # Добавляем их в стопку
        self.stacked_widget.addWidget(self.login_screen)    # Это индекс 0
        self.stacked_widget.addWidget(self.register_screen) # Это индекс 1

        # Основной слой, который держит стопку
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def setup_login_screen(self):
        """Экран входа: 2 поля и кнопка перехода"""
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Авторизация"))
        
        # Поля ввода
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.Password) # Скрывает символы
        layout.addWidget(self.pass_input)

        # Кнопки
        btn_login = QPushButton("Войти")
        layout.addWidget(btn_login)

        btn_to_reg = QPushButton("Нет аккаунта? Зарегистрироваться")
        # При нажатии меняем индекс на 1 (экран регистрации)
        btn_to_reg.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(btn_to_reg)

        page.setLayout(layout)
        return page

    def setup_register_screen(self):
        """Экран регистрации с проверкой пароля"""
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<h2>Регистрация</h2>"))
        
        self.reg_login = QLineEdit()
        self.reg_login.setPlaceholderText("Придумайте логин")
        layout.addWidget(self.reg_login)

        # Поле для первого ввода пароля
        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Придумайте пароль")
        self.reg_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_pass)

        # Поле для подтверждения
        self.reg_pass_confirm = QLineEdit()
        self.reg_pass_confirm.setPlaceholderText("Повторите пароль")
        self.reg_pass_confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_pass_confirm)

        # Кнопка создания аккаунта
        btn_reg = QPushButton("Создать аккаунт")
        # Теперь кнопка вызывает специальную функцию проверки
        btn_reg.clicked.connect(self.handle_registration)
        layout.addWidget(btn_reg)

        btn_back = QPushButton("Назад ко входу")
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_back)

        page.setLayout(layout)
        return page

    def handle_registration(self):
        """Логика проверки паролей"""
        login = self.reg_login.text()
        pass1 = self.reg_pass.text()
        pass2 = self.reg_pass_confirm.text()

        # Тестируем условия
        if not login or not pass1:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if pass1 == pass2:
            # Если пароли совпали
            QMessageBox.information(self, "Успех", f"Аккаунт {login} успешно создан!")
            # Тут в будущем Михаил (бэкенд) подключит базу данных [cite: 17, 19]
            self.stacked_widget.setCurrentIndex(0) # Возвращаем на вход
        else:
            # Если пароли разные
            QMessageBox.critical(self, "Ошибка", "Пароли не совпадают! Попробуйте еще раз.")
            self.reg_pass.clear() # Очищаем поля, чтобы ввести заново
            self.reg_pass_confirm.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TavernaApp()
    window.show()
    sys.exit(app.exec_())