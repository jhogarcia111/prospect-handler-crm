from src.models.database import db
from datetime import datetime
from sqlalchemy import text, DECIMAL

class Cliente(db.Model):
    __tablename__ = 'tblClientes'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    empresa = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    telefono_movil = db.Column(db.String(50), nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    ciudad = db.Column(db.String(100), nullable=True)
    estado_provincia = db.Column(db.String(100), nullable=True)
    codigo_postal = db.Column(db.String(20), nullable=True)
    pais = db.Column(db.String(100), nullable=True, default='Colombia')
    
    # Campos de clasificación
    industria_id = db.Column(db.Integer, db.ForeignKey('tblIndustrias.id'), nullable=True)
    fuente_id = db.Column(db.Integer, db.ForeignKey('tblFuentes.id'), nullable=True)
    estado = db.Column(db.String(50), nullable=False, default='prospecto')  # prospecto, activo, inactivo
    
    # Campos de seguimiento
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_ultimo_contacto = db.Column(db.DateTime, nullable=True)
    empleado_asignado_id = db.Column(db.Integer, db.ForeignKey('tblEmpleados.id'), nullable=True)
    
    # Campos adicionales
    sitio_web = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    notas = db.Column(db.Text, nullable=True)
    valor_estimado = db.Column(DECIMAL(15, 2), nullable=True)
    
    # Relaciones
    industria = db.relationship('Industria', backref='clientes', lazy=True)
    fuente = db.relationship('Fuente', backref='clientes', lazy=True)
    empleado_asignado = db.relationship('Empleado', backref='clientes_asignados', lazy=True)
    oportunidades = db.relationship('Oportunidad', backref='cliente', lazy=True, cascade='all, delete-orphan')
    actividades = db.relationship('ActividadRealizada', backref='cliente', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cliente {self.nombre_completo}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'empresa': self.empresa,
            'email': self.email,
            'telefono': self.telefono,
            'telefono_movil': self.telefono_movil,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'estado_provincia': self.estado_provincia,
            'codigo_postal': self.codigo_postal,
            'pais': self.pais,
            'industria_id': self.industria_id,
            'industria': self.industria.nombre if self.industria else None,
            'fuente_id': self.fuente_id,
            'fuente': self.fuente.nombre if self.fuente else None,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'fecha_ultimo_contacto': self.fecha_ultimo_contacto.isoformat() if self.fecha_ultimo_contacto else None,
            'empleado_asignado_id': self.empleado_asignado_id,
            'empleado_asignado': self.empleado_asignado.nombre if self.empleado_asignado else None,
            'sitio_web': self.sitio_web,
            'linkedin': self.linkedin,
            'notas': self.notas,
            'valor_estimado': float(self.valor_estimado) if self.valor_estimado else None,
            'total_oportunidades': len(self.oportunidades) if self.oportunidades else 0
        }
    
    @classmethod
    def get_by_id(cls, cliente_id):
        """Obtiene un cliente por ID"""
        return cls.query.get(cliente_id)
    
    @classmethod
    def get_all(cls, filtros=None):
        """Obtiene todos los clientes con filtros opcionales"""
        query = cls.query
        
        if filtros:
            if filtros.get('estado'):
                query = query.filter(cls.estado == filtros['estado'])
            if filtros.get('industria_id'):
                query = query.filter(cls.industria_id == filtros['industria_id'])
            if filtros.get('empleado_asignado_id'):
                query = query.filter(cls.empleado_asignado_id == filtros['empleado_asignado_id'])
            if filtros.get('busqueda'):
                busqueda = f"%{filtros['busqueda']}%"
                query = query.filter(
                    db.or_(
                        cls.nombre_completo.like(busqueda),
                        cls.empresa.like(busqueda),
                        cls.email.like(busqueda)
                    )
                )
        
        return query.order_by(cls.fecha_actualizacion.desc()).all()
    
    def save(self):
        """Guarda el cliente en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina el cliente de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True

