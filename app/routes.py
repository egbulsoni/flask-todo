from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Task

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_task = Task(name=request.form['task'])
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))