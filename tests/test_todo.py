import pytest
import os
from app import app, db
from app.models import Task

@pytest.fixture
def client():
    # Absolute path to the instance/ folder inside app/
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Directory of test_todo.py
    instance_dir = os.path.join(base_dir, '..', 'app', 'instance')  # Go back to the root and enter app/instance
    os.makedirs(instance_dir, exist_ok=True)  # Create the folder if it does not exist

    # Set up the test database
    test_db_path = os.path.join(instance_dir, 'test.db')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{test_db_path}'

    with app.app_context():
        db.create_all()
    yield app.test_client()
    with app.app_context():
        db.drop_all()
        # Remove the test file to avoid future conflicts
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

def test_home_get(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task(client):
    response = client.post('/', data={'task': 'Fazer café'})
    assert response.status_code == 302
    with app.app_context():
        task = Task.query.filter_by(name='Fazer café').first()
        assert task is not None

def test_delete_task(client):
    with app.app_context():
        task = Task(name='Teste')
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    response = client.get(f'/delete/{task_id}')
    assert response.status_code == 302
    with app.app_context():
        task = Task.query.get(task_id)
        assert task is None
