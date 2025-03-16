from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'tasks.db'

def get_db_connection():
    """Returns a connection to the database."""  # Updated translation
    return sqlite3.connect(DATABASE)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Only creates the database the first time (can be moved to init_db.py)  # Updated translation
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT)''')

    if request.method == 'POST':
        new_task = request.form['task']
        with get_db_connection() as conn:
            conn.execute("INSERT INTO tasks (name) VALUES (?)", (new_task,))
            conn.commit()
        return redirect(url_for('home'))

    with get_db_connection() as conn:
        tasks = conn.execute("SELECT id, name FROM tasks").fetchall()

    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
