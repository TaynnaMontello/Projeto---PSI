from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from database import get_db_connection  # Função que retorna conexão com o banco

app = Flask(__name__)
app.secret_key = "supersecreto123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(id=user_data['id'], nome=user_data['nome'], email=user_data['email'])
    return None

@app.route('/')
def index():
    return render_template('base.html', usuario=current_user)

from flask import make_response

@app.route('/lembrar_usuario')
def lembrar_usuario():
    resposta = make_response(redirect(url_for('index')))
    resposta.set_cookie('nome_usuario', current_user.nome)
    return resposta

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template('500.html'), 500


@app.route('/cadastrar_pessoa', methods=['GET', 'POST'])
def cadastrar_pessoa():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        senha = request.form['senha'].strip()

        if not nome or not email or not senha:
            flash('Preencha todos os campos.')
            return redirect(url_for('cadastrar_pessoa'))

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            conn.close()
            flash('Este e-mail já está cadastrado.')
            return redirect(url_for('cadastrar_pessoa'))

        senha_hash = generate_password_hash(senha)

        cursor.execute(
            'INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
            (nome, email, senha_hash)
        )
        conn.commit()
        conn.close()

        flash('Usuário registrado com sucesso!')
        return redirect(url_for('login'))

    return render_template('cadastrar_pessoa.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        senha = request.form['senha'].strip()

        if not email or not senha:
            flash('Preencha todos os campos, por favor 💌')
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['senha'], senha):
            user = User(id=usuario['id'], nome=usuario['nome'], email=usuario['email'])
            login_user(user)
            flash('Login feito com sucesso!')
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/projetos/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_projeto():
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        descricao = request.form['descricao'].strip()
        usuario = current_user.nome  # nome do usuário logado

        if not titulo or not descricao:
            flash('Todos os campos devem ser preenchidos.')
            return redirect(url_for('cadastrar_projeto'))

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO projetos (titulo, descricao, usuario) VALUES (?, ?, ?)',
            (titulo, descricao, usuario)
        )
        conn.commit()
        conn.close()

        flash('Projeto cadastrado com sucesso!')
        return redirect(url_for('listar_projetos'))

    return render_template('cadastrar_projeto.html')

@app.route('/projetos')
def listar_projetos():
    conn = sqlite3.connect('jogo.db')
    conn.row_factory = sqlite3.Row  # para poder acessar como dicionário
    cursor = conn.cursor()

    # Seleciona tudo menos o id, ordenando do mais novo para o mais antigo
    cursor.execute("SELECT titulo, descricao, usuario FROM projetos ORDER BY id DESC")
    projetos = cursor.fetchall()

    conn.close()
    return render_template('projetos.html', projetos=projetos)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu com sucesso! 💔')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
