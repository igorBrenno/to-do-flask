import sqlite3 as sqlite

def criarTabela():
    conn = sqlite.connect("gestaoDB.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
            email TEXT NOT NULL
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close

def inserirUsuario(nome, email, senha):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, email, senha) values (? ,? ,?)            
    ''', (nome, email, senha))
    conn.commit()
    conn.close()

def login(email, senha):
    conn = sqlite.connect("gestaoDB.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=? and senha=?", (email, senha))
    dados = cursor.fetchall()
    conn.close()
    if len(dados) > 0:
        return True
    else:
        return False

def verificarUsuario(email):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", [email])
    dados = cursor.fetchall()
    conn.close()
    if len(dados) > 0:
        return True
    else:
        return False
    
def recuperarSenhaBD(nome, email):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE nome=? and email=?", (nome, email))
    senha = cursor.fetchone()
    conn.close()
    return senha