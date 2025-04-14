from flask import Flask, request, jsonify
from flasgger import Swagger
import psycopg2
from psycopg2 import sql, DatabaseError

app = Flask(__name__)
swagger = Swagger(app)

# Подключение к базе данных PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="qwe",
        user="postgres",
        password="1",
        host="localhost",
        port="5432"

    )
    conn.autocommit = True
    print("Подключение к базе данных успешно!")
except DatabaseError as e:
    print(f"Ошибка подключения к базе данных: {e}")
    exit()

cur = conn.cursor()


@app.route('/add_game', methods=['POST'])
def add_game():
    """
    Добавить игру в базу данных.
    ---
    parameters:
      - name: name
        in: body
        required: true
        type: string
        description: Название игры
      - name: price
        in: body
        required: true
        type: number
        format: float
        description: Цена игры
      - name: quantity
        in: body
        required: true
        type: integer
        description: Количество игр в наличии
    responses:
      200:
        description: Данные успешно сохранены
      400:
        description: Некорректные данные
      500:
        description: Ошибка при сохранении данных
    """
    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    if not name or price is None or quantity is None:
        return jsonify({"error": "Некорректные данные"}), 400

    try:
        cur.execute(
            "INSERT INTO games (name, price, quantity) VALUES (%s, %s, %s)",
            (name, float(price), int(quantity))
        )
        print(f"Добавлена игра: {name}, Цена: {price}, Количество: {quantity}")
        return jsonify({"message": "Данные сохранены!"}), 200
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
        return jsonify({"error": "Ошибка при сохранении данных"}), 500


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

cur.close()
conn.close()