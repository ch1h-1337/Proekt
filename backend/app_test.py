import unittest
from flask import Flask, jsonify, request
from flask.testing import FlaskClient
from unittest.mock import patch
from server import app  # Замените на имя вашего файла с сервером


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_add_game_success(self):
        data = {
            "name": "Game Name",
            "price": 19.99,
            "quantity": 10
        }
        response = self.client.post("/add_game", json=data)

        # Декодируем байтовую строку в UTF-8 и проверяем, что данные сохранены
        response_data = response.json()  # Это если сервер возвращает JSON
        self.assertIn("Данные сохранены!", response_data.get("message", ""))

    # Остальные тесты остаются такими же


if __name__ == "__main__":
    unittest.main()
