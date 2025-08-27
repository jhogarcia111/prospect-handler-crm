from flask import Blueprint, request, jsonify
from src.models import Oportunidad, Cliente, Empleado, Servicio, Fuente, db
from datetime import datetime, date

oportunidades_bp = Blueprint('oportunidades', __name__)

@oportunidades_bp.route('/oportunidades', methods=['GET'])
def get_oportunidades():
    """Obtiene todas las oportunidades con filtros opcionales"""
    try:
        filtros = {}
        
        # Obtener parámetros de consulta
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('prioridad'):
            filtros['prioridad'] = request.args.get('prioridad')
        if request.args.get('empleado_asignado_id'):
            filtros['empleado_asignado_id'] = int(request.args.get('empleado_asignado_id'))
        if request.args.get('cliente_id'):
            filtros['cliente_id'] = int(request.args.get('cliente_id'))
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        oportunidades = Oportunidad.get_all(filtros)
        
        return jsonify({
            'success': True,
            'data': [oportunidad.to_dict() for oportunidad in oportunidades],
            'total': len(oportunidades)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener oportunidades: {str(e)}'
        }), 500

@oportunidades_bp.route('/oportunidades/kanban', methods=['GET'])
def get_oportunidades_kanban():
    """Obtiene oportunidades agrupadas por estado para el tablero Kanban"""
    try:
        oportunidades_por_estado = Oportunidad.get_by_estado()
        
        return jsonify({
            'success': True,
            'data': oportunidades_por_estado
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener oportunidades para Kanban: {str(e)}'
        }), 500

@oportunidades_bp.route('/oportunidades/<int:oportunidad_id>', methods=['GET'])
def get_oportunidad(oportunidad_id):
    """Obtiene una oportunidad específica por ID"""
    try:
        oportunidad = Oportunidad.get_by_id(oportunidad_id)
        
        if not oportunidad:
            return jsonify({
                'success': False,
                'message': 'Oportunidad no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': oportunidad.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener oportunidad: {str(e)}'
        }), 500

