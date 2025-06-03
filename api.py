from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'dados.db'

# Inicializa o banco e cria tabela se não existir
def inicializar_banco():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ph (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL,
            horario TEXT
        )
    ''')
    conn.commit()
    conn.close()

inicializar_banco()

@app.route('/enviar', methods=['POST'])
def enviar_ph():
    data = request.get_json()
    ph = data.get("ph")
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO ph (valor, horario) VALUES (?, ?)", (ph, horario))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "ph_recebido": ph, "horario": horario})

@app.route('/obter', methods=['GET'])
def obter_ph():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, horario FROM ph ORDER BY id DESC LIMIT 1")
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return jsonify({"ph": resultado[0], "horario": resultado[1]})
    else:
        return jsonify({"ph": None, "horario": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
