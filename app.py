from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Debug: pra ver se o app tá iniciando
print("Iniciando o Flask app...")

# Usa uma lista em memória em vez de SQLite
tarefas = [("Teste 1", 1), ("Teste 2", 2)]  # Simula o formato (nome, id)

@app.route('/', methods=['GET', 'POST'])
def home():
    print("Acessando a rota home...")
    global tarefas
    if request.method == 'POST':
        nova_tarefa = request.form['tarefa']
        # Adiciona a nova tarefa com um "id" incremental
        novo_id = max([t[1] for t in tarefas], default=0) + 1
        tarefas.append((nova_tarefa, novo_id))
        print(f"Tarefa adicionada: {nova_tarefa}, ID: {novo_id}")
        return redirect(url_for('home'))

    print(f"Tarefas atuais: {tarefas}")
    return render_template('index.html', tarefas=[(t[1], t[0]) for t in tarefas])  # Inverte pra o template

@app.route('/deletar/<int:id>')
def deletar(id):
    print(f"Tentando deletar tarefa com ID: {id}")
    global tarefas
    tarefas = [t for t in tarefas if t[1] != id]
    print(f"Tarefas após deletar: {tarefas}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"Rodando Flask na porta {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)