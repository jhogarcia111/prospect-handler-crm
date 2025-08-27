from src.models.database import db
from datetime import datetime
from sqlalchemy import text, DECIMAL

class Oportunidad(db.Model):
    __tablename__ = 'tblOportunidades'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    
    # Relación con cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('tblClientes.id'), nullable=False)
    
    # Campos de valor y probabilidad
    valor_estimado = db.Column(DECIMAL(15, 2), nullable=True)
    probabilidad = db.Column(db.Integer, nullable=True, default=50)  # Porcentaje 0-100
    prioridad = db.Column(db.String(20), nullable=False, default='medium')  # low, medium, high
    
    # Campos de estado y seguimiento
    estado = db.Column(db.String(50), nullable=False, default='prospecto')  # prospecto, contactado, propuesta, negociacion, cerrado, perdido
    resultado = db.Column(db.String(50), nullable=True)  # ganado, perdido, cancelado
    
    # Campos de fechas
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_estimada_cierre = db.Column(db.Date, nullable=True)
    fecha_cierre_real = db.Column(db.Date, nullable=True)
    
    # Campos de asignación
    empleado_asignado_id = db.Column(db.Integer, db.ForeignKey('tblEmpleados.id'), nullable=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('tblServicios.id'), nullable=True)
    fuente_id = db.Column(db.Integer, db.ForeignKey('tblFuentes.id'), nullable=True)
    
    # Campos adicionales
    notas = db.Column(db.Text, nullable=True)
    motivo_perdida = db.Column(db.Text, nullable=True)
    competidor = db.Column(db.String(255), nullable=True)
    
    # Relaciones
    empleado_asignado = db.relationship('Empleado', backref='oportunidades_asignadas', lazy=True)
    servicio = db.relationship('Servicio', backref='oportunidades', lazy=True)
    fuente = db.relationship('Fuente', backref='oportunidades', lazy=True)
    actividades = db.relationship('ActividadRealizada', backref='oportunidad', lazy=True, cascade='all, delete-orphan')
    seguimientos = db.relationship('SeguimientoOportunidad', backref='oportunidad', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Oportunidad {self.titulo}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre_completo if self.cliente else None,
            'cliente_empresa': self.cliente.empresa if self.cliente else None,
            'valor_estimado': float(self.valor_estimado) if self.valor_estimado else None,
            'probabilidad': self.probabilidad,
            'prioridad': self.prioridad,
            'estado': self.estado,
            'resultado': self.resultado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'fecha_estimada_cierre': self.fecha_estimada_cierre.isoformat() if self.fecha_estimada_cierre else None,
            'fecha_cierre_real': self.fecha_cierre_real.isoformat() if self.fecha_cierre_real else None,
            'empleado_asignado_id': self.empleado_asignado_id,
            'empleado_asignado': self.empleado_asignado.nombre if self.empleado_asignado else None,
            'servicio_id': self.servicio_id,
            'servicio': self.servicio.nombre if self.servicio else None,
            'fuente_id': self.fuente_id,
            'fuente': self.fuente.nombre if self.fuente else None,
            'notas': self.notas,
            'motivo_perdida': self.motivo_perdida,
            'competidor': self.competidor,
            'total_actividades': len(self.actividades) if self.actividades else 0
        }
    
    @classmethod
    def get_by_id(cls, oportunidad_id):
        """Obtiene una oportunidad por ID"""
        return cls.query.get(oportunidad_id)
    
    @classmethod
    def get_all(cls, filtros=None):
        """Obtiene todas las oportunidades con filtros opcionales"""
        query = cls.query
        
        if filtros:
            if filtros.get('estado'):
                query = query.filter(cls.estado == filtros['estado'])
            if filtros.get('prioridad'):
                query = query.filter(cls.prioridad == filtros['prioridad'])
            if filtros.get('empleado_asignado_id'):
                query = query.filter(cls.empleado_asignado_id == filtros['empleado_asignado_id'])
            if filtros.get('cliente_id'):
                query = query.filter(cls.cliente_id == filtros['cliente_id'])
            if filtros.get('busqueda'):
                busqueda = f"%{filtros['busqueda']}%"
                query = query.filter(
                    db.or_(
                        cls.titulo.like(busqueda),
                        cls.descripcion.like(busqueda)
                    )
                )
        
        return query.order_by(cls.fecha_actualizacion.desc()).all()
    
    @classmethod
    def get_by_estado(cls):
        """Obtiene oportunidades agrupadas por estado para el Kanban"""
        estados = ['prospecto', 'contactado', 'propuesta', 'negociacion', 'cerrado']
        resultado = {}
        
        for estado in estados:
            oportunidades = cls.query.filter(cls.estado == estado).order_by(cls.fecha_actualizacion.desc()).all()
            resultado[estado] = [opp.to_dict() for opp in oportunidades]
        
        return resultado
    
    @classmethod
    def get_estadisticas(cls):
        """Obtiene estadísticas de oportunidades"""
        total = cls.query.count()
        abiertas = cls.query.filter(cls.estado.in_(['prospecto', 'contactado', 'propuesta', 'negociacion'])).count()
        cerradas_ganadas = cls.query.filter(cls.estado == 'cerrado', cls.resultado == 'ganado').count()
        cerradas_perdidas = cls.query.filter(cls.estado == 'cerrado', cls.resultado == 'perdido').count()
        
        valor_total = db.session.query(db.func.sum(cls.valor_estimado)).filter(
            cls.estado.in_(['prospecto', 'contactado', 'propuesta', 'negociacion'])
        ).scalar() or 0
        
        valor_cerradas = db.session.query(db.func.sum(cls.valor_estimado)).filter(
            cls.estado == 'cerrado', cls.resultado == 'ganado'
        ).scalar() or 0
        
        return {
            'total': total,
            'abiertas': abiertas,
            'cerradas_ganadas': cerradas_ganadas,
            'cerradas_perdidas': cerradas_perdidas,
            'valor_total_pipeline': float(valor_total),
            'valor_cerradas_ganadas': float(valor_cerradas),
            'tasa_conversion': round((cerradas_ganadas / total * 100) if total > 0 else 0, 2)
        }
    
    def save(self):
        """Guarda la oportunidad en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina la oportunidad de la base de datos"""
        db.session.delete(self)
        db.session.commit()
        return True
    
    def cambiar_estado(self, nuevo_estado, resultado=None):
        """Cambia el estado de la oportunidad"""
        self.estado = nuevo_estado
        if resultado:
            self.resultado = resultado
        if nuevo_estado == 'cerrado':
            self.fecha_cierre_real = datetime.utcnow().date()
        self.save()
        return self

