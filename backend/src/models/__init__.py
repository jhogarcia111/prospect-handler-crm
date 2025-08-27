from src.models.database import db, init_database, create_tables, drop_tables
from src.models.cliente import Cliente
from src.models.oportunidad import Oportunidad
from src.models.empleado import Empleado
from src.models.actividad import ActividadProspeccion, ActividadRealizada, ListadoActividades
from src.models.catalogo import Industria, Fuente, Servicio, Plataforma, Resultado, MedioPago
from src.models.finanzas import PagoRecibido, Control, SeguimientoOportunidad

# Lista de todos los modelos para facilitar las operaciones
ALL_MODELS = [
    Cliente,
    Oportunidad,
    Empleado,
    ActividadProspeccion,
    ActividadRealizada,
    ListadoActividades,
    Industria,
    Fuente,
    Servicio,
    Plataforma,
    Resultado,
    MedioPago,
    PagoRecibido,
    Control,
    SeguimientoOportunidad
]

__all__ = [
    'db',
    'init_database',
    'create_tables',
    'drop_tables',
    'Cliente',
    'Oportunidad',
    'Empleado',
    'ActividadProspeccion',
    'ActividadRealizada',
    'ListadoActividades',
    'Industria',
    'Fuente',
    'Servicio',
    'Plataforma',
    'Resultado',
    'MedioPago',
    'PagoRecibido',
    'Control',
    'SeguimientoOportunidad',
    'ALL_MODELS'
]

