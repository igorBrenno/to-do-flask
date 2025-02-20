from flask import Flask, render_template, request, flash
import gestaoBD

app = Flask(__name__)

gestaoBD.criarTabela()
app.secret_key = "GeeksForGeeks"

usuarios = []

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = str(request.form.get("senha"))
        if(gestaoBD.verificarUsuario(email)==False):
            gestaoBD.inserirUsuario(nome, email, senha)
            flash("Cadastro realizado com sucesso! Faça login.", "sucess")
            return render_template("login.html")
    return render_template("cadastro.html")

@app.route("/autenticarUsuario", methods=["POST", "GET"])
def autenticar():
    email = request.form.get("email")
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

def listarUsuarios():
    #return render_template("lista.html", lista=lista_usuarios)
    lista_usuariosDB = gestaoBD.listarUsuarios()
    return render_template("lista.html", lista=lista_usuariosDB)

app.run(debug=True)

