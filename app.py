from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '8228.12349876'  # Cambia esto por algo seguro

# Conexión a MongoDB
client = MongoClient("mongodb+srv://david01mc:1234TFM.@tfm-cluster.lrhnd.mongodb.net/?retryWrites=true&w=majority&appName=TFM-Cluster")
db = client['chat_logs_db']
users_collection = db['users']

# Ruta de login / registro
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']

        if action == 'register':
            existing_user = users_collection.find_one({'username': username})
            if existing_user:
                flash('El nombre de usuario ya está registrado. Intente con otro.')
                return redirect(url_for('login'))

            hashed_password = generate_password_hash(password)
            users_collection.insert_one({'username': username, 'password': hashed_password})
            flash('Usuario registrado con éxito.')
            return redirect(url_for('login'))

        elif action == 'login':
            user = users_collection.find_one({'username': username})
            if user and check_password_hash(user['password'], password):
                return redirect(url_for('chat', username=username))
            else:
                flash('Usuario o contraseña incorrectos.')

    return render_template('login.html')

# Ruta del chat
@app.route('/chat/<username>')
def chat(username):
    return render_template('chat.html', username=username)

# API para responder mensajes
@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    user_message = data.get('message', '')

    bot_response = f"Hola, has dicho: {user_message}"
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
