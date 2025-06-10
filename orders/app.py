from flask import Flask, jsonify
import redis
import requests
import mysql.connector

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/order')
def create_order():
    cached = cache.get('product')
    if cached:
        product = eval(cached)
    else:
        r = requests.get('http://products:3001/products')
        product = r.json()['products'][0]
        cache.set('product', str(product))

    db = mysql.connector.connect(
        host="db",
        user="root",
        password="example",
        database="ecommerce"
    )
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, quantity INT, total_price INT)")
    cursor.execute("INSERT INTO orders (product_id, quantity, total_price) VALUES (%s, %s, %s)", (product['id'], 2, product['price'] * 2))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({
        "order_id": 101,
        "product_id": product['id'],
        "quantity": 2,
        "total_price": product['price'] * 2
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
