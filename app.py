from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Debug: pra ver se o app tá iniciando
print("Iniciando o Flask app...")

def criar_banco():
    print("Criando banco de dados...")
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
        return redirect(url_for('home'))

    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("SELECT id, nome FROM tarefas")
    tarefas = c.fetchall()
    conn.close()

    return render_template('index.html', tarefas=tarefas)

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"Rodando Flask na porta {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)