from src.models.database import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Industria(db.Model):
    """Tabla de catálogo de industrias"""
    __tablename__ = 'tblIndustrias'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Industria {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'total_clientes': len(self.clientes) if hasattr(self, 'clientes') else 0
        }

class Fuente(db.Model):
    """Tabla de catálogo de fuentes de leads"""
    __tablename__ = 'tblFuentes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(100), nullable=True)  # digital, referido, evento, etc.
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Fuente {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'total_clientes': len(self.clientes) if hasattr(self, 'clientes') else 0,
            'total_oportunidades': len(self.oportunidades) if hasattr(self, 'oportunidades') else 0
        }

class Servicio(db.Model):
    """Tabla de catálogo de servicios"""
    __tablename__ = 'tblServicios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    precio_base = db.Column(DECIMAL(15, 2), nullable=True)
    unidad = db.Column(db.String(50), nullable=True)  # hora, proyecto, mes, etc.
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Servicio {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'precio_base': float(self.precio_base) if self.precio_base else None,
            'unidad': self.unidad,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'total_oportunidades': len(self.oportunidades) if hasattr(self, 'oportunidades') else 0
        }

class Plataforma(db.Model):
    """Tabla de catálogo de plataformas"""
    __tablename__ = 'tblPlataformas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    tipo = db.Column(db.String(100), nullable=True)  # social, web, app, etc.
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Plataforma {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'url': self.url,
            'tipo': self.tipo,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Resultado(db.Model):
    """Tabla de catálogo de resultados de actividades"""
    __tablename__ = 'tblResultados'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(100), nullable=True)  # positivo, negativo, neutro
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resultado {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class MedioPago(db.Model):
    """Tabla de catálogo de medios de pago"""
    __tablename__ = 'tblMediosDePago'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(100), nullable=True)  # efectivo, transferencia, tarjeta, etc.
    comision_porcentaje = db.Column(DECIMAL(5, 2), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MedioPago {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'comision_porcentaje': float(self.comision_porcentaje) if self.comision_porcentaje else None,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

# Funciones de utilidad para los catálogos
def get_catalogo_base(modelo_clase, filtros=None):
    """Función genérica para obtener datos de catálogos"""
    query = modelo_clase.query
    
    if filtros:
        if filtros.get('activo') is not None:
            query = query.filter(modelo_clase.activo == filtros['activo'])
        if filtros.get('busqueda'):
            busqueda = f"%{filtros['busqueda']}%"
            query = query.filter(modelo_clase.nombre.like(busqueda))
    
    return query.order_by(modelo_clase.nombre.asc()).all()

def save_catalogo_item(item):
    """Función genérica para guardar elementos de catálogo"""
    db.session.add(item)
    db.session.commit()
    return item

def delete_catalogo_item(item):
    """Función genérica para eliminar elementos de catálogo"""
    db.session.delete(item)
    db.session.commit()
    return True

