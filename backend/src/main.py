import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models import init_database, create_tables, drop_tables
from src.routes.clientes import clientes_bp
from src.routes.oportunidades import oportunidades_bp
from src.routes.actividades import actividades_bp
from src.routes.empleados import empleados_bp
from src.routes.catalogos import catalogos_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
CORS(app) # Habilitar CORS para todas las rutas

# Inicializar la base de datos
init_database(app)

# Crear tablas si no existen
with app.app_context():
    create_tables()

# Registrar Blueprints
app.register_blueprint(clientes_bp, url_prefix='/api')
app.register_blueprint(oportunidades_bp, url_prefix='/api')
app.register_blueprint(actividades_bp, url_prefix='/api')
app.register_blueprint(empleados_bp, url_prefix='/api')
app.register_blueprint(catalogos_bp, url_prefix='/api')

@app.route('/')
def index():
    return "Bienvenido al backend de Prospect Handler!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