@oportunidades_bp.route('/oportunidades', methods=['POST'])
def create_oportunidad():
    """Crea una nueva oportunidad"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('titulo'):
            return jsonify({
                'success': False,
                'message': 'El título es requerido'
            }), 400
        
        if not data.get('cliente_id'):
            return jsonify({
                'success': False,
                'message': 'El cliente es requerido'
            }), 400
        
        # Validar que el cliente existe
        cliente = Cliente.get_by_id(data['cliente_id'])
        if not cliente:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 400
        
        # Crear nueva oportunidad
        oportunidad = Oportunidad(
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            cliente_id=data['cliente_id'],
            valor_estimado=data.get('valor_estimado'),
            probabilidad=data.get('probabilidad', 50),
            prioridad=data.get('prioridad', 'medium'),
            estado=data.get('estado', 'prospecto'),
            empleado_asignado_id=data.get('empleado_asignado_id'),
            servicio_id=data.get('servicio_id'),
            fuente_id=data.get('fuente_id'),
            notas=data.get('notas')
        )
        
        # Convertir fecha estimada de cierre si se proporciona
        if data.get('fecha_estimada_cierre'):
            try:
                oportunidad.fecha_estimada_cierre = datetime.strptime(
                    data['fecha_estimada_cierre'], '%Y-%m-%d'
                ).date()
            except ValueError:
                pass
        
        oportunidad.save()
        
        return jsonify({
            'success': True,
            'message': 'Oportunidad creada exitosamente',
            'data': oportunidad.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear oportunidad: {str(e)}'
        }), 500

@oportunidades_bp.route('/oportunidades/<int:oportunidad_id>', methods=['PUT'])
def update_oportunidad(oportunidad_id):
    """Actualiza una oportunidad existente"""
    try:
        oportunidad = Oportunidad.get_by_id(oportunidad_id)
        
        if not oportunidad:
            return jsonify({
                'success': False,
                'message': 'Oportunidad no encontrada'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'titulo' in data:
            oportunidad.titulo = data['titulo']
        if 'descripcion' in data:
            oportunidad.descripcion = data['descripcion']
        if 'valor_estimado' in data:
            oportunidad.valor_estimado = data['valor_estimado']
        if 'probabilidad' in data:
            oportunidad.probabilidad = data['probabilidad']
        if 'prioridad' in data:
            oportunidad.prioridad = data['prioridad']
        if 'estado' in data:
            oportunidad.estado = data['estado']
        if 'resultado' in data:
            oportunidad.resultado = data['resultado']
        if 'empleado_asignado_id' in data:
            oportunidad.empleado_asignado_id = data['empleado_asignado_id']
        if 'servicio_id' in data:
            oportunidad.servicio_id = data['servicio_id']
        if 'fuente_id' in data:
            oportunidad.fuente_id = data['fuente_id']
        if 'notas' in data:
            oportunidad.notas = data['notas']
        if 'motivo_perdida' in data:
            oportunidad.motivo_perdida = data['motivo_perdida']
        if 'competidor' in data:
            oportunidad.competidor = data['competidor']
        
        # Actualizar fechas
        if 'fecha_estimada_cierre' in data and data['fecha_estimada_cierre']:
            try:
                oportunidad.fecha_estimada_cierre = datetime.strptime(
                    data['fecha_estimada_cierre'], '%Y-%m-%d'
                ).date()
            except ValueError:
                pass
        
        # Si se cambia a cerrado, establecer fecha de cierre real
        if data.get('estado') == 'cerrado' and not oportunidad.fecha_cierre_real:
            oportunidad.fecha_cierre_real = datetime.utcnow().date()
        
        oportunidad.fecha_actualizacion = datetime.utcnow()
        oportunidad.save()
        
        return jsonify({
            'success': True,
            'message': 'Oportunidad actualizada exitosamente',
            'data': oportunidad.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar oportunidad: {str(e)}'
        }), 500

@oportunidades_bp.route('/oportunidades/<int:oportunidad_id>/estado', methods=['PUT'])
def cambiar_estado_oportunidad(oportunidad_id):
    """Cambia el estado de una oportunidad (para drag & drop en Kanban)"""
    try:
        oportunidad = Oportunidad.get_by_id(oportunidad_id)
        
        if not oportunidad:
            return jsonify({
                'success': False,
                'message': 'Oportunidad no encontrada'
            }), 404
        
        data = request.get_json()
        nuevo_estado = data.get('estado')
        resultado = data.get('resultado')
        
        if not nuevo_estado:
            return jsonify({
                'success': False,
                'message': 'El nuevo estado es requerido'
            }), 400
        
        oportunidad.cambiar_estado(nuevo_estado, resultado)
        
        return jsonify({
            'success': True,
            'message': 'Estado actualizado exitosamente',
            'data': oportunidad.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al cambiar estado: {str(e)}'
        }), 500

@oportunidades_bp.route('/oportunidades/<int:oportunidad_id>', methods=['DELETE'])
def delete_oportunidad(oportunidad_id):
    """Elimina una oportunidad"""
    try:
        oportunidad = Oportunidad.get_by_id(oportunidad_id)
        
        if not oportunidad:
            return jsonify({
                'success': False,
                'message': 'Oportunidad no encontrada'
            }), 404
        
        oportunidad.delete()
        
        return jsonify({
            'success': True,
            'message': 'Oportunidad eliminada exitosamente'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar oportunidad: {str(e)}'
        }), 500

@oportunidades_bp.route('/oportunidades/estadisticas', methods=['GET'])
def get_estadisticas_oportunidades():
    """Obtiene estadísticas de oportunidades"""
    try:
        estadisticas = Oportunidad.get_estadisticas()
        
        return jsonify({
            'success': True,
            'data': estadisticas
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }), 500

