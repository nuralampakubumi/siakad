
from flask import Flask,  flash, render_template, request, jsonify, url_for, redirect
from backend.db import db 
from backend.users import usersapp
from backend.auth import auth
from backend.mahasiswa import mahasiswa


# membuat variabel menggunakan fungsi class Flask
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'lalla'
app.register_blueprint(usersapp)
app.register_blueprint(auth)
app.register_blueprint(mahasiswa)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)