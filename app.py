from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content:
            new_task = Task(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
    else:
        tasks = Task.query.order_by(Task.id).all()
        return render_template('index.html', tasks=tasks)

@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    try:
        task.completed = True
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue completing your task'

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task'

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
