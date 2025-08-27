import { useState } from 'react'
import { 
  Plus, 
  Search, 
  Filter,
  MoreHorizontal,
  Mail,
  Phone,
  MapPin,
  Building,
  Edit,
  Trash2,
  Eye
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import ClienteModal from '@/components/modals/ClienteModal'
import '../App.css'

// Datos de ejemplo para los clientes
const initialClients = [
  {
    id: 1,
    name: 'María González',
    company: 'TechCorp Solutions',
    industry: 'Tecnología',
    email: 'maria.gonzalez@techcorp.com',
    phone: '+1 (555) 123-4567',
    address: 'Madrid, España',
    status: 'active',
    lastContact: '2024-01-15',
    opportunities: 3,
    totalValue: 45000
  },
  {
    id: 2,
    name: 'Carlos Ruiz',
    company: 'StartupXYZ',
    industry: 'Fintech',
    email: 'carlos@startupxyz.com',
    phone: '+1 (555) 234-5678',
    address: 'Barcelona, España',
    status: 'active',
    lastContact: '2024-01-18',
    opportunities: 1,
    totalValue: 8500
  },
  {
    id: 3,
    name: 'Ana Martínez',
    company: 'Innovate Inc',
    industry: 'Marketing',
    email: 'ana.martinez@innovate.com',
    phone: '+1 (555) 345-6789',
    address: 'Valencia, España',
    status: 'prospect',
    lastContact: '2024-01-10',
    opportunities: 2,
    totalValue: 22000
  },
  {
    id: 4,
    name: 'Luis Pérez',
    company: 'Future Tech',
    industry: 'Tecnología',
    email: 'luis.perez@futuretech.com',
    phone: '+1 (555) 456-7890',
    address: 'Sevilla, España',
    status: 'active',
    lastContact: '2024-01-12',
    opportunities: 1,
    totalValue: 20000
  },
  {
    id: 5,
    name: 'Sofia López',
    company: 'Digital Ventures',
    industry: 'E-commerce',
    email: 'sofia@digitalventures.com',
    phone: '+1 (555) 567-8901',
    address: 'Bilbao, España',
    status: 'inactive',
    lastContact: '2024-01-08',
    opportunities: 1,
    totalValue: 25000
  }
]

const getStatusColor = (status) => {
  switch (status) {
    case 'active': return 'bg-green-100 text-green-800'
    case 'prospect': return 'bg-blue-100 text-blue-800'
    case 'inactive': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'active': return 'Activo'
    case 'prospect': return 'Prospecto'
    case 'inactive': return 'Inactivo'
    default: return 'Desconocido'
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const getInitials = (name) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase()
}

export default function Clientes() {
  const [clients, setClients] = useState(initialClients)
  const [selectedClient, setSelectedClient] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingClient, setEditingClient] = useState(null)

  const filteredClients = clients.filter(client => {
    const matchesSearch = client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterStatus === 'all' || client.status === filterStatus
    return matchesSearch && matchesFilter
  })

  const handleClientClick = (client) => {
    setSelectedClient(client)
  }

  const handleNewClient = () => {
    setEditingClient(null)
    setIsModalOpen(true)
  }

  const handleEditClient = (client, e) => {
    e.stopPropagation()
    setEditingClient(client)
    setIsModalOpen(true)
  }

  const handleSaveClient = (clientData) => {
    if (editingClient) {
      // Editar cliente existente
      setClients(clients.map(client => 
        client.id === editingClient.id 
          ? { ...client, ...clientData }
          : client
      ))
    } else {
      // Crear nuevo cliente
      const newClient = {
        id: Date.now(),
        ...clientData,
        lastContact: new Date().toISOString().split('T')[0],
        opportunities: 0,
        totalValue: 0
      }
      setClients([...clients, newClient])
    }
  }

  const handleDeleteClient = (clientId, e) => {
    e.stopPropagation()
    if (confirm('¿Estás seguro de que quieres eliminar este cliente?')) {
      setClients(clients.filter(client => client.id !== clientId))
      if (selectedClient && selectedClient.id === clientId) {
        setSelectedClient(null)
      }
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clientes</h1>
          <p className="text-gray-600">Gestiona tu base de datos de clientes</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700" onClick={handleNewClient}>
          <Plus className="h-4 w-4 mr-2" />
          Nuevo Cliente
        </Button>
      </div>

      {/* Filtros y búsqueda */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Buscar clientes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <select 
          className="px-3 py-2 border border-gray-300 rounded-md text-sm"
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
        >
          <option value="all">Todos los estados</option>
          <option value="active">Activos</option>
          <option value="prospect">Prospectos</option>
          <option value="inactive">Inactivos</option>
        </select>
        <Button variant="outline">
          <Filter className="h-4 w-4 mr-2" />
          Más filtros
        </Button>
      </div>

      {/* Estadísticas rápidas */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-gray-900">
              {clients.length}
            </div>
            <p className="text-sm text-gray-600">Total Clientes</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">
              {clients.filter(c => c.status === 'active').length}
            </div>
            <p className="text-sm text-gray-600">Activos</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">
              {clients.filter(c => c.status === 'prospect').length}
            </div>
            <p className="text-sm text-gray-600">Prospectos</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-gray-600">
              {formatCurrency(clients.reduce((sum, c) => sum + c.totalValue, 0))}
            </div>
            <p className="text-sm text-gray-600">Valor Total</p>
          </CardContent>
        </Card>
      </div>

      {/* Lista de clientes */}
      <div className="flex gap-6">
        <div className="flex-1">
          <Card>
            <CardHeader>
              <CardTitle>Lista de Clientes ({filteredClients.length})</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Cliente
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Empresa
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Industria
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Estado
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Oportunidades
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Valor
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Acciones
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredClients.map((client) => (
                      <tr 
                        key={client.id} 
                        className="hover:bg-gray-50 cursor-pointer"
                        onClick={() => handleClientClick(client)}
                      >
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <Avatar className="h-8 w-8">
                              <AvatarFallback className="bg-blue-100 text-blue-600">
                                {getInitials(client.name)}
                              </AvatarFallback>
                            </Avatar>
                            <div className="ml-3">
                              <div className="text-sm font-medium text-gray-900">
                                {client.name}
                              </div>
                              <div className="text-sm text-gray-500">
                                {client.email}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {client.company}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {client.industry}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <Badge className={getStatusColor(client.status)}>
                            {getStatusText(client.status)}
                          </Badge>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {client.opportunities}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-green-600">
                          {formatCurrency(client.totalValue)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <div className="flex items-center justify-end space-x-2">
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              className="h-8 w-8"
                              onClick={(e) => {
                                e.stopPropagation()
                                handleClientClick(client)
                              }}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              className="h-8 w-8"
                              onClick={(e) => handleEditClient(client, e)}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              className="h-8 w-8 text-red-600"
                              onClick={(e) => handleDeleteClient(client.id, e)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Panel de detalles del cliente */}
        {selectedClient && (
          <div className="w-80 flex-shrink-0">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Perfil del Cliente</CardTitle>
                  <Button variant="ghost" size="icon" onClick={() => setSelectedClient(null)}>
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="text-center">
                  <Avatar className="h-16 w-16 mx-auto mb-4">
                    <AvatarFallback className="bg-blue-100 text-blue-600 text-lg">
                      {getInitials(selectedClient.name)}
                    </AvatarFallback>
                  </Avatar>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {selectedClient.name}
                  </h3>
                  <p className="text-gray-600">{selectedClient.company}</p>
                  <Badge className={`mt-2 ${getStatusColor(selectedClient.status)}`}>
                    {getStatusText(selectedClient.status)}
                  </Badge>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Mail className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-900">{selectedClient.email}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Phone className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-900">{selectedClient.phone}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <MapPin className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-900">{selectedClient.address}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Building className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-900">{selectedClient.industry}</span>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h4 className="font-medium text-gray-900 mb-3">Estadísticas</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Oportunidades</span>
                      <span className="text-sm font-medium text-gray-900">
                        {selectedClient.opportunities}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Valor Total</span>
                      <span className="text-sm font-medium text-green-600">
                        {formatCurrency(selectedClient.totalValue)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Último Contacto</span>
                      <span className="text-sm text-gray-900">
                        {new Date(selectedClient.lastContact).toLocaleDateString('es-ES')}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h4 className="font-medium text-gray-900 mb-3">Actividad Reciente</h4>
                  <div className="space-y-2">
                    <div className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                      Reunión programada - Hace 2 días
                    </div>
                    <div className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                      Propuesta enviada - Hace 1 semana
                    </div>
                    <div className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                      Primer contacto - Hace 2 semanas
                    </div>
                  </div>
                </div>

                <div className="flex space-x-2">
                  <Button className="flex-1">
                    Editar
                  </Button>
                  <Button variant="outline" className="flex-1">
                    Contactar
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/* Modal para crear/editar cliente */}
      <ClienteModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        cliente={editingClient}
        onSave={handleSaveClient}
      />
    </div>
  )
}

