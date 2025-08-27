import { useState, useEffect, useCallback } from 'react';

// Hook personalizado para manejar estados de API
export const useApi = (apiFunction, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (...args) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiFunction(...args);
      setData(response.data);
      return response;
    } catch (err) {
      setError(err.message || 'Error al cargar datos');
      console.error('API Error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiFunction]);

  useEffect(() => {
    fetchData();
  }, dependencies);

  const refetch = useCallback((...args) => {
    return fetchData(...args);
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    refetch,
    setData
  };
};

// Hook para operaciones CRUD
export const useCrud = (apiObject) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const executeOperation = useCallback(async (operation, ...args) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiObject[operation](...args);
      return response;
    } catch (err) {
      setError(err.message || 'Error en la operación');
      console.error('CRUD Error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiObject]);

  const create = useCallback((data) => {
    return executeOperation('create', data);
  }, [executeOperation]);

  const update = useCallback((id, data) => {
    return executeOperation('update', id, data);
  }, [executeOperation]);

  const remove = useCallback((id) => {
    return executeOperation('delete', id);
  }, [executeOperation]);

  const getById = useCallback((id) => {
    return executeOperation('getById', id);
  }, [executeOperation]);

  return {
    loading,
    error,
    create,
    update,
    remove,
    getById,
    setError
  };
};

// Hook para manejar formularios con API
export const useFormApi = (apiFunction, onSuccess, onError) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submit = useCallback(async (formData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiFunction(formData);
      
      if (onSuccess) {
        onSuccess(response);
      }
      
      return response;
    } catch (err) {
      const errorMessage = err.message || 'Error al enviar formulario';
      setError(errorMessage);
      
      if (onError) {
        onError(err);
      }
      
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiFunction, onSuccess, onError]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    loading,
    error,
    submit,
    clearError
  };
};

// Hook para manejar listas con filtros
export const useFilteredList = (apiFunction, initialFilters = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState(initialFilters);
  const [total, setTotal] = useState(0);

  const fetchData = useCallback(async (newFilters = filters) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiFunction(newFilters);
      setData(response.data || []);
      setTotal(response.total || response.data?.length || 0);
      return response;
    } catch (err) {
      setError(err.message || 'Error al cargar datos');
      console.error('Filtered List Error:', err);
      setData([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [apiFunction, filters]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const updateFilters = useCallback((newFilters) => {
    const updatedFilters = { ...filters, ...newFilters };
    setFilters(updatedFilters);
    fetchData(updatedFilters);
  }, [filters, fetchData]);

  const clearFilters = useCallback(() => {
    setFilters(initialFilters);
    fetchData(initialFilters);
  }, [initialFilters, fetchData]);

  const refetch = useCallback(() => {
    return fetchData();
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    filters,
    total,
    updateFilters,
    clearFilters,
    refetch,
    setData
  };
};

// Hook para notificaciones
export const useNotification = () => {
  const [notifications, setNotifications] = useState([]);

  const addNotification = useCallback((message, type = 'info', duration = 5000) => {
    const id = Date.now();
    const notification = { id, message, type };
    
    setNotifications(prev => [...prev, notification]);
    
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }
    
    return id;
  }, []);

  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  }, []);

  const clearNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  return {
    notifications,
    addNotification,
    removeNotification,
    clearNotifications
  };
};

export default {
  useApi,
  useCrud,
  useFormApi,
  useFilteredList,
  useNotification
};

