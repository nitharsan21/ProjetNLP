from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/AI', methods=['POST'])
def AI():
    # RECUPERE LE MESSAGE ET LE DECAPSULE
    result = request.get_json()
    print(result)
    message = json.loads(result)
    print(message)

    # ENVOIE LE MESSAGE VERS L'IA
    result = message["msg"]
    print(result)

    # RETOURNE LA REPONSE DE L'IA
    return jsonify({'AImsg': result})


app.debug = True
app.run()
