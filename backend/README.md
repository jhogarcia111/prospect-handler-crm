# Prospect Handler CRM - Backend API

## Descripción
Backend API desarrollado en Flask para el sistema CRM Prospect Handler. Incluye gestión completa de clientes, oportunidades, actividades, empleados y catálogos.

## Características
- ✅ API REST completa con Flask
- ✅ Base de datos MySQL compatible con phpMyAdmin
- ✅ Modelos de datos basados en MS Access
- ✅ CORS habilitado para frontend React
- ✅ Validación de datos y manejo de errores
- ✅ Endpoints para todas las operaciones CRUD

## Estructura del Proyecto
```
prospect-handler-api/
├── src/
│   ├── main.py                 # Archivo principal de Flask
│   ├── models/                 # Modelos de base de datos
│   │   ├── __init__.py
│   │   ├── database.py         # Configuración de base de datos
│   │   ├── cliente.py          # Modelo de Cliente
│   │   ├── oportunidad.py      # Modelo de Oportunidad
│   │   ├── actividad.py        # Modelo de Actividad
│   │   ├── empleado.py         # Modelo de Empleado
│   │   ├── catalogo.py         # Modelos de catálogos
│   │   └── finanzas.py         # Modelos financieros
│   └── routes/                 # Rutas de la API
│       ├── clientes.py         # Endpoints de clientes
│       ├── oportunidades.py    # Endpoints de oportunidades
│       ├── actividades.py      # Endpoints de actividades
│       ├── empleados.py        # Endpoints de empleados
│       └── catalogos.py        # Endpoints de catálogos
├── database_setup.sql          # Script de configuración de MySQL
├── requirements.txt            # Dependencias de Python
└── README.md                   # Este archivo
```

## Configuración de Base de Datos MySQL

### 1. Crear la Base de Datos
Ejecuta el script `database_setup.sql` en phpMyAdmin o tu cliente MySQL:

```sql
-- El script creará automáticamente:
-- - Base de datos 'prospect_handler'
-- - Todas las tablas necesarias
-- - Datos de ejemplo para pruebas
-- - Índices para optimización
```

### 2. Variables de Entorno
Configura las siguientes variables de entorno en tu hosting:

```bash
MYSQL_HOST=localhost          # Host de MySQL
MYSQL_PORT=3306              # Puerto de MySQL (por defecto 3306)
MYSQL_USER=tu_usuario        # Usuario de MySQL
MYSQL_PASSWORD=tu_password   # Contraseña de MySQL
MYSQL_DATABASE=prospect_handler  # Nombre de la base de datos
```

## Instalación Local

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd prospect-handler-api
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=tu_password
export MYSQL_DATABASE=prospect_handler
```

### 5. Ejecutar la aplicación
```bash
cd src
python main.py
```

La API estará disponible en `http://localhost:5000`

## Endpoints de la API

### Clientes
- `GET /api/clientes` - Obtener todos los clientes
- `GET /api/clientes/{id}` - Obtener cliente por ID
- `POST /api/clientes` - Crear nuevo cliente
- `PUT /api/clientes/{id}` - Actualizar cliente
- `DELETE /api/clientes/{id}` - Eliminar cliente
- `GET /api/clientes/estadisticas` - Estadísticas de clientes

### Oportunidades
- `GET /api/oportunidades` - Obtener todas las oportunidades
- `GET /api/oportunidades/kanban` - Datos para tablero Kanban
- `GET /api/oportunidades/{id}` - Obtener oportunidad por ID
- `POST /api/oportunidades` - Crear nueva oportunidad
- `PUT /api/oportunidades/{id}` - Actualizar oportunidad
- `PUT /api/oportunidades/{id}/estado` - Cambiar estado (Kanban)
- `DELETE /api/oportunidades/{id}` - Eliminar oportunidad
- `GET /api/oportunidades/estadisticas` - Estadísticas de oportunidades

### Actividades
- `GET /api/actividades` - Obtener todas las actividades
- `GET /api/actividades/{id}` - Obtener actividad por ID
- `POST /api/actividades` - Crear nueva actividad
- `PUT /api/actividades/{id}` - Actualizar actividad
- `DELETE /api/actividades/{id}` - Eliminar actividad
- `GET /api/actividades/proximas-acciones` - Próximas acciones
- `GET /api/actividades/recientes` - Actividades recientes

### Empleados
- `GET /api/empleados` - Obtener todos los empleados
- `GET /api/empleados/activos` - Empleados activos (para selects)
- `GET /api/empleados/{id}` - Obtener empleado por ID
- `POST /api/empleados` - Crear nuevo empleado
- `PUT /api/empleados/{id}` - Actualizar empleado
- `DELETE /api/empleados/{id}` - Eliminar empleado
- `GET /api/empleados/estadisticas` - Estadísticas de empleados
- `GET /api/empleados/{id}/rendimiento` - Rendimiento de empleado

### Catálogos
- `GET /api/industrias` - Obtener industrias
- `GET /api/fuentes` - Obtener fuentes
- `GET /api/servicios` - Obtener servicios
- `GET /api/plataformas` - Obtener plataformas
- `GET /api/resultados` - Obtener resultados
- `GET /api/medios-pago` - Obtener medios de pago
- `GET /api/catalogos/resumen` - Resumen de todos los catálogos

## Filtros y Parámetros

### Filtros Comunes
- `estado` - Filtrar por estado
- `busqueda` - Búsqueda por texto
- `empleado_id` - Filtrar por empleado asignado
- `fecha_desde` - Filtrar desde fecha
- `fecha_hasta` - Filtrar hasta fecha

### Ejemplo de Uso
```javascript
// Obtener clientes activos
GET /api/clientes?estado=activo

// Buscar oportunidades
GET /api/oportunidades?busqueda=desarrollo&estado=propuesta

// Actividades de un empleado
GET /api/actividades?empleado_id=1&fecha_desde=2024-01-01
```

## Estructura de Respuestas

### Respuesta Exitosa
```json
{
  "success": true,
  "data": [...],
  "total": 10,
  "message": "Operación exitosa"
}
```

### Respuesta de Error
```json
{
  "success": false,
  "message": "Descripción del error"
}
```

## Despliegue en Hosting

### 1. Subir archivos
- Sube todos los archivos del proyecto a tu hosting
- Asegúrate de que el hosting soporte Python y Flask

### 2. Configurar base de datos
- Ejecuta `database_setup.sql` en phpMyAdmin
- Configura las variables de entorno en el panel de control

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar servidor web
- Configura tu servidor web (Apache/Nginx) para servir la aplicación Flask
- Asegúrate de que el puerto esté abierto y accesible

## Datos de Ejemplo

El script SQL incluye datos de ejemplo:
- 8 Industrias
- 8 Fuentes de contacto
- 6 Servicios
- 6 Plataformas
- 9 Tipos de resultado
- 7 Medios de pago
- 4 Empleados
- 5 Clientes
- 5 Oportunidades
- 5 Actividades
- 3 Pagos

## Seguridad

- ✅ Validación de datos de entrada
- ✅ Manejo seguro de errores
- ✅ Configuración de CORS
- ⚠️ **Importante**: Configura autenticación y autorización para producción

## Soporte

Para soporte técnico o preguntas sobre la implementación, contacta al equipo de desarrollo.

## Licencia

Este proyecto es propiedad de [Tu Empresa]. Todos los derechos reservados.

