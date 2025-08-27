from flask import Blueprint, request, jsonify
from src.models import (
    Industria, Fuente, Servicio, Plataforma, Resultado, MedioPago,
    get_catalogo_base, save_catalogo_item, delete_catalogo_item
)

catalogos_bp = Blueprint('catalogos', __name__)

# ==================== INDUSTRIAS ====================

@catalogos_bp.route('/industrias', methods=['GET'])
def get_industrias():
    """Obtiene todas las industrias"""
    try:
        filtros = {}
        if request.args.get('activo') is not None:
            filtros['activo'] = request.args.get('activo').lower() == 'true'
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        industrias = get_catalogo_base(Industria, filtros)
        
        return jsonify({
            'success': True,
            'data': [industria.to_dict() for industria in industrias],
            'total': len(industrias)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener industrias: {str(e)}'
        }), 500

@catalogos_bp.route('/industrias', methods=['POST'])
def create_industria():
    """Crea una nueva industria"""
    try:
        data = request.get_json()
        
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'El nombre es requerido'
            }), 400
        
        industria = Industria(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            activo=data.get('activo', True)
        )
        
        save_catalogo_item(industria)
        
        return jsonify({
            'success': True,
            'message': 'Industria creada exitosamente',
            'data': industria.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear industria: {str(e)}'
        }), 500

@catalogos_bp.route('/industrias/<int:industria_id>', methods=['PUT'])
def update_industria(industria_id):
    """Actualiza una industria"""
    try:
        industria = Industria.query.get(industria_id)
        
        if not industria:
            return jsonify({
                'success': False,
                'message': 'Industria no encontrada'
            }), 404
        
        data = request.get_json()
        
        if 'nombre' in data:
            industria.nombre = data['nombre']
        if 'descripcion' in data:
            industria.descripcion = data['descripcion']
        if 'activo' in data:
            industria.activo = data['activo']
        
        save_catalogo_item(industria)
        
        return jsonify({
            'success': True,
            'message': 'Industria actualizada exitosamente',
            'data': industria.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar industria: {str(e)}'
        }), 500

@catalogos_bp.route('/industrias/<int:industria_id>', methods=['DELETE'])
def delete_industria(industria_id):
    """Elimina una industria"""
    try:
        industria = Industria.query.get(industria_id)
        
        if not industria:
            return jsonify({
                'success': False,
                'message': 'Industria no encontrada'
            }), 404
        
        delete_catalogo_item(industria)
        
        return jsonify({
            'success': True,
            'message': 'Industria eliminada exitosamente'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar industria: {str(e)}'
        }), 500

# ==================== FUENTES ====================

@catalogos_bp.route('/fuentes', methods=['GET'])
def get_fuentes():
    """Obtiene todas las fuentes"""
    try:
        filtros = {}
        if request.args.get('activo') is not None:
            filtros['activo'] = request.args.get('activo').lower() == 'true'
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        fuentes = get_catalogo_base(Fuente, filtros)
        
        return jsonify({
            'success': True,
            'data': [fuente.to_dict() for fuente in fuentes],
            'total': len(fuentes)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener fuentes: {str(e)}'
        }), 500

@catalogos_bp.route('/fuentes', methods=['POST'])
def create_fuente():
    """Crea una nueva fuente"""
    try:
        data = request.get_json()
        
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'El nombre es requerido'
            }), 400
        
        fuente = Fuente(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            tipo=data.get('tipo'),
            activo=data.get('activo', True)
        )
        
        save_catalogo_item(fuente)
        
        return jsonify({
            'success': True,
            'message': 'Fuente creada exitosamente',
            'data': fuente.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear fuente: {str(e)}'
        }), 500

# ==================== SERVICIOS ====================

@catalogos_bp.route('/servicios', methods=['GET'])
def get_servicios():
    """Obtiene todos los servicios"""
    try:
        filtros = {}
        if request.args.get('activo') is not None:
            filtros['activo'] = request.args.get('activo').lower() == 'true'
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        servicios = get_catalogo_base(Servicio, filtros)
        
        return jsonify({
            'success': True,
            'data': [servicio.to_dict() for servicio in servicios],
            'total': len(servicios)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener servicios: {str(e)}'
        }), 500

@catalogos_bp.route('/servicios', methods=['POST'])
def create_servicio():
    """Crea un nuevo servicio"""
    try:
        data = request.get_json()
        
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'El nombre es requerido'
            }), 400
        
        servicio = Servicio(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            categoria=data.get('categoria'),
            precio_base=data.get('precio_base'),
            unidad=data.get('unidad'),
            activo=data.get('activo', True)
        )
        
        save_catalogo_item(servicio)
        
        return jsonify({
            'success': True,
            'message': 'Servicio creado exitosamente',
            'data': servicio.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear servicio: {str(e)}'
        }), 500

