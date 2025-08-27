import React from 'react';
import { 
  BarChart3, 
  Users, 
  DollarSign, 
  TrendingUp,
  Activity,
  Calendar,
  MessageSquare,
  Phone
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { useApi } from '../hooks/useApi';
import { dashboardAPI } from '../services/api';
import '../App.css'

export default function Dashboard() {
  const { data: dashboardData, loading, error } = useApi(dashboardAPI.getDatos);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map(i => (
              <Card key={i}>
                <CardContent className="p-6">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div className="h-8 bg-gray-200 rounded w-1/2"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h3 className="text-red-800 font-medium">Error al cargar el dashboard</h3>
          <p className="text-red-600 text-sm mt-1">{error}</p>
        </div>
      </div>
    );
  }

  const clientesData = dashboardData?.clientes || {};
  const oportunidadesData = dashboardData?.oportunidades || {};
  const empleadosData = dashboardData?.empleados || {};
  const actividadesRecientes = dashboardData?.actividades_recientes || [];

  // Datos para gráficos
  const opportunityData = [
    { month: 'Ene', value: 15 },
    { month: 'Feb', value: 22 },
    { month: 'Mar', value: 18 },
    { month: 'Abr', value: 28 },
    { month: 'May', value: 35 },
    { month: 'Jun', value: oportunidadesData.abiertas || 42 },
  ];

  const revenueData = [
    { name: 'LinkedIn', value: 45, color: '#0ea5e9' },
    { name: 'WhatsApp', value: 30, color: '#10b981' },
    { name: 'Email', value: 25, color: '#f59e0b' },
  ];

  const recentActivities = actividadesRecientes.length > 0 ? actividadesRecientes.map((actividad, index) => ({
    id: index + 1,
    type: actividad.tipo?.toLowerCase() || 'activity',
    title: actividad.descripcion || actividad.tipo,
    client: actividad.cliente_nombre || 'Cliente',
    time: actividad.fecha || 'Fecha no disponible',
    icon: actividad.tipo === 'Llamada telefónica' ? Phone : 
          actividad.tipo === 'Reunión' ? Calendar : 
          actividad.tipo === 'Email' ? MessageSquare : Activity,
  })) : [
    {
      id: 1,
      type: 'linkedin',
      title: 'Contacto inicial con María González',
      client: 'TechCorp Solutions',
      time: 'Hace 2 horas',
      icon: MessageSquare,
    },
    {
      id: 2,
      type: 'call',
      title: 'Llamada de seguimiento',
      client: 'Innovate Inc',
      time: 'Hace 4 horas',
      icon: Phone,
    },
    {
      id: 3,
      type: 'meeting',
      title: 'Reunión de propuesta',
      client: 'StartupXYZ',
      time: 'Ayer',
      icon: Calendar,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Resumen de tu actividad de prospección</p>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Total Oportunidades
            </CardTitle>
            <BarChart3 className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {oportunidadesData.total || 125}
            </div>
            <p className="text-xs text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +{oportunidadesData.abiertas || 12}% desde el mes pasado
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Clientes Activos
            </CardTitle>
            <Users className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {clientesData.activos || 89}
            </div>
            <p className="text-xs text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +{clientesData.prospectos || 8}% desde el mes pasado
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Valor Pipeline
            </CardTitle>
            <DollarSign className="h-4 w-4 text-emerald-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              ${(oportunidadesData.valor_total_pipeline || 28400).toLocaleString()}
            </div>
            <p className="text-xs text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +15% desde el mes pasado
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Tasa de Conversión
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {oportunidadesData.tasa_conversion || 24.5}%
            </div>
            <p className="text-xs text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +3.2% desde el mes pasado
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos y actividades */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Gráfico de oportunidades */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Oportunidades por Mes</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={opportunityData}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis dataKey="month" />
                <YAxis />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Actividades recientes */}
        <Card>
          <CardHeader>
            <CardTitle>Actividades Recientes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-50">
                    <activity.icon className="h-4 w-4 text-blue-600" />
                  </div>
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-gray-900">
                    {activity.title}
                  </p>
                  <p className="text-sm text-gray-500">{activity.client}</p>
                  <p className="text-xs text-gray-400">{activity.time}</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Gráfico de ingresos por fuente */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Ingresos por Fuente</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={revenueData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {revenueData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {revenueData.map((item) => (
                <div key={item.name} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div 
                      className="h-3 w-3 rounded-full" 
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm text-gray-600">{item.name}</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">{item.value}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Resumen del Mes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Nuevos prospectos</span>
              <span className="text-sm font-medium text-gray-900">{clientesData.prospectos || 34}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Oportunidades abiertas</span>
              <span className="text-sm font-medium text-gray-900">{oportunidadesData.abiertas || 12}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Propuestas enviadas</span>
              <span className="text-sm font-medium text-gray-900">{oportunidadesData.en_propuesta || 8}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Deals cerrados</span>
              <span className="text-sm font-medium text-green-600">{oportunidadesData.cerradas_ganadas || 5}</span>
            </div>
            <hr className="my-4" />
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-900">Total pipeline</span>
              <span className="text-lg font-bold text-green-600">
                ${(oportunidadesData.valor_total_pipeline || 28400).toLocaleString()}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

