from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'um3dfhc%p=x$*uiv!313gevyk-)@ghh0tj42o5_k_z59-83ayc'

def inicio_db(): #abrir o banco de dados
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')#Definir tela inicial
def index():
    return redirect(url_for('register')) #modificar para colocar um fundo com 2 botoes

@app.route('/register', methods=['GET', 'POST']) #Resposvavel pelo registro, enviar ou receber
def register():
    if request.method == 'POST':
        username = request.form['username'] #Coletar dados
        password = generate_password_hash(request.form['password'])

        try: #Inserir no BD
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Usuário registrado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe.', 'danger')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) #Similar ao Registro porém responsavel pelo Login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Login inválido.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')#abre a tela inicial (sem nada, apenas um olá)
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    inicio_db()
    app.run(debug=True)
