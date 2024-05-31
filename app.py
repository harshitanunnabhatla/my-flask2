from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging

# Initialize the Flask application
app = Flask(__name__)

# Configuring the SQLAlchemy part of the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create the database and the database tables
with app.app_context():
    db.create_all()

# Define the index route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content:
            new_task = Task(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect(url_for('index'))
            except Exception as e:
                logging.error("Error adding task: %s", e)
                return 'There was an issue adding your task'
    else:
        tasks = Task.query.order_by(Task.id).all()
        return render_template('index.html', tasks=tasks)

# Define the complete task route
@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    try:
        task.completed = True
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        logging.error("Error completing task: %s", e)
        return 'There was an issue completing your task'

# Define the delete task route
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        logging.error("Error deleting task: %s", e)
        return 'There was an issue deleting your task'
