from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from werkzeug.wrappers import Response
from werkzeug.routing import Map, Rule
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

# Lista em memória
tarefas = [("Teste 1", 1), ("Teste 2", 2)]

# Adaptador pra Flask-style routing
url_map = Map([
    Rule('/', endpoint='home', methods=['GET', 'POST']),
    Rule('/deletar/<int:id>', endpoint='deletar', methods=['GET'])
])

def home(request: Request):
    print("Acessando a rota home...")
    global tarefas
    if request.method == "POST":
        form = request.form
        nova_tarefa = form.get('tarefa', '')
        if nova_tarefa:
            novo_id = max([t[1] for t in tarefas], default=0) + 1
            tarefas.append((nova_tarefa, novo_id))
            print(f"Tarefa adicionada: {nova_tarefa}, ID: {novo_id}")
    print(f"Tarefas atuais: {tarefas}")
    return templates.TemplateResponse('index.html', {"request": request, "tarefas": [(t[1], t[0]) for t in tarefas]})

def deletar(request: Request, id: int):
    print(f"Tentando deletar tarefa com ID: {id}")
    global tarefas
    tarefas = [t for t in tarefas if t[1] != id]
    print(f"Tarefas após deletar: {tarefas}")
    return templates.TemplateResponse('index.html', {"request": request, "tarefas": [(t[1], t[0]) for t in tarefas]})

# Monta o dispatcher
endpoints = {
    'home': home,
    'deletar': deletar
}

def application(environ, start_response):
    request = Request(environ)
    urls = url_map.bind_to_environ(environ)
    endpoint, kwargs = urls.match()
    response = endpoints[endpoint](request, **kwargs)
    return Response.from_app(response, environ)(environ, start_response)

app.mount("/", WSGIApplication(application))

# Handler pro Vercel
def handler():
    return app