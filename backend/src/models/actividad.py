from src.models.database import db
from datetime import datetime

class ActividadProspeccion(db.Model):
    """Tabla de catálogo de tipos de actividades de prospección"""
    __tablename__ = 'tblActividadesProspección'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f'<ActividadProspeccion {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo
        }

class ActividadRealizada(db.Model):
    """Tabla de actividades realizadas con clientes/oportunidades"""
    __tablename__ = 'tblActividadesRealizadas'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(100), nullable=False)  # llamada, email, reunion, etc.
    descripcion = db.Column(db.Text, nullable=False)
    
    # Campos de fecha y hora
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relaciones
    cliente_id = db.Column(db.Integer, db.ForeignKey('tblClientes.id'), nullable=True)
    oportunidad_id = db.Column(db.Integer, db.ForeignKey('tblOportunidades.id'), nullable=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('tblEmpleados.id'), nullable=True)
    
    # Campos de resultado
    resultado = db.Column(db.String(100), nullable=False)  # exitoso, pendiente, no_contacto, etc.
    proxima_accion = db.Column(db.Text, nullable=True)
    fecha_proxima_accion = db.Column(db.Date, nullable=True)
    
    # Campos adicionales
    notas = db.Column(db.Text, nullable=True)
    duracion_minutos = db.Column(db.Integer, nullable=True)
    
    # Relaciones
    empleado = db.relationship('Empleado', backref='actividades_realizadas', lazy=True)
    
    def __repr__(self):
        return f'<ActividadRealizada {self.tipo} - {self.fecha}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'hora': self.hora.strftime('%H:%M') if self.hora else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre_completo if self.cliente else None,
            'oportunidad_id': self.oportunidad_id,
            'oportunidad_titulo': self.oportunidad.titulo if self.oportunidad else None,
            'empleado_id': self.empleado_id,
            'empleado_nombre': self.empleado.nombre if self.empleado else None,
            'resultado': self.resultado,
            'proxima_accion': self.proxima_accion,
            'fecha_proxima_accion': self.fecha_proxima_accion.isoformat() if self.fecha_proxima_accion else None,
            'notas': self.notas,
            'duracion_minutos': self.duracion_minutos
        }
    
    @classmethod
    def get_by_cliente(cls, cliente_id):
        """Obtiene actividades por cliente"""
        return cls.query.filter(cls.cliente_id == cliente_id).order_by(cls.fecha.desc(), cls.hora.desc()).all()
    
    @classmethod
    def get_by_oportunidad(cls, oportunidad_id):
        """Obtiene actividades por oportunidad"""
        return cls.query.filter(cls.oportunidad_id == oportunidad_id).order_by(cls.fecha.desc(), cls.hora.desc()).all()
    
    @classmethod
    def get_by_empleado(cls, empleado_id, fecha_desde=None, fecha_hasta=None):
        """Obtiene actividades por empleado con filtros de fecha"""
        query = cls.query.filter(cls.empleado_id == empleado_id)
        
        if fecha_desde:
            query = query.filter(cls.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(cls.fecha <= fecha_hasta)
        
        return query.order_by(cls.fecha.desc(), cls.hora.desc()).all()
    
    @classmethod
    def get_proximas_acciones(cls, empleado_id=None, fecha_limite=None):
        """Obtiene próximas acciones pendientes"""
        query = cls.query.filter(cls.proxima_accion.isnot(None), cls.fecha_proxima_accion.isnot(None))
        
        if empleado_id:
            query = query.filter(cls.empleado_id == empleado_id)
        if fecha_limite:
            query = query.filter(cls.fecha_proxima_accion <= fecha_limite)
        
        return query.order_by(cls.fecha_proxima_accion.asc()).all()
    
    def save(self):
        """Guarda la actividad en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina la actividad de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True

class ListadoActividades(db.Model):
    """Tabla de catálogo de actividades disponibles"""
    __tablename__ = 'tblListadoActividades'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f'<ListadoActividades {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'activo': self.activo
        }

