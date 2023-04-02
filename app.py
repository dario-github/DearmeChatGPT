import gradio as gr
import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["dearme_chat"]
users = mongo_db["users"]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({"_id": int(user_id)})
    if user_data:
        return User(user_data["_id"], user_data["username"], user_data["password"])
    else:
        return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.find_one({"username": username}):
            return "Username already exists!"
        users.insert_one({"username": username, "password": password})
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({"username": username})
        if user and user["password"] == password:
            login_user(User(user["_id"], user["username"], user["password"]))
            return redirect(url_for('protected'))
        else:
            return "Incorrect username or password."
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/protected_gradio_interface')
@login_required
def protected_gradio_interface():
    iface = gr.Interface.load("huggingface/prayuth/api-key")
    return iface.serve_files()


@app.route('/gradio', methods=['GET'])
@login_required
def gradio():
    gradio_url = "https://chat.dariolink.ml"
    return render_template("gradio.html", gradio_url=gradio_url)

@app.route('/')
def index():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
