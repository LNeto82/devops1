from flask import Flask, jsonify
import requests
import json
import redis

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

PRODUCT_CACHE_KEY = 'product'

@app.route('/order', methods=['GET'])
def create_order():
    # Verifica se existe dado no Redis
    cached = cache.get(PRODUCT_CACHE_KEY)

    if cached:
        try:
            # ⚠️ garante que é JSON válido
            product = json.loads(cached)
            print("CACHE HIT: produto obtido do cache")
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON do cache:", e)
            cache.delete(PRODUCT_CACHE_KEY)  # remove valor inválido
            return jsonify({'error': 'Produto em cache corrompido, cache limpo'}), 500
    else:
        # Busca da API Node.js
        try:
            response = requests.get('http://localhost:4001/products')
            response.raise_for_status()
            products_list = response.json().get('products')
            if not products_list:
                return jsonify({'error': 'Nenhum produto encontrado na API'}), 404
            product = products_list[0]  # pega o primeiro

            # ✅ Salva como JSON válido (aspas duplas)
            cache.set(PRODUCT_CACHE_KEY, json.dumps(product), ex=60)
            print("CACHE MISS: produto buscado da API e salvo no cache")
        except Exception as e:
            return jsonify({'error': 'Erro ao buscar produto da API: ' + str(e)}), 500

    return jsonify(product)


if __name__ == '__main__':
    app.run(port=4002)
