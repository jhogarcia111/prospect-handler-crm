from flask import Blueprint, request, jsonify
from src.models import Empleado, db
from datetime import datetime

empleados_bp = Blueprint('empleados', __name__)

@empleados_bp.route('/empleados', methods=['GET'])
def get_empleados():
    """Obtiene todos los empleados con filtros opcionales"""
    try:
        filtros = {}
        
        # Obtener parámetros de consulta
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('departamento'):
            filtros['departamento'] = request.args.get('departamento')
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        empleados = Empleado.get_all(filtros)
        
        return jsonify({
            'success': True,
            'data': [empleado.to_dict() for empleado in empleados],
            'total': len(empleados)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener empleados: {str(e)}'
        }), 500

@empleados_bp.route('/empleados/activos', methods=['GET'])
def get_empleados_activos():
    """Obtiene solo empleados activos (para selects)"""
    try:
        empleados = Empleado.get_activos()
        
        return jsonify({
            'success': True,
            'data': [{'id': emp.id, 'nombre': emp.nombre_completo} for emp in empleados],
            'total': len(empleados)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener empleados activos: {str(e)}'
        }), 500

@empleados_bp.route('/empleados/<int:empleado_id>', methods=['GET'])
def get_empleado(empleado_id):
    """Obtiene un empleado específico por ID"""
    try:
        empleado = Empleado.get_by_id(empleado_id)
        
        if not empleado:
            return jsonify({
                'success': False,
                'message': 'Empleado no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': empleado.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener empleado: {str(e)}'
        }), 500

@empleados_bp.route('/empleados', methods=['POST'])
def create_empleado():
    """Crea un nuevo empleado"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'El nombre es requerido'
            }), 400
        
        # Crear nuevo empleado
        empleado = Empleado(
            nombre=data['nombre'],
            apellido=data.get('apellido'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            posicion=data.get('posicion'),
            departamento=data.get('departamento'),
            salario=data.get('salario'),
            estado=data.get('estado', 'activo'),
            supervisor_id=data.get('supervisor_id'),
            notas=data.get('notas')
        )
        
        # Convertir fecha de ingreso si se proporciona
        if data.get('fecha_ingreso'):
            try:
                empleado.fecha_ingreso = datetime.strptime(
                    data['fecha_ingreso'], '%Y-%m-%d'
                ).date()
            except ValueError:
                pass
        
        empleado.save()
        
        return jsonify({
            'success': True,
            'message': 'Empleado creado exitosamente',
            'data': empleado.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear empleado: {str(e)}'
        }), 500

@empleados_bp.route('/empleados/<int:empleado_id>', methods=['PUT'])
def update_empleado(empleado_id):
    """Actualiza un empleado existente"""
    try:
        empleado = Empleado.get_by_id(empleado_id)
        
        if not empleado:
            return jsonify({
                'success': False,
                'message': 'Empleado no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            empleado.nombre = data['nombre']
        if 'apellido' in data:
            empleado.apellido = data['apellido']
        if 'email' in data:
            empleado.email = data['email']
        if 'telefono' in data:
            empleado.telefono = data['telefono']
        if 'posicion' in data:
            empleado.posicion = data['posicion']
        if 'departamento' in data:
            empleado.departamento = data['departamento']
        if 'salario' in data:
            empleado.salario = data['salario']
        if 'estado' in data:
            empleado.estado = data['estado']
        if 'supervisor_id' in data:
            empleado.supervisor_id = data['supervisor_id']
        if 'notas' in data:
            empleado.notas = data['notas']
        
        # Actualizar fecha de ingreso
        if 'fecha_ingreso' in data and data['fecha_ingreso']:
            try:
                empleado.fecha_ingreso = datetime.strptime(
                    data['fecha_ingreso'], '%Y-%m-%d'
                ).date()
            except ValueError:
                pass
        
        empleado.fecha_actualizacion = datetime.utcnow()
        empleado.save()
        
        return jsonify({
            'success': True,
            'message': 'Empleado actualizado exitosamente',
            'data': empleado.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar empleado: {str(e)}'
        }), 500

@empleados_bp.route('/empleados/<int:empleado_id>', methods=['DELETE'])
def delete_empleado(empleado_id):
    """Elimina un empleado"""
    try:
        empleado = Empleado.get_by_id(empleado_id)
        
        if not empleado:
            return jsonify({
                'success': False,
                'message': 'Empleado no encontrado'
            }), 404
        
        empleado.delete()
        
        return jsonify({
            'success': True,
            'message': 'Empleado eliminado exitosamente'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar empleado: {str(e)}'
        }), 500

@empleados_bp.route('/empleados/estadisticas', methods=['GET'])
def get_estadisticas_empleados():
    """Obtiene estadísticas de empleados"""
    try:
        estadisticas = Empleado.get_estadisticas()
        
        return jsonify({
            'success': True,
            'data': estadisticas
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }), 500

@empleados_bp.route('/empleados/<int:empleado_id>/rendimiento', methods=['GET'])
def get_rendimiento_empleado(empleado_id):
    """Obtiene métricas de rendimiento de un empleado"""
    try:
        empleado = Empleado.get_by_id(empleado_id)
        
        if not empleado:
            return jsonify({
                'success': False,
                'message': 'Empleado no encontrado'
            }), 404
        
        # Obtener estadísticas del empleado
        total_clientes = len(empleado.clientes_asignados) if hasattr(empleado, 'clientes_asignados') else 0
        total_oportunidades = len(empleado.oportunidades_asignadas) if hasattr(empleado, 'oportunidades_asignadas') else 0
        total_actividades = len(empleado.actividades_realizadas) if hasattr(empleado, 'actividades_realizadas') else 0
        
        # Calcular valor total de oportunidades asignadas
        valor_total_oportunidades = 0
        if hasattr(empleado, 'oportunidades_asignadas'):
            for oportunidad in empleado.oportunidades_asignadas:
                if oportunidad.valor_estimado:
                    valor_total_oportunidades += float(oportunidad.valor_estimado)
        
        # Calcular oportunidades cerradas ganadas
        oportunidades_ganadas = 0
        if hasattr(empleado, 'oportunidades_asignadas'):
            oportunidades_ganadas = len([
                opp for opp in empleado.oportunidades_asignadas 
                if opp.estado == 'cerrado' and opp.resultado == 'ganado'
            ])
        
        return jsonify({
            'success': True,
            'data': {
                'empleado': empleado.to_dict(),
                'total_clientes': total_clientes,
                'total_oportunidades': total_oportunidades,
                'total_actividades': total_actividades,
                'valor_total_oportunidades': valor_total_oportunidades,
                'oportunidades_ganadas': oportunidades_ganadas,
                'tasa_conversion': round((oportunidades_ganadas / total_oportunidades * 100) if total_oportunidades > 0 else 0, 2)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener rendimiento: {str(e)}'
        }), 500

