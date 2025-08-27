-- =====================================================
-- SCRIPT DE CONFIGURACIÓN DE BASE DE DATOS MYSQL
-- PROSPECT HANDLER CRM
-- =====================================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS prospect_handler CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE prospect_handler;

-- =====================================================
-- TABLAS DE CATÁLOGOS
-- =====================================================

-- Tabla de Industrias
CREATE TABLE IF NOT EXISTS tblIndustrias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Fuentes
CREATE TABLE IF NOT EXISTS tblFuentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    tipo VARCHAR(100),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Servicios
CREATE TABLE IF NOT EXISTS tblServicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),
    precio_base DECIMAL(15,2),
    unidad VARCHAR(50),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Plataformas
CREATE TABLE IF NOT EXISTS tblPlataformas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    url VARCHAR(500),
    tipo VARCHAR(100),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Resultados
CREATE TABLE IF NOT EXISTS tblResultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    categoria VARCHAR(100),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Medios de Pago
CREATE TABLE IF NOT EXISTS tblMediosDePago (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    tipo VARCHAR(100),
    comision_porcentaje DECIMAL(5,2),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA DE EMPLEADOS
-- =====================================================

CREATE TABLE IF NOT EXISTS tblEmpleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    telefono VARCHAR(50),
    posicion VARCHAR(255),
    departamento VARCHAR(100),
    fecha_ingreso DATE,
    salario DECIMAL(15,2),
    estado VARCHAR(50) NOT NULL DEFAULT 'activo',
    supervisor_id INT,
    notas TEXT,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supervisor_id) REFERENCES tblEmpleados(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA DE CLIENTES
-- =====================================================

CREATE TABLE IF NOT EXISTS tblClientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    empresa VARCHAR(255),
    cargo VARCHAR(255),
    email VARCHAR(255),
    telefono VARCHAR(50),
    telefono_alternativo VARCHAR(50),
    direccion TEXT,
    ciudad VARCHAR(100),
    pais VARCHAR(100),
    codigo_postal VARCHAR(20),
    industria_id INT,
    fuente_id INT,
    empleado_asignado_id INT,
    estado VARCHAR(50) NOT NULL DEFAULT 'prospecto',
    calificacion VARCHAR(20),
    sitio_web VARCHAR(255),
    linkedin VARCHAR(255),
    notas TEXT,
    valor_estimado DECIMAL(15,2),
    fecha_primer_contacto DATETIME,
    fecha_ultimo_contacto DATETIME,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (industria_id) REFERENCES tblIndustrias(id) ON DELETE SET NULL,
    FOREIGN KEY (fuente_id) REFERENCES tblFuentes(id) ON DELETE SET NULL,
    FOREIGN KEY (empleado_asignado_id) REFERENCES tblEmpleados(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA DE OPORTUNIDADES
-- =====================================================

CREATE TABLE IF NOT EXISTS tblOportunidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    cliente_id INT NOT NULL,
    valor_estimado DECIMAL(15,2),
    probabilidad INT DEFAULT 50,
    prioridad VARCHAR(20) NOT NULL DEFAULT 'medium',
    estado VARCHAR(50) NOT NULL DEFAULT 'prospecto',
    resultado VARCHAR(50),
    empleado_asignado_id INT,
    servicio_id INT,
    fuente_id INT,
    fecha_estimada_cierre DATE,
    fecha_cierre_real DATE,
    motivo_perdida TEXT,
    competidor VARCHAR(255),
    notas TEXT,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES tblClientes(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_asignado_id) REFERENCES tblEmpleados(id) ON DELETE SET NULL,
    FOREIGN KEY (servicio_id) REFERENCES tblServicios(id) ON DELETE SET NULL,
    FOREIGN KEY (fuente_id) REFERENCES tblFuentes(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA DE ACTIVIDADES REALIZADAS
-- =====================================================

CREATE TABLE IF NOT EXISTS tblActividadesRealizadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    resultado VARCHAR(100) NOT NULL,
    cliente_id INT,
    oportunidad_id INT,
    empleado_id INT,
    fecha DATE NOT NULL,
    hora TIME,
    duracion_minutos INT,
    proxima_accion TEXT,
    fecha_proxima_accion DATE,
    notas TEXT,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES tblClientes(id) ON DELETE CASCADE,
    FOREIGN KEY (oportunidad_id) REFERENCES tblOportunidades(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES tblEmpleados(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA DE PAGOS RECIBIDOS
-- =====================================================

CREATE TABLE IF NOT EXISTS tblPagosRecibidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_factura VARCHAR(100),
    cliente_id INT NOT NULL,
    oportunidad_id INT,
    medio_pago_id INT,
    monto_bruto DECIMAL(15,2) NOT NULL,
    descuento DECIMAL(15,2) DEFAULT 0,
    impuestos DECIMAL(15,2) DEFAULT 0,
    comision DECIMAL(15,2) DEFAULT 0,
    monto_neto DECIMAL(15,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    fecha_vencimiento DATE,
    estado VARCHAR(50) NOT NULL DEFAULT 'pendiente',
    referencia_pago VARCHAR(255),
    notas TEXT,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES tblClientes(id) ON DELETE CASCADE,
    FOREIGN KEY (oportunidad_id) REFERENCES tblOportunidades(id) ON DELETE SET NULL,
    FOREIGN KEY (medio_pago_id) REFERENCES tblMediosDePago(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA DE CONTROL
-- =====================================================

CREATE TABLE IF NOT EXISTS tblControl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parametro VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    descripcion TEXT,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- DATOS DE EJEMPLO
-- =====================================================

-- Insertar Industrias
INSERT IGNORE INTO tblIndustrias (nombre, descripcion) VALUES
('Tecnología', 'Empresas de desarrollo de software y tecnología'),
('Servicios', 'Empresas de servicios profesionales'),
('Manufactura', 'Empresas de manufactura y producción'),
('Salud', 'Empresas del sector salud y farmacéutico'),
('Educación', 'Instituciones educativas y de capacitación'),
('Finanzas', 'Bancos, aseguradoras y servicios financieros'),
('Retail', 'Comercio minorista y e-commerce'),
('Construcción', 'Empresas de construcción e inmobiliarias');

-- Insertar Fuentes
INSERT IGNORE INTO tblFuentes (nombre, descripcion, tipo) VALUES
('LinkedIn', 'Contactos generados a través de LinkedIn', 'Red Social'),
('WhatsApp', 'Contactos generados a través de WhatsApp', 'Mensajería'),
('Email Marketing', 'Contactos generados por campañas de email', 'Email'),
('Referidos', 'Contactos referidos por clientes existentes', 'Referencia'),
('Sitio Web', 'Contactos que llegaron a través del sitio web', 'Web'),
('Eventos', 'Contactos generados en eventos y conferencias', 'Evento'),
('Llamadas en Frío', 'Contactos generados por llamadas directas', 'Teléfono'),
('Google Ads', 'Contactos generados por publicidad en Google', 'Publicidad');

-- Insertar Servicios
INSERT IGNORE INTO tblServicios (nombre, descripcion, categoria, precio_base, unidad) VALUES
('Desarrollo Web', 'Desarrollo de sitios web y aplicaciones', 'Desarrollo', 5000.00, 'proyecto'),
('Consultoría IT', 'Consultoría en tecnologías de información', 'Consultoría', 150.00, 'hora'),
('Marketing Digital', 'Servicios de marketing digital y SEO', 'Marketing', 2000.00, 'mes'),
('Diseño Gráfico', 'Diseño de identidad corporativa y materiales', 'Diseño', 800.00, 'proyecto'),
('Capacitación', 'Cursos y capacitaciones empresariales', 'Educación', 300.00, 'hora'),
('Soporte Técnico', 'Soporte técnico y mantenimiento', 'Soporte', 100.00, 'hora');

-- Insertar Plataformas
INSERT IGNORE INTO tblPlataformas (nombre, descripcion, url, tipo) VALUES
('LinkedIn Sales Navigator', 'Herramienta de prospección en LinkedIn', 'https://linkedin.com', 'CRM'),
('HubSpot', 'Plataforma de CRM y marketing', 'https://hubspot.com', 'CRM'),
('Mailchimp', 'Plataforma de email marketing', 'https://mailchimp.com', 'Email'),
('Zoom', 'Plataforma de videoconferencias', 'https://zoom.us', 'Comunicación'),
('Slack', 'Plataforma de comunicación empresarial', 'https://slack.com', 'Comunicación'),
('Google Workspace', 'Suite de productividad de Google', 'https://workspace.google.com', 'Productividad');

-- Insertar Resultados
INSERT IGNORE INTO tblResultados (nombre, descripcion, categoria) VALUES
('Exitoso', 'La actividad se completó exitosamente', 'Positivo'),
('Sin Respuesta', 'No hubo respuesta del contacto', 'Neutro'),
('No Interesado', 'El contacto no mostró interés', 'Negativo'),
('Reagendar', 'Se necesita reagendar la actividad', 'Pendiente'),
('Información Enviada', 'Se envió información solicitada', 'Positivo'),
('Reunión Programada', 'Se programó una reunión', 'Positivo'),
('Propuesta Solicitada', 'El cliente solicitó una propuesta', 'Positivo'),
('Cerrado - Ganado', 'Se cerró la venta exitosamente', 'Positivo'),
('Cerrado - Perdido', 'Se perdió la oportunidad', 'Negativo');

-- Insertar Medios de Pago
INSERT IGNORE INTO tblMediosDePago (nombre, descripcion, tipo, comision_porcentaje) VALUES
('Transferencia Bancaria', 'Pago por transferencia bancaria', 'Transferencia', 0.00),
('Tarjeta de Crédito', 'Pago con tarjeta de crédito', 'Tarjeta', 3.50),
('PayPal', 'Pago a través de PayPal', 'Digital', 4.00),
('Efectivo', 'Pago en efectivo', 'Efectivo', 0.00),
('Cheque', 'Pago con cheque', 'Cheque', 0.00),
('Stripe', 'Pago a través de Stripe', 'Digital', 2.90),
('Mercado Pago', 'Pago a través de Mercado Pago', 'Digital', 5.00);

-- Insertar Empleados de ejemplo
INSERT IGNORE INTO tblEmpleados (nombre, apellido, email, telefono, posicion, departamento, fecha_ingreso, salario, estado) VALUES
('Juan', 'Pérez', 'juan.perez@empresa.com', '+1234567890', 'Gerente de Ventas', 'Ventas', '2023-01-15', 75000.00, 'activo'),
('María', 'González', 'maria.gonzalez@empresa.com', '+1234567891', 'Ejecutiva de Ventas', 'Ventas', '2023-03-01', 55000.00, 'activo'),
('Carlos', 'Rodríguez', 'carlos.rodriguez@empresa.com', '+1234567892', 'Desarrollador Senior', 'Tecnología', '2022-11-10', 80000.00, 'activo'),
('Ana', 'Martínez', 'ana.martinez@empresa.com', '+1234567893', 'Especialista en Marketing', 'Marketing', '2023-05-20', 60000.00, 'activo');

-- Insertar Clientes de ejemplo
INSERT IGNORE INTO tblClientes (nombre_completo, empresa, cargo, email, telefono, industria_id, fuente_id, empleado_asignado_id, estado, calificacion, fecha_primer_contacto) VALUES
('Roberto Fernández', 'SmartBusiness Corp', 'CEO', 'roberto@smartbusiness.com', '+1234567894', 1, 1, 1, 'cliente', 'A', '2024-01-15 10:30:00'),
('Laura Sánchez', 'TechInnovate Solutions', 'CTO', 'laura@techinnovate.com', '+1234567895', 1, 2, 2, 'prospecto', 'B', '2024-02-20 14:15:00'),
('Miguel Torres', 'Global Services Inc', 'Director de Operaciones', 'miguel@globalservices.com', '+1234567896', 2, 3, 1, 'cliente', 'A', '2024-01-10 09:00:00'),
('Carmen López', 'HealthTech Innovations', 'Gerente de Proyectos', 'carmen@healthtech.com', '+1234567897', 4, 1, 3, 'prospecto', 'C', '2024-03-05 16:45:00'),
('Diego Ramírez', 'EduSoft Solutions', 'Fundador', 'diego@edusoft.com', '+1234567898', 5, 4, 2, 'lead', 'B', '2024-03-15 11:20:00');

-- Insertar Oportunidades de ejemplo
INSERT IGNORE INTO tblOportunidades (titulo, descripcion, cliente_id, valor_estimado, probabilidad, prioridad, estado, empleado_asignado_id, servicio_id, fecha_estimada_cierre) VALUES
('Desarrollo de App Móvil - SmartBusiness', 'Desarrollo de aplicación móvil para gestión empresarial', 1, 25000.00, 80, 'high', 'propuesta', 1, 1, '2024-05-30'),
('Consultoría IT - TechInnovate', 'Consultoría para migración a la nube', 2, 15000.00, 60, 'medium', 'contactado', 2, 2, '2024-06-15'),
('Marketing Digital - Global Services', 'Campaña de marketing digital integral', 3, 8000.00, 90, 'high', 'negociacion', 1, 3, '2024-04-20'),
('Sistema de Gestión - HealthTech', 'Desarrollo de sistema de gestión hospitalaria', 4, 45000.00, 40, 'medium', 'prospecto', 3, 1, '2024-07-10'),
('Plataforma E-learning - EduSoft', 'Desarrollo de plataforma de educación online', 5, 30000.00, 70, 'high', 'propuesta', 2, 1, '2024-06-01');

-- Insertar Actividades de ejemplo
INSERT IGNORE INTO tblActividadesRealizadas (tipo, descripcion, resultado, cliente_id, oportunidad_id, empleado_id, fecha, hora, proxima_accion, fecha_proxima_accion) VALUES
('Llamada telefónica', 'Llamada inicial para presentar servicios', 'Exitoso', 1, 1, 1, '2024-03-10', '10:30:00', 'Enviar propuesta comercial', '2024-03-15'),
('Email', 'Envío de información sobre consultoría IT', 'Información Enviada', 2, 2, 2, '2024-03-12', '14:00:00', 'Llamada de seguimiento', '2024-03-18'),
('Reunión', 'Reunión de presentación de propuesta', 'Propuesta Solicitada', 3, 3, 1, '2024-03-08', '16:00:00', 'Enviar cotización final', '2024-03-12'),
('LinkedIn', 'Contacto inicial a través de LinkedIn', 'Sin Respuesta', 4, 4, 3, '2024-03-14', '09:15:00', 'Segundo contacto por email', '2024-03-20'),
('WhatsApp', 'Seguimiento por WhatsApp', 'Reunión Programada', 5, 5, 2, '2024-03-16', '11:45:00', 'Preparar presentación', '2024-03-22');

-- Insertar Pagos de ejemplo
INSERT IGNORE INTO tblPagosRecibidos (numero_factura, cliente_id, oportunidad_id, medio_pago_id, monto_bruto, descuento, impuestos, monto_neto, fecha_pago, estado) VALUES
('FAC-001', 1, 1, 1, 25000.00, 0.00, 4000.00, 29000.00, '2024-03-01', 'pagado'),
('FAC-002', 3, 3, 2, 8000.00, 800.00, 1152.00, 8352.00, '2024-03-15', 'pagado'),
('FAC-003', 2, 2, 3, 15000.00, 0.00, 2400.00, 17400.00, '2024-04-01', 'pendiente');

-- Insertar parámetros de control
INSERT IGNORE INTO tblControl (parametro, valor, descripcion) VALUES
('version_sistema', '1.0.0', 'Versión actual del sistema'),
('moneda_base', 'USD', 'Moneda base para cálculos'),
('iva_porcentaje', '16', 'Porcentaje de IVA aplicable'),
('empresa_nombre', 'Prospect Handler CRM', 'Nombre de la empresa'),
('empresa_email', 'admin@prospecthandler.com', 'Email principal de la empresa');

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para mejorar rendimiento
CREATE INDEX idx_clientes_estado ON tblClientes(estado);
CREATE INDEX idx_clientes_empleado ON tblClientes(empleado_asignado_id);
CREATE INDEX idx_oportunidades_estado ON tblOportunidades(estado);
CREATE INDEX idx_oportunidades_cliente ON tblOportunidades(cliente_id);
CREATE INDEX idx_actividades_fecha ON tblActividadesRealizadas(fecha);
CREATE INDEX idx_actividades_cliente ON tblActividadesRealizadas(cliente_id);
CREATE INDEX idx_pagos_fecha ON tblPagosRecibidos(fecha_pago);
CREATE INDEX idx_pagos_estado ON tblPagosRecibidos(estado);

-- =====================================================
-- SCRIPT COMPLETADO
-- =====================================================

SELECT 'Base de datos Prospect Handler configurada exitosamente' AS mensaje;

