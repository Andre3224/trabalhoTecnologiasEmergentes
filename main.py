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
    return redirect(url_for('login')) #modificar para colocar um fundo com 2 botoes

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

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form['action']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        if action == 'update':
            new_password = request.form['new_password']
            hashed_pw = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_pw, session['user_id']))
            conn.commit()
            flash("Senha atualizada com sucesso!", "success")

        elif action == 'delete':
            cursor.execute("DELETE FROM users WHERE id = ?", (session['user_id'],))
            conn.commit()
            session.clear()
            conn.close()
            flash("Conta deletada com sucesso.", "info")
            return redirect(url_for('register'))

        conn.close()
    return render_template('account.html', username=session['username'])

@app.route('/admin')
def admin_panel():
    if 'username' not in session or session['username'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('admin.html', users=users)


@app.route('/admin/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if 'username' in session and session['username'] == 'admin':
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
    return redirect('/admin')


if __name__ == '__main__':
    inicio_db()
    app.run(debug=True)