# ==================== PLATAFORMAS ====================

@catalogos_bp.route('/plataformas', methods=['GET'])
def get_plataformas():
    """Obtiene todas las plataformas"""
    try:
        filtros = {}
        if request.args.get('activo') is not None:
            filtros['activo'] = request.args.get('activo').lower() == 'true'
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        plataformas = get_catalogo_base(Plataforma, filtros)
        
        return jsonify({
            'success': True,
            'data': [plataforma.to_dict() for plataforma in plataformas],
            'total': len(plataformas)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener plataformas: {str(e)}'
        }), 500

@catalogos_bp.route('/plataformas', methods=['POST'])
def create_plataforma():
    """Crea una nueva plataforma"""
    try:
        data = request.get_json()
        
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'El nombre es requerido'
            }), 400
        
        plataforma = Plataforma(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            url=data.get('url'),
            tipo=data.get('tipo'),
            activo=data.get('activo', True)
        )
        
        save_catalogo_item(plataforma)
        
        return jsonify({
            'success': True,
            'message': 'Plataforma creada exitosamente',
            'data': plataforma.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear plataforma: {str(e)}'
        }), 500

# ==================== RESULTADOS ====================

@catalogos_bp.route('/resultados', methods=['GET'])
def get_resultados():
    """Obtiene todos los resultados"""
    try:
        filtros = {}
        if request.args.get('activo') is not None:
            filtros['activo'] = request.args.get('activo').lower() == 'true'
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        resultados = get_catalogo_base(Resultado, filtros)
        
        return jsonify({
            'success': True,
            'data': [resultado.to_dict() for resultado in resultados],
            'total': len(resultados)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener resultados: {str(e)}'
        }), 500

@catalogos_bp.route('/resultados', methods=['POST'])
def create_resultado():
    """Crea un nuevo resultado"""
    try:
        data = request.get_json()
        
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'El nombre es requerido'
            }), 400
        
        resultado = Resultado(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            categoria=data.get('categoria'),
            activo=data.get('activo', True)
        )
        
        save_catalogo_item(resultado)
        
        return jsonify({
            'success': True,
            'message': 'Resultado creado exitosamente',
            'data': resultado.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear resultado: {str(e)}'
        }), 500

# ==================== MEDIOS DE PAGO ====================

@catalogos_bp.route('/medios-pago', methods=['GET'])
def get_medios_pago():
    """Obtiene todos los medios de pago"""
    try:
        filtros = {}
        if request.args.get('activo') is not None:
            filtros['activo'] = request.args.get('activo').lower() == 'true'
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        medios_pago = get_catalogo_base(MedioPago, filtros)
        
        return jsonify({
            'success': True,
            'data': [medio.to_dict() for medio in medios_pago],
            'total': len(medios_pago)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener medios de pago: {str(e)}'
        }), 500

@catalogos_bp.route('/medios-pago', methods=['POST'])
def create_medio_pago():
    """Crea un nuevo medio de pago"""
    try:
        data = request.get_json()
        
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'El nombre es requerido'
            }), 400
        
        medio_pago = MedioPago(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            tipo=data.get('tipo'),
            comision_porcentaje=data.get('comision_porcentaje'),
            activo=data.get('activo', True)
        )
        
        save_catalogo_item(medio_pago)
        
        return jsonify({
            'success': True,
            'message': 'Medio de pago creado exitosamente',
            'data': medio_pago.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear medio de pago: {str(e)}'
        }), 500

# ==================== ENDPOINTS GENÉRICOS ====================

@catalogos_bp.route('/catalogos/resumen', methods=['GET'])
def get_resumen_catalogos():
    """Obtiene un resumen de todos los catálogos"""
    try:
        resumen = {
            'industrias': Industria.query.filter(Industria.activo == True).count(),
            'fuentes': Fuente.query.filter(Fuente.activo == True).count(),
            'servicios': Servicio.query.filter(Servicio.activo == True).count(),
            'plataformas': Plataforma.query.filter(Plataforma.activo == True).count(),
            'resultados': Resultado.query.filter(Resultado.activo == True).count(),
            'medios_pago': MedioPago.query.filter(MedioPago.activo == True).count()
        }
        
        return jsonify({
            'success': True,
            'data': resumen
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener resumen: {str(e)}'
        }), 500

