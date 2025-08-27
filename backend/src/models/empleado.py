from src.models.database import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Empleado(db.Model):
    __tablename__ = 'tblEmpleados'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    telefono = db.Column(db.String(50), nullable=True)
    
    # Campos de trabajo
    posicion = db.Column(db.String(255), nullable=True)
    departamento = db.Column(db.String(100), nullable=True)
    fecha_ingreso = db.Column(db.Date, nullable=True)
    salario = db.Column(DECIMAL(15, 2), nullable=True)
    
    # Campos de estado
    estado = db.Column(db.String(50), nullable=False, default='activo')  # activo, inactivo, suspendido
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos adicionales
    supervisor_id = db.Column(db.Integer, db.ForeignKey('tblEmpleados.id'), nullable=True)
    notas = db.Column(db.Text, nullable=True)
    
    # Relaciones
    supervisor = db.relationship('Empleado', remote_side=[id], backref='subordinados', lazy=True)
    
    def __repr__(self):
        return f'<Empleado {self.nombre} {self.apellido}>'
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del empleado"""
        if self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'telefono': self.telefono,
            'posicion': self.posicion,
            'departamento': self.departamento,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'salario': float(self.salario) if self.salario else None,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'supervisor_id': self.supervisor_id,
            'supervisor_nombre': self.supervisor.nombre_completo if self.supervisor else None,
            'notas': self.notas,
            'total_clientes': len(self.clientes_asignados) if hasattr(self, 'clientes_asignados') else 0,
            'total_oportunidades': len(self.oportunidades_asignadas) if hasattr(self, 'oportunidades_asignadas') else 0
        }
    
    @classmethod
    def get_by_id(cls, empleado_id):
        """Obtiene un empleado por ID"""
        return cls.query.get(empleado_id)
    
    @classmethod
    def get_all(cls, filtros=None):
        """Obtiene todos los empleados con filtros opcionales"""
        query = cls.query
        
        if filtros:
            if filtros.get('estado'):
                query = query.filter(cls.estado == filtros['estado'])
            if filtros.get('departamento'):
                query = query.filter(cls.departamento == filtros['departamento'])
            if filtros.get('busqueda'):
                busqueda = f"%{filtros['busqueda']}%"
                query = query.filter(
                    db.or_(
                        cls.nombre.like(busqueda),
                        cls.apellido.like(busqueda),
                        cls.email.like(busqueda),
                        cls.posicion.like(busqueda)
                    )
                )
        
        return query.order_by(cls.nombre.asc()).all()
    
    @classmethod
    def get_activos(cls):
        """Obtiene solo empleados activos"""
        return cls.query.filter(cls.estado == 'activo').order_by(cls.nombre.asc()).all()
    
    @classmethod
    def get_estadisticas(cls):
        """Obtiene estadísticas de empleados"""
        total = cls.query.count()
        activos = cls.query.filter(cls.estado == 'activo').count()
        inactivos = cls.query.filter(cls.estado == 'inactivo').count()
        
        departamentos = db.session.query(cls.departamento, db.func.count(cls.id)).filter(
            cls.departamento.isnot(None)
        ).group_by(cls.departamento).all()
        
        return {
            'total': total,
            'activos': activos,
            'inactivos': inactivos,
            'departamentos': dict(departamentos) if departamentos else {}
        }
    
    def save(self):
        """Guarda el empleado en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina el empleado de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True

