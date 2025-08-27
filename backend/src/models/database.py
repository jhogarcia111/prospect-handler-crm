import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_database(app):
    """Inicializa la configuración de la base de datos"""
    
    # Configuración para MySQL
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_database = os.environ.get('MYSQL_DATABASE', 'prospect_handler')
    
    # URI de conexión MySQL
    mysql_uri = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
    
    # Configuración de SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'charset': 'utf8mb4',
            'autocommit': True
        }
    }
    
    db.init_app(app)
    
    return db

def create_tables():
    """Crea todas las tablas en la base de datos"""
    db.create_all()
    print("Tablas creadas exitosamente")

def drop_tables():
    """Elimina todas las tablas de la base de datos"""
    db.drop_all()
    print("Tablas eliminadas exitosamente")

