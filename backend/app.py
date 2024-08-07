"""
Main application module for the Task Manager application.
Handles routes, user authentication, task management, and real-time updates.
"""
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, join_room, leave_room
from forms import LoginForm, RegisterForm, TaskForm, UpdateTaskForm
from models import User
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config["MONGO_URI"] = "mongodb://localhost:27017/taskmanager"

mongo = PyMongo(app)
socketio = SocketIO(app)  
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
    
@socketio.on('join')
def on_join(data):
    """Handles a user joining a room for real-time updates."""
    room = data['room']
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    """ Handles a user leaving a room for real-time updates."""
    room = data['room']
    leave_room(room)

@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the database by user ID."""
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(str(user_data["_id"]), user_data["username"], user_data["password"])
    return None

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user_data = mongo.db.users.find_one({"username": form.username.data})
        if user_data and user_data["password"] == form.password.data:
            user = User(str(user_data["_id"]), user_data["username"], user_data["password"])
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    form = RegisterForm()
    if form.validate_on_submit():
        if not mongo.db.users.find_one({"username": form.username.data}):
            user_id = mongo.db.users.insert_one({
                "username": form.username.data,
                "password": form.password.data
            }).inserted_id
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
        flash('Username already exists.')
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """ Logs the user out and redirects to the home page."""
    logout_user()
    return redirect(url_for('home'))

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    """Renders the task management page and handles task creation."""
    form = TaskForm()
    if form.validate_on_submit():
        task_id = mongo.db.tasks.insert_one({
            "user_id": str(current_user.id),  # Ensure user_id is a string
            "title": form.title.data,
            "description": form.description.data
        }).inserted_id
        task = mongo.db.tasks.find_one({"_id": task_id})
        socketio.emit('new_task', {'task_id': str(task["_id"]), 'task': task}, room=current_user.id)
        return redirect(url_for('tasks'))
    
    user_tasks = mongo.db.tasks.find({"user_id": str(current_user.id)})
    tasks = {str(task["_id"]): task for task in user_tasks}
    print(f"Fetched tasks for user {current_user.id}: {tasks}")  # Debugging print statement
    return render_template('tasks.html', form=form, tasks=tasks)

@app.route('/task/<task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    """Handles task update."""
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id), "user_id": str(current_user.id)})
    if not task:
        return redirect(url_for('tasks'))
    form = UpdateTaskForm()
    if form.validate_on_submit():
        mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {
            "title": form.title.data,
            "description": form.description.data
        }})
        updated_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        socketio.emit('update_task', {'task_id': str(updated_task["_id"]), 'task': updated_task}, room=current_user.id)
        return redirect(url_for('tasks'))
    form.title.data = task['title']
    form.description.data = task['description']
    return render_template('update_task.html', form=form)

@app.route('/task/delete/<task_id>')
@login_required
def delete_task(task_id):
    """Handles task deletion."""
    mongo.db.tasks.delete_one({"_id": ObjectId(task_id), "user_id": str(current_user.id)})
    socketio.emit('delete_task', {'task_id': task_id}, room=current_user.id)
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    socketio.run(app, debug=True)