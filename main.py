from flask import Flask, render_template, request, flash
import gestaoBD

app = Flask(__name__)

gestaoBD.criarTabela()

usuarios = []

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastrarUsuario", methods=["POST"])
def cadastrarUsuario():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = str(request.form.get("senha"))
    if(gestaoBD.verificarUsuario(email)==False):
        gestaoBD.inserirUsuario(nome, email, senha)
        flash("Cadastro realizado com sucesso! Faça login.", "sucess")
        return render_template("login.html")
    else:
        return render_template("cadastro.html")

@app.route("/autenticarUsuaruio", methods=["POST"])
def autenticar():
    email = request.form.get("emal")
    senha = str(request.form.get("senha"))

    logado = gestaoBD.login(email, senha)
    if (logado == True):
        return render_template("todo-list.html")
    else:
        flash("Email ou senha incorretos", "danger")
        return render_template("login.html")


@app.route("/todo-list")
def todolist():
    return render_template("todo-list.html")

app.run(debug=True)

