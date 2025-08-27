from flask import Blueprint, request, jsonify
from src.models import Cliente, Industria, Fuente, Empleado, db
from datetime import datetime

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """Obtiene todos los clientes con filtros opcionales"""
    try:
        filtros = {}
        
        # Obtener parámetros de consulta
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('industria_id'):
            filtros['industria_id'] = int(request.args.get('industria_id'))
        if request.args.get('empleado_asignado_id'):
            filtros['empleado_asignado_id'] = int(request.args.get('empleado_asignado_id'))
        if request.args.get('busqueda'):
            filtros['busqueda'] = request.args.get('busqueda')
        
        clientes = Cliente.get_all(filtros)
        
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes],
            'total': len(clientes)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener clientes: {str(e)}'
        }), 500

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """Obtiene un cliente específico por ID"""
    try:
        cliente = Cliente.get_by_id(cliente_id)
        
        if not cliente:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': cliente.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener cliente: {str(e)}'
        }), 500

@clientes_bp.route('/clientes', methods=['POST'])
def create_cliente():
    """Crea un nuevo cliente"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('nombre_completo'):
            return jsonify({
                'success': False,
                'message': 'El nombre completo es requerido'
            }), 400
        
        # Crear nuevo cliente
        cliente = Cliente(
            nombre_completo=data['nombre_completo'],
            empresa=data.get('empresa'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            telefono_movil=data.get('telefono_movil'),
            direccion=data.get('direccion'),
            ciudad=data.get('ciudad'),
            estado_provincia=data.get('estado_provincia'),
            codigo_postal=data.get('codigo_postal'),
            pais=data.get('pais', 'Colombia'),
            industria_id=data.get('industria_id'),
            fuente_id=data.get('fuente_id'),
            estado=data.get('estado', 'prospecto'),
            empleado_asignado_id=data.get('empleado_asignado_id'),
            sitio_web=data.get('sitio_web'),
            linkedin=data.get('linkedin'),
            notas=data.get('notas'),
            valor_estimado=data.get('valor_estimado')
        )
        
        cliente.save()
        
        return jsonify({
            'success': True,
            'message': 'Cliente creado exitosamente',
            'data': cliente.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear cliente: {str(e)}'
        }), 500

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    """Actualiza un cliente existente"""
    try:
        cliente = Cliente.get_by_id(cliente_id)
        
        if not cliente:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre_completo' in data:
            cliente.nombre_completo = data['nombre_completo']
        if 'empresa' in data:
            cliente.empresa = data['empresa']
        if 'email' in data:
            cliente.email = data['email']
        if 'telefono' in data:
            cliente.telefono = data['telefono']
        if 'telefono_movil' in data:
            cliente.telefono_movil = data['telefono_movil']
        if 'direccion' in data:
            cliente.direccion = data['direccion']
        if 'ciudad' in data:
            cliente.ciudad = data['ciudad']
        if 'estado_provincia' in data:
            cliente.estado_provincia = data['estado_provincia']
        if 'codigo_postal' in data:
            cliente.codigo_postal = data['codigo_postal']
        if 'pais' in data:
            cliente.pais = data['pais']
        if 'industria_id' in data:
            cliente.industria_id = data['industria_id']
        if 'fuente_id' in data:
            cliente.fuente_id = data['fuente_id']
        if 'estado' in data:
            cliente.estado = data['estado']
        if 'empleado_asignado_id' in data:
            cliente.empleado_asignado_id = data['empleado_asignado_id']
        if 'sitio_web' in data:
            cliente.sitio_web = data['sitio_web']
        if 'linkedin' in data:
            cliente.linkedin = data['linkedin']
        if 'notas' in data:
            cliente.notas = data['notas']
        if 'valor_estimado' in data:
            cliente.valor_estimado = data['valor_estimado']
        
        cliente.fecha_actualizacion = datetime.utcnow()
        cliente.save()
        
        return jsonify({
            'success': True,
            'message': 'Cliente actualizado exitosamente',
            'data': cliente.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar cliente: {str(e)}'
        }), 500

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    """Elimina un cliente"""
    try:
        cliente = Cliente.get_by_id(cliente_id)
        
        if not cliente:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
        
        cliente.delete()
        
        return jsonify({
            'success': True,
            'message': 'Cliente eliminado exitosamente'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar cliente: {str(e)}'
        }), 500

@clientes_bp.route('/clientes/estadisticas', methods=['GET'])
def get_estadisticas_clientes():
    """Obtiene estadísticas de clientes"""
    try:
        total = Cliente.query.count()
        prospectos = Cliente.query.filter(Cliente.estado == 'prospecto').count()
        activos = Cliente.query.filter(Cliente.estado == 'activo').count()
        inactivos = Cliente.query.filter(Cliente.estado == 'inactivo').count()
        
        # Clientes por industria
        industrias = db.session.query(
            Industria.nombre,
            db.func.count(Cliente.id)
        ).join(Cliente, Cliente.industria_id == Industria.id, isouter=True).group_by(Industria.nombre).all()
        
        # Clientes por fuente
        fuentes = db.session.query(
            Fuente.nombre,
            db.func.count(Cliente.id)
        ).join(Cliente, Cliente.fuente_id == Fuente.id, isouter=True).group_by(Fuente.nombre).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'prospectos': prospectos,
                'activos': activos,
                'inactivos': inactivos,
                'por_industria': dict(industrias) if industrias else {},
                'por_fuente': dict(fuentes) if fuentes else {}
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }), 500

