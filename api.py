from flask import Flask, request, jsonify

app = Flask(__name__)
valor_ph = {"ph": None}  # Dado armazenado na memória

@app.route('/enviar', methods=['POST'])
def enviar_ph():
    data = request.get_json()
    valor_ph["ph"] = data.get("ph")
    return jsonify({"status": "ok", "ph_recebido": valor_ph["ph"]})

@app.route('/obter', methods=['GET'])
def obter_ph():
    return jsonify(valor_ph)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
