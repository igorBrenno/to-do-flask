from db import db
# from sqlalchemy import Boolean
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(350), nullable=False)

    todos = db.relationship('Todo', backref='owner', lazy=True)

class Todo(UserMixin, db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    tarefa = db.Column(db.String(200))
    status = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)