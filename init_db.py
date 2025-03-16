import os
from app import app, db

def init_database():
    # Caminho absoluto pra pasta instance/ dentro de app/
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Diretório do init_db.py
    instance_dir = os.path.join(base_dir, 'app', 'instance')
    os.makedirs(instance_dir, exist_ok=True)  # Cria a pasta se não existir

    # Confirma o caminho do banco
    db_path = os.path.join(instance_dir, 'tasks.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    with app.app_context():
        db.create_all()
        print(f"Database created successfully at: {db_path}")

if __name__ == "__main__":
    init_database()