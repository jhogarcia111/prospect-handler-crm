from src.models.database import db
from datetime import datetime
from sqlalchemy import DECIMAL

class PagoRecibido(db.Model):
    """Tabla de pagos recibidos"""
    __tablename__ = 'tblPagosRecibidos'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_factura = db.Column(db.String(100), nullable=True)
    numero_recibo = db.Column(db.String(100), nullable=True)
    
    # Relaciones
    cliente_id = db.Column(db.Integer, db.ForeignKey('tblClientes.id'), nullable=False)
    oportunidad_id = db.Column(db.Integer, db.ForeignKey('tblOportunidades.id'), nullable=True)
    medio_pago_id = db.Column(db.Integer, db.ForeignKey('tblMediosDePago.id'), nullable=True)
    
    # Campos de montos
    monto_bruto = db.Column(DECIMAL(15, 2), nullable=False)
    descuento = db.Column(DECIMAL(15, 2), nullable=True, default=0)
    impuestos = db.Column(DECIMAL(15, 2), nullable=True, default=0)
    comision = db.Column(DECIMAL(15, 2), nullable=True, default=0)
    monto_neto = db.Column(DECIMAL(15, 2), nullable=False)
    
    # Campos de fechas
    fecha_pago = db.Column(db.Date, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Campos de estado
    estado = db.Column(db.String(50), nullable=False, default='pendiente')  # pendiente, pagado, vencido, cancelado
    moneda = db.Column(db.String(10), nullable=False, default='USD')
    
    # Campos adicionales
    concepto = db.Column(db.Text, nullable=True)
    notas = db.Column(db.Text, nullable=True)
    referencia_pago = db.Column(db.String(255), nullable=True)
    
    # Relaciones
    cliente = db.relationship('Cliente', backref='pagos_recibidos', lazy=True)
    oportunidad = db.relationship('Oportunidad', backref='pagos_recibidos', lazy=True)
    medio_pago = db.relationship('MedioPago', backref='pagos_recibidos', lazy=True)
    
    def __repr__(self):
        return f'<PagoRecibido {self.numero_factura} - {self.monto_neto}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_factura': self.numero_factura,
            'numero_recibo': self.numero_recibo,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre_completo if self.cliente else None,
            'cliente_empresa': self.cliente.empresa if self.cliente else None,
            'oportunidad_id': self.oportunidad_id,
            'oportunidad_titulo': self.oportunidad.titulo if self.oportunidad else None,
            'medio_pago_id': self.medio_pago_id,
            'medio_pago': self.medio_pago.nombre if self.medio_pago else None,
            'monto_bruto': float(self.monto_bruto),
            'descuento': float(self.descuento) if self.descuento else 0,
            'impuestos': float(self.impuestos) if self.impuestos else 0,
            'comision': float(self.comision) if self.comision else 0,
            'monto_neto': float(self.monto_neto),
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'estado': self.estado,
            'moneda': self.moneda,
            'concepto': self.concepto,
            'notas': self.notas,
            'referencia_pago': self.referencia_pago
        }
    
    @classmethod
    def get_estadisticas_financieras(cls, fecha_desde=None, fecha_hasta=None):
        """Obtiene estadísticas financieras"""
        query = cls.query
        
        if fecha_desde:
            query = query.filter(cls.fecha_pago >= fecha_desde)
        if fecha_hasta:
            query = query.filter(cls.fecha_pago <= fecha_hasta)
        
        # Totales por estado
        total_pagado = query.filter(cls.estado == 'pagado').with_entities(
            db.func.sum(cls.monto_neto)
        ).scalar() or 0
        
        total_pendiente = query.filter(cls.estado == 'pendiente').with_entities(
            db.func.sum(cls.monto_neto)
        ).scalar() or 0
        
        total_vencido = query.filter(cls.estado == 'vencido').with_entities(
            db.func.sum(cls.monto_neto)
        ).scalar() or 0
        
        # Conteos
        count_pagado = query.filter(cls.estado == 'pagado').count()
        count_pendiente = query.filter(cls.estado == 'pendiente').count()
        count_vencido = query.filter(cls.estado == 'vencido').count()
        
        # Ingresos por mes (últimos 12 meses)
        ingresos_mensuales = db.session.query(
            db.func.date_format(cls.fecha_pago, '%Y-%m').label('mes'),
            db.func.sum(cls.monto_neto).label('total')
        ).filter(
            cls.estado == 'pagado',
            cls.fecha_pago >= datetime.now().replace(day=1, month=1) if not fecha_desde else cls.fecha_pago >= fecha_desde
        ).group_by(
            db.func.date_format(cls.fecha_pago, '%Y-%m')
        ).order_by('mes').all()
        
        return {
            'total_pagado': float(total_pagado),
            'total_pendiente': float(total_pendiente),
            'total_vencido': float(total_vencido),
            'count_pagado': count_pagado,
            'count_pendiente': count_pendiente,
            'count_vencido': count_vencido,
            'ingresos_mensuales': [
                {'mes': mes, 'total': float(total)} 
                for mes, total in ingresos_mensuales
            ]
        }
    
    def save(self):
        """Guarda el pago en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self

class Control(db.Model):
    """Tabla de control para configuraciones del sistema"""
    __tablename__ = 'tblControl'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clave = db.Column(db.String(255), nullable=False, unique=True)
    valor = db.Column(db.Text, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(50), nullable=False, default='texto')  # texto, numero, booleano, fecha
    categoria = db.Column(db.String(100), nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Control {self.clave}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'clave': self.clave,
            'valor': self.valor,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    @classmethod
    def get_valor(cls, clave, valor_defecto=None):
        """Obtiene un valor de configuración"""
        control = cls.query.filter(cls.clave == clave).first()
        return control.valor if control else valor_defecto
    
    @classmethod
    def set_valor(cls, clave, valor, descripcion=None, tipo='texto', categoria=None):
        """Establece un valor de configuración"""
        control = cls.query.filter(cls.clave == clave).first()
        
        if control:
            control.valor = valor
            control.fecha_actualizacion = datetime.utcnow()
        else:
            control = cls(
                clave=clave,
                valor=valor,
                descripcion=descripcion,
                tipo=tipo,
                categoria=categoria
            )
        
        db.session.add(control)
        db.session.commit()
        return control

class SeguimientoOportunidad(db.Model):
    """Tabla de seguimiento de cambios en oportunidades"""
    __tablename__ = 'tblSeguimientosOportunidades'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oportunidad_id = db.Column(db.Integer, db.ForeignKey('tblOportunidades.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('tblEmpleados.id'), nullable=True)
    
    # Campos de cambio
    campo_modificado = db.Column(db.String(100), nullable=False)
    valor_anterior = db.Column(db.Text, nullable=True)
    valor_nuevo = db.Column(db.Text, nullable=True)
    
    # Campos de fecha
    fecha_cambio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Campos adicionales
    notas = db.Column(db.Text, nullable=True)
    
    # Relaciones
    empleado = db.relationship('Empleado', backref='seguimientos_realizados', lazy=True)
    
    def __repr__(self):
        return f'<SeguimientoOportunidad {self.oportunidad_id} - {self.campo_modificado}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'oportunidad_id': self.oportunidad_id,
            'empleado_id': self.empleado_id,
            'empleado_nombre': self.empleado.nombre_completo if self.empleado else None,
            'campo_modificado': self.campo_modificado,
            'valor_anterior': self.valor_anterior,
            'valor_nuevo': self.valor_nuevo,
            'fecha_cambio': self.fecha_cambio.isoformat() if self.fecha_cambio else None,
            'notas': self.notas
        }

