// Configuración base de la API
const API_BASE_URL = 'https://5000-icvr8o94zm604eokr0hcn-e716493d.manusvm.computer/api';

// Función helper para hacer peticiones HTTP
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || `HTTP error! status: ${response.status}`);
    }
    
    return data;
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};

// ==================== CLIENTES ====================

export const clientesAPI = {
  // Obtener todos los clientes
  getAll: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.keys(filtros).forEach(key => {
      if (filtros[key]) params.append(key, filtros[key]);
    });
    
    const queryString = params.toString();
    return apiRequest(`/clientes${queryString ? `?${queryString}` : ''}`);
  },

  // Obtener cliente por ID
  getById: (id) => apiRequest(`/clientes/${id}`),

  // Crear nuevo cliente
  create: (clienteData) => apiRequest('/clientes', {
    method: 'POST',
    body: JSON.stringify(clienteData),
  }),

  // Actualizar cliente
  update: (id, clienteData) => apiRequest(`/clientes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(clienteData),
  }),

  // Eliminar cliente
  delete: (id) => apiRequest(`/clientes/${id}`, {
    method: 'DELETE',
  }),

  // Obtener estadísticas de clientes
  getEstadisticas: () => apiRequest('/clientes/estadisticas'),
};

// ==================== OPORTUNIDADES ====================

export const oportunidadesAPI = {
  // Obtener todas las oportunidades
  getAll: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.keys(filtros).forEach(key => {
      if (filtros[key]) params.append(key, filtros[key]);
    });
    
    const queryString = params.toString();
    return apiRequest(`/oportunidades${queryString ? `?${queryString}` : ''}`);
  },

  // Obtener oportunidades para Kanban
  getKanban: () => apiRequest('/oportunidades/kanban'),

  // Obtener oportunidad por ID
  getById: (id) => apiRequest(`/oportunidades/${id}`),

  // Crear nueva oportunidad
  create: (oportunidadData) => apiRequest('/oportunidades', {
    method: 'POST',
    body: JSON.stringify(oportunidadData),
  }),

  // Actualizar oportunidad
  update: (id, oportunidadData) => apiRequest(`/oportunidades/${id}`, {
    method: 'PUT',
    body: JSON.stringify(oportunidadData),
  }),

  // Cambiar estado de oportunidad (para Kanban)
  cambiarEstado: (id, estado, resultado = null) => apiRequest(`/oportunidades/${id}/estado`, {
    method: 'PUT',
    body: JSON.stringify({ estado, resultado }),
  }),

  // Eliminar oportunidad
  delete: (id) => apiRequest(`/oportunidades/${id}`, {
    method: 'DELETE',
  }),

  // Obtener estadísticas de oportunidades
  getEstadisticas: () => apiRequest('/oportunidades/estadisticas'),
};

// ==================== ACTIVIDADES ====================

export const actividadesAPI = {
  // Obtener todas las actividades
  getAll: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.keys(filtros).forEach(key => {
      if (filtros[key]) params.append(key, filtros[key]);
    });
    
    const queryString = params.toString();
    return apiRequest(`/actividades${queryString ? `?${queryString}` : ''}`);
  },

  // Obtener actividad por ID
  getById: (id) => apiRequest(`/actividades/${id}`),

  // Crear nueva actividad
  create: (actividadData) => apiRequest('/actividades', {
    method: 'POST',
    body: JSON.stringify(actividadData),
  }),

  // Actualizar actividad
  update: (id, actividadData) => apiRequest(`/actividades/${id}`, {
    method: 'PUT',
    body: JSON.stringify(actividadData),
  }),

  // Eliminar actividad
  delete: (id) => apiRequest(`/actividades/${id}`, {
    method: 'DELETE',
  }),

  // Obtener próximas acciones
  getProximasAcciones: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.keys(filtros).forEach(key => {
      if (filtros[key]) params.append(key, filtros[key]);
    });
    
    const queryString = params.toString();
    return apiRequest(`/actividades/proximas-acciones${queryString ? `?${queryString}` : ''}`);
  },

  // Obtener actividades recientes
  getRecientes: (limite = 10, empleadoId = null) => {
    const params = new URLSearchParams();
    params.append('limite', limite);
    if (empleadoId) params.append('empleado_id', empleadoId);
    
    return apiRequest(`/actividades/recientes?${params.toString()}`);
  },
};

// ==================== EMPLEADOS ====================

export const empleadosAPI = {
  // Obtener todos los empleados
  getAll: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.keys(filtros).forEach(key => {
      if (filtros[key]) params.append(key, filtros[key]);
    });
    
    const queryString = params.toString();
    return apiRequest(`/empleados${queryString ? `?${queryString}` : ''}`);
  },

  // Obtener empleados activos (para selects)
  getActivos: () => apiRequest('/empleados/activos'),

  // Obtener empleado por ID
  getById: (id) => apiRequest(`/empleados/${id}`),

  // Crear nuevo empleado
  create: (empleadoData) => apiRequest('/empleados', {
    method: 'POST',
    body: JSON.stringify(empleadoData),
  }),

  // Actualizar empleado
  update: (id, empleadoData) => apiRequest(`/empleados/${id}`, {
    method: 'PUT',
    body: JSON.stringify(empleadoData),
  }),

  // Eliminar empleado
  delete: (id) => apiRequest(`/empleados/${id}`, {
    method: 'DELETE',
  }),

  // Obtener estadísticas de empleados
  getEstadisticas: () => apiRequest('/empleados/estadisticas'),

  // Obtener rendimiento de empleado
  getRendimiento: (id) => apiRequest(`/empleados/${id}/rendimiento`),
};

// ==================== CATÁLOGOS ====================

export const catalogosAPI = {
  // Industrias
  industrias: {
    getAll: (filtros = {}) => {
      const params = new URLSearchParams();
      Object.keys(filtros).forEach(key => {
        if (filtros[key] !== undefined) params.append(key, filtros[key]);
      });
      
      const queryString = params.toString();
      return apiRequest(`/industrias${queryString ? `?${queryString}` : ''}`);
    },
    create: (data) => apiRequest('/industrias', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id, data) => apiRequest(`/industrias/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    delete: (id) => apiRequest(`/industrias/${id}`, {
      method: 'DELETE',
    }),
  },

  // Fuentes
  fuentes: {
    getAll: (filtros = {}) => {
      const params = new URLSearchParams();
      Object.keys(filtros).forEach(key => {
        if (filtros[key] !== undefined) params.append(key, filtros[key]);
      });
      
      const queryString = params.toString();
      return apiRequest(`/fuentes${queryString ? `?${queryString}` : ''}`);
    },
    create: (data) => apiRequest('/fuentes', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },

  // Servicios
  servicios: {
    getAll: (filtros = {}) => {
      const params = new URLSearchParams();
      Object.keys(filtros).forEach(key => {
        if (filtros[key] !== undefined) params.append(key, filtros[key]);
      });
      
      const queryString = params.toString();
      return apiRequest(`/servicios${queryString ? `?${queryString}` : ''}`);
    },
    create: (data) => apiRequest('/servicios', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },

  // Plataformas
  plataformas: {
    getAll: (filtros = {}) => {
      const params = new URLSearchParams();
      Object.keys(filtros).forEach(key => {
        if (filtros[key] !== undefined) params.append(key, filtros[key]);
      });
      
      const queryString = params.toString();
      return apiRequest(`/plataformas${queryString ? `?${queryString}` : ''}`);
    },
    create: (data) => apiRequest('/plataformas', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },

  // Resultados
  resultados: {
    getAll: (filtros = {}) => {
      const params = new URLSearchParams();
      Object.keys(filtros).forEach(key => {
        if (filtros[key] !== undefined) params.append(key, filtros[key]);
      });
      
      const queryString = params.toString();
      return apiRequest(`/resultados${queryString ? `?${queryString}` : ''}`);
    },
    create: (data) => apiRequest('/resultados', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },

  // Medios de Pago
  mediosPago: {
    getAll: (filtros = {}) => {
      const params = new URLSearchParams();
      Object.keys(filtros).forEach(key => {
        if (filtros[key] !== undefined) params.append(key, filtros[key]);
      });
      
      const queryString = params.toString();
      return apiRequest(`/medios-pago${queryString ? `?${queryString}` : ''}`);
    },
    create: (data) => apiRequest('/medios-pago', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },

  // Resumen de todos los catálogos
  getResumen: () => apiRequest('/catalogos/resumen'),
};

// ==================== DASHBOARD ====================

export const dashboardAPI = {
  // Obtener datos del dashboard
  getDatos: async () => {
    try {
      const [
        clientesStats,
        oportunidadesStats,
        empleadosStats,
        actividadesRecientes
      ] = await Promise.all([
        clientesAPI.getEstadisticas(),
        oportunidadesAPI.getEstadisticas(),
        empleadosAPI.getEstadisticas(),
        actividadesAPI.getRecientes(5)
      ]);

      return {
        success: true,
        data: {
          clientes: clientesStats.data,
          oportunidades: oportunidadesStats.data,
          empleados: empleadosStats.data,
          actividades_recientes: actividadesRecientes.data
        }
      };
    } catch (error) {
      console.error('Error al obtener datos del dashboard:', error);
      throw error;
    }
  }
};

// Exportar todas las APIs
export default {
  clientes: clientesAPI,
  oportunidades: oportunidadesAPI,
  actividades: actividadesAPI,
  empleados: empleadosAPI,
  catalogos: catalogosAPI,
  dashboard: dashboardAPI,
};

