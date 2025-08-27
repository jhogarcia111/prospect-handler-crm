from flask import Blueprint, request, jsonify
from src.models import ActividadRealizada, Cliente, Oportunidad, Empleado, db
from datetime import datetime, date

actividades_bp = Blueprint('actividades', __name__)

@actividades_bp.route('/actividades', methods=['GET'])
def get_actividades():
    """Obtiene todas las actividades con filtros opcionales"""
    try:
        # Obtener parámetros de consulta
        cliente_id = request.args.get('cliente_id', type=int)
        oportunidad_id = request.args.get('oportunidad_id', type=int)
        empleado_id = request.args.get('empleado_id', type=int)
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        
        query = ActividadRealizada.query
        
        # Aplicar filtros
        if cliente_id:
            query = query.filter(ActividadRealizada.cliente_id == cliente_id)
        if oportunidad_id:
            query = query.filter(ActividadRealizada.oportunidad_id == oportunidad_id)
        if empleado_id:
            query = query.filter(ActividadRealizada.empleado_id == empleado_id)
        
        # Filtros de fecha
        if fecha_desde:
            try:
                fecha_desde_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                query = query.filter(ActividadRealizada.fecha >= fecha_desde_obj)
            except ValueError:
                pass
        
        if fecha_hasta:
            try:
                fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                query = query.filter(ActividadRealizada.fecha <= fecha_hasta_obj)
            except ValueError:
                pass
        
        actividades = query.order_by(
            ActividadRealizada.fecha.desc(),
            ActividadRealizada.hora.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'data': [actividad.to_dict() for actividad in actividades],
            'total': len(actividades)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener actividades: {str(e)}'
        }), 500

@actividades_bp.route('/actividades/<int:actividad_id>', methods=['GET'])
def get_actividad(actividad_id):
    """Obtiene una actividad específica por ID"""
    try:
        actividad = ActividadRealizada.query.get(actividad_id)
        
        if not actividad:
            return jsonify({
                'success': False,
                'message': 'Actividad no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': actividad.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener actividad: {str(e)}'
        }), 500

