from flask import Flask, render_template, redirect, request, url_for
from models import Usuario, Todo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import db

app = Flask(__name__)
app.secret_key = 'fodameno'
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario

@app.route('/')
@login_required
# login_required Faz com que só possa acessar essa rota quando estiver logado
def home():
    todos = db.session.query(Todo).filter_by(user_id=current_user.id).all()
    return render_template('home.html', todos=todos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = db.session.query(Usuario).filter_by(email=email, senha=senha).first()
        if not user:
            return 'Nome ou senha incorretos.'
        login_user(user)
        return redirect(url_for('home'))
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)

        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    
    nova_tarefa = Todo(tarefa=todo, status=False, user_id=current_user.id)
    db.session.add(nova_tarefa)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    todo = db.session.query(Todo).filter_by(id=index).first()
    print(todo)
    if request.method == 'POST':
        info = str(request.form['edit-todo'])
        todo.tarefa = info
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('edit.html', todo=todo, index=index)

@app.route('/check/<int:index>')
def check(index):
    print("CHeck")
    todo = db.session.query(Todo).filter_by(id=index).first()
    print(todo)
    if todo:
        todo.status = not todo.status
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:index>')
def delete(index):
    todo = db.session.query(Todo).filter_by(id=index).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return "Todo não encontrado"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)