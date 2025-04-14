import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class GameClient(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавление игры")
        self.setGeometry(100, 100, 300, 200)

        # Основной макет
        layout = QVBoxLayout(self)  # Передаем self, чтобы макет применился к окну

        # Поля ввода
        self.name_label = QLabel("Название игры:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.price_label = QLabel("Цена:")
        self.price_input = QLineEdit()
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)

        self.quantity_label = QLabel("Количество:")
        self.quantity_input = QLineEdit()
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        # Кнопка отправки данных
        self.submit_button = QPushButton("Добавить игру")
        self.submit_button.clicked.connect(self.send_data)
        layout.addWidget(self.submit_button)

    def send_data(self):
        name = self.name_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()

        if not name or not price or not quantity:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и количество должны быть числами!")
            return

        data = {
            "name": name,
            "price": price,
            "quantity": quantity
        }

        try:
            response = requests.post("http://localhost:5000/add_game", json=data)
            response_data = response.json()

            if response.status_code == 200:
                QMessageBox.information(self, "Успех", response_data.get("message", "Данные сохранены!"))
            else:
                QMessageBox.warning(self, "Ошибка", response_data.get("error", "Ошибка при сохранении данных."))
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к серверу!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameClient()
    window.show()
    sys.exit(app.exec())  # В PyQt6 используется exec(), а не exec_()
