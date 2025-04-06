from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Criar banco de dados e tabela
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                 )''')
conn.commit()
conn.close()

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name, email = data.get('name'), data.get('email')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid
        return jsonify({"id": user_id, "name": name, "email": email}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email já cadastrado"}), 400
    finally:
        conn.close()

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [dict(id=row[0], name=row[1], email=row[2]) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)