@actividades_bp.route('/actividades', methods=['POST'])
def create_actividad():
    """Crea una nueva actividad"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('tipo'):
            return jsonify({
                'success': False,
                'message': 'El tipo de actividad es requerido'
            }), 400
        
        if not data.get('descripcion'):
            return jsonify({
                'success': False,
                'message': 'La descripción es requerida'
            }), 400
        
        if not data.get('fecha'):
            return jsonify({
                'success': False,
                'message': 'La fecha es requerida'
            }), 400
        
        if not data.get('resultado'):
            return jsonify({
                'success': False,
                'message': 'El resultado es requerido'
            }), 400
        
        # Validar que al menos cliente_id o oportunidad_id esté presente
        if not data.get('cliente_id') and not data.get('oportunidad_id'):
            return jsonify({
                'success': False,
                'message': 'Se requiere cliente_id o oportunidad_id'
            }), 400
        
        # Crear nueva actividad
        actividad = ActividadRealizada(
            tipo=data['tipo'],
            descripcion=data['descripcion'],
            resultado=data['resultado'],
            cliente_id=data.get('cliente_id'),
            oportunidad_id=data.get('oportunidad_id'),
            empleado_id=data.get('empleado_id'),
            proxima_accion=data.get('proxima_accion'),
            notas=data.get('notas'),
            duracion_minutos=data.get('duracion_minutos')
        )
        
        # Convertir fecha
        try:
            actividad.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Formato de fecha inválido. Use YYYY-MM-DD'
            }), 400
        
        # Convertir hora si se proporciona
        if data.get('hora'):
            try:
                actividad.hora = datetime.strptime(data['hora'], '%H:%M').time()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Formato de hora inválido. Use HH:MM'
                }), 400
        
        # Convertir fecha de próxima acción si se proporciona
        if data.get('fecha_proxima_accion'):
            try:
                actividad.fecha_proxima_accion = datetime.strptime(
                    data['fecha_proxima_accion'], '%Y-%m-%d'
                ).date()
            except ValueError:
                pass
        
        actividad.save()
        
        # Actualizar fecha de último contacto del cliente si aplica
        if actividad.cliente_id:
            cliente = Cliente.get_by_id(actividad.cliente_id)
            if cliente:
                cliente.fecha_ultimo_contacto = datetime.combine(actividad.fecha, actividad.hora or datetime.min.time())
                cliente.save()
        
        return jsonify({
            'success': True,
            'message': 'Actividad creada exitosamente',
            'data': actividad.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear actividad: {str(e)}'
        }), 500

@actividades_bp.route('/actividades/<int:actividad_id>', methods=['PUT'])
def update_actividad(actividad_id):
    """Actualiza una actividad existente"""
    try:
        actividad = ActividadRealizada.query.get(actividad_id)
        
        if not actividad:
            return jsonify({
                'success': False,
                'message': 'Actividad no encontrada'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'tipo' in data:
            actividad.tipo = data['tipo']
        if 'descripcion' in data:
            actividad.descripcion = data['descripcion']
        if 'resultado' in data:
            actividad.resultado = data['resultado']
        if 'proxima_accion' in data:
            actividad.proxima_accion = data['proxima_accion']
        if 'notas' in data:
            actividad.notas = data['notas']
        if 'duracion_minutos' in data:
            actividad.duracion_minutos = data['duracion_minutos']
        
        # Actualizar fecha
        if 'fecha' in data:
            try:
                actividad.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Formato de fecha inválido. Use YYYY-MM-DD'
                }), 400
        
        # Actualizar hora
        if 'hora' in data:
            if data['hora']:
                try:
                    actividad.hora = datetime.strptime(data['hora'], '%H:%M').time()
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Formato de hora inválido. Use HH:MM'
                    }), 400
            else:
                actividad.hora = None
        
        # Actualizar fecha de próxima acción
        if 'fecha_proxima_accion' in data:
            if data['fecha_proxima_accion']:
                try:
                    actividad.fecha_proxima_accion = datetime.strptime(
                        data['fecha_proxima_accion'], '%Y-%m-%d'
                    ).date()
                except ValueError:
                    pass
            else:
                actividad.fecha_proxima_accion = None
        
        actividad.save()
        
        return jsonify({
            'success': True,
            'message': 'Actividad actualizada exitosamente',
            'data': actividad.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar actividad: {str(e)}'
        }), 500

@actividades_bp.route('/actividades/<int:actividad_id>', methods=['DELETE'])
def delete_actividad(actividad_id):
    """Elimina una actividad"""
    try:
        actividad = ActividadRealizada.query.get(actividad_id)
        
        if not actividad:
            return jsonify({
                'success': False,
                'message': 'Actividad no encontrada'
            }), 404
        
        actividad.delete()
        
        return jsonify({
            'success': True,
            'message': 'Actividad eliminada exitosamente'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar actividad: {str(e)}'
        }), 500

@actividades_bp.route('/actividades/proximas-acciones', methods=['GET'])
def get_proximas_acciones():
    """Obtiene próximas acciones pendientes"""
    try:
        empleado_id = request.args.get('empleado_id', type=int)
        fecha_limite = request.args.get('fecha_limite')
        
        fecha_limite_obj = None
        if fecha_limite:
            try:
                fecha_limite_obj = datetime.strptime(fecha_limite, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        actividades = ActividadRealizada.get_proximas_acciones(empleado_id, fecha_limite_obj)
        
        return jsonify({
            'success': True,
            'data': [actividad.to_dict() for actividad in actividades],
            'total': len(actividades)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener próximas acciones: {str(e)}'
        }), 500

@actividades_bp.route('/actividades/recientes', methods=['GET'])
def get_actividades_recientes():
    """Obtiene las actividades más recientes"""
    try:
        limite = request.args.get('limite', 10, type=int)
        empleado_id = request.args.get('empleado_id', type=int)
        
        query = ActividadRealizada.query
        
        if empleado_id:
            query = query.filter(ActividadRealizada.empleado_id == empleado_id)
        
        actividades = query.order_by(
            ActividadRealizada.fecha.desc(),
            ActividadRealizada.hora.desc()
        ).limit(limite).all()
        
        return jsonify({
            'success': True,
            'data': [actividad.to_dict() for actividad in actividades],
            'total': len(actividades)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener actividades recientes: {str(e)}'
        }), 500

