from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def criar_banco():
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY, nome TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    criar_banco()

    if request.method == 'POST':
        nova_tarefa = request.form['tarefa']
        conn = sqlite3.connect('tarefas.db')
        c = conn.cursor()
        c.execute("INSERT INTO tarefas (nome) VALUES (?)", (nova_tarefa,))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))  # Volta pra página principal após adicionar

    # Pega as tarefas com id e nome
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("SELECT id, nome FROM tarefas")
    tarefas = c.fetchall()  # Pega tudo como tuplas (id, nome)
    conn.close()

    return render_template('index.html', tarefas=tarefas)

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))  # Volta pra página principal após deletar

if __name__ == '__main__':
    app.run(debug=True)