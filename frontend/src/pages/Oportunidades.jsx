import { useState } from 'react'
import { 
  Plus, 
  Search, 
  Filter,
  MoreHorizontal,
  Calendar,
  User,
  DollarSign
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import OportunidadModal from '@/components/modals/OportunidadModal'
import ActividadModal from '@/components/modals/ActividadModal'
import '../App.css'

// Datos de ejemplo para las oportunidades
const initialOpportunities = {
  prospecto: [
    {
      id: 1,
      title: 'Consultoría Digital - TechCorp',
      client: 'María González',
      company: 'TechCorp Solutions',
      value: 15000,
      date: '2024-01-15',
      priority: 'high'
    },
    {
      id: 2,
      title: 'Desarrollo Web - StartupXYZ',
      client: 'Carlos Ruiz',
      company: 'StartupXYZ',
      value: 8500,
      date: '2024-01-18',
      priority: 'medium'
    }
  ],
  contactado: [
    {
      id: 3,
      title: 'Marketing Digital - Innovate',
      client: 'Ana Martínez',
      company: 'Innovate Inc',
      value: 12000,
      date: '2024-01-10',
      priority: 'high'
    },
    {
      id: 4,
      title: 'Consultoría IT - Future Tech',
      client: 'Luis Pérez',
      company: 'Future Tech',
      value: 20000,
      date: '2024-01-12',
      priority: 'high'
    }
  ],
  propuesta: [
    {
      id: 5,
      title: 'E-commerce Platform - Digital Ventures',
      client: 'Sofia López',
      company: 'Digital Ventures',
      value: 25000,
      date: '2024-01-08',
      priority: 'high'
    }
  ],
  negociacion: [
    {
      id: 6,
      title: 'CRM Implementation - GlobalCorp',
      client: 'Roberto Silva',
      company: 'GlobalCorp',
      value: 35000,
      date: '2024-01-05',
      priority: 'high'
    }
  ],
  cerrado: [
    {
      id: 7,
      title: 'Website Redesign - LocalBiz',
      client: 'Carmen Torres',
      company: 'LocalBiz',
      value: 7500,
      date: '2024-01-20',
      priority: 'medium'
    }
  ]
}

const columns = [
  { id: 'prospecto', title: 'Prospecto', color: 'bg-gray-100' },
  { id: 'contactado', title: 'Contactado', color: 'bg-blue-100' },
  { id: 'propuesta', title: 'Propuesta', color: 'bg-yellow-100' },
  { id: 'negociacion', title: 'Negociación', color: 'bg-orange-100' },
  { id: 'cerrado', title: 'Cerrado', color: 'bg-green-100' }
]

const getPriorityColor = (priority) => {
  switch (priority) {
    case 'high': return 'bg-red-100 text-red-800'
    case 'medium': return 'bg-yellow-100 text-yellow-800'
    case 'low': return 'bg-green-100 text-green-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

export default function Oportunidades() {
  const [opportunities, setOpportunities] = useState(initialOpportunities)
  const [selectedOpportunity, setSelectedOpportunity] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingOpportunity, setEditingOpportunity] = useState(null)
  const [isActividadModalOpen, setIsActividadModalOpen] = useState(false)
  const [activities, setActivities] = useState([])

  const handleCardClick = (opportunity) => {
    setSelectedOpportunity(opportunity)
  }

  const handleNewOpportunity = () => {
    setEditingOpportunity(null)
    setIsModalOpen(true)
  }

  const handleEditOpportunity = (opportunity) => {
    setEditingOpportunity(opportunity)
    setIsModalOpen(true)
  }

  const handleSaveOpportunity = (opportunityData) => {
    if (editingOpportunity) {
      // Editar oportunidad existente
      const updatedOpportunities = { ...opportunities }
      Object.keys(updatedOpportunities).forEach(status => {
        updatedOpportunities[status] = updatedOpportunities[status].map(opp => 
          opp.id === editingOpportunity.id 
            ? { ...opp, ...opportunityData }
            : opp
        )
      })
      setOpportunities(updatedOpportunities)
    } else {
      // Crear nueva oportunidad
      const newOpportunity = {
        id: Date.now(),
        ...opportunityData
      }
      const status = opportunityData.status || 'prospecto'
      setOpportunities(prev => ({
        ...prev,
        [status]: [...(prev[status] || []), newOpportunity]
      }))
    }
  }

  const handleNewActivity = () => {
    setIsActividadModalOpen(true)
  }

  const handleSaveActivity = (activityData) => {
    const newActivity = {
      id: Date.now(),
      ...activityData
    }
    setActivities(prev => [...prev, newActivity])
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Oportunidades</h1>
          <p className="text-gray-600">Gestiona tu pipeline de ventas</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700" onClick={handleNewOpportunity}>
          <Plus className="h-4 w-4 mr-2" />
          Nueva Oportunidad
        </Button>
      </div>

      {/* Filtros y búsqueda */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Buscar oportunidades..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline">
          <Filter className="h-4 w-4 mr-2" />
          Filtros
        </Button>
      </div>

      {/* Tablero Kanban */}
      <div className="flex space-x-6 overflow-x-auto pb-4">
        {columns.map((column) => (
          <div key={column.id} className="flex-shrink-0 w-80">
            <div className={`rounded-lg p-4 ${column.color}`}>
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-900">{column.title}</h3>
                <Badge variant="secondary">
                  {opportunities[column.id]?.length || 0}
                </Badge>
              </div>
              
              <div className="space-y-3">
                {opportunities[column.id]?.map((opportunity) => (
                  <Card 
                    key={opportunity.id} 
                    className="cursor-pointer hover:shadow-md transition-shadow"
                    onClick={() => handleCardClick(opportunity)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-medium text-gray-900 text-sm leading-tight">
                          {opportunity.title}
                        </h4>
                        <Button variant="ghost" size="icon" className="h-6 w-6">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex items-center text-xs text-gray-600">
                          <User className="h-3 w-3 mr-1" />
                          {opportunity.client}
                        </div>
                        <div className="text-xs text-gray-500">
                          {opportunity.company}
                        </div>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center text-xs text-gray-600">
                            <DollarSign className="h-3 w-3 mr-1" />
                            {formatCurrency(opportunity.value)}
                          </div>
                          <Badge 
                            variant="secondary" 
                            className={`text-xs ${getPriorityColor(opportunity.priority)}`}
                          >
                            {opportunity.priority}
                          </Badge>
                        </div>
                        <div className="flex items-center text-xs text-gray-500">
                          <Calendar className="h-3 w-3 mr-1" />
                          {new Date(opportunity.date).toLocaleDateString('es-ES')}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
                
                {/* Botón para agregar nueva oportunidad en la columna */}
                <Button 
                  variant="ghost" 
                  className="w-full border-2 border-dashed border-gray-300 hover:border-gray-400 h-12"
                  onClick={() => {
                    setEditingOpportunity({ status: column.id })
                    setIsModalOpen(true)
                  }}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Agregar
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Panel de detalles (sidebar) */}
      {selectedOpportunity && (
        <div className="fixed inset-y-0 right-0 z-50 w-96 bg-white shadow-xl border-l border-gray-200">
          <div className="flex h-full flex-col">
            <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
              <h2 className="text-lg font-semibold text-gray-900">
                Detalles de la Oportunidad
              </h2>
              <Button 
                variant="ghost" 
                size="icon"
                onClick={() => setSelectedOpportunity(null)}
              >
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </div>
            
            <div className="flex-1 overflow-y-auto px-6 py-4">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    {selectedOpportunity.title}
                  </h3>
                  <Badge className={getPriorityColor(selectedOpportunity.priority)}>
                    Prioridad {selectedOpportunity.priority}
                  </Badge>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Cliente</label>
                    <p className="text-sm text-gray-900">{selectedOpportunity.client}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-700">Empresa</label>
                    <p className="text-sm text-gray-900">{selectedOpportunity.company}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-700">Valor</label>
                    <p className="text-lg font-semibold text-green-600">
                      {formatCurrency(selectedOpportunity.value)}
                    </p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-700">Fecha</label>
                    <p className="text-sm text-gray-900">
                      {new Date(selectedOpportunity.date).toLocaleDateString('es-ES')}
                    </p>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    Actividades Recientes
                  </label>
                  <div className="space-y-2">
                    <div className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                      Llamada de seguimiento - Hace 2 días
                    </div>
                    <div className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                      Email enviado - Hace 1 semana
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="border-t border-gray-200 px-6 py-4">
              <div className="flex space-x-3">
                <Button 
                  className="flex-1"
                  onClick={() => handleEditOpportunity(selectedOpportunity)}
                >
                  Editar
                </Button>
                <Button 
                  variant="outline" 
                  className="flex-1"
                  onClick={handleNewActivity}
                >
                  Actividad
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal para crear/editar oportunidad */}
      <OportunidadModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        oportunidad={editingOpportunity}
        onSave={handleSaveOpportunity}
      />

      {/* Modal para agregar actividad */}
      <ActividadModal
        isOpen={isActividadModalOpen}
        onClose={() => setIsActividadModalOpen(false)}
        oportunidad={selectedOpportunity}
        onSave={handleSaveActivity}
      />
    </div>
  )
}

