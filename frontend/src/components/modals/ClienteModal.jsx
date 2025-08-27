import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function ClienteModal({ isOpen, onClose, cliente = null, onSave }) {
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    industry: '',
    email: '',
    phone: '',
    address: '',
    status: 'prospect'
  })

  useEffect(() => {
    if (cliente) {
      setFormData({
        name: cliente.name || '',
        company: cliente.company || '',
        industry: cliente.industry || '',
        email: cliente.email || '',
        phone: cliente.phone || '',
        address: cliente.address || '',
        status: cliente.status || 'prospect'
      })
    } else {
      setFormData({
        name: '',
        company: '',
        industry: '',
        email: '',
        phone: '',
        address: '',
        status: 'prospect'
      })
    }
  }, [cliente, isOpen])

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave(formData)
    onClose()
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-gray-900/80" onClick={onClose} />
      <Card className="relative z-50 w-full max-w-lg mx-4">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>
              {cliente ? 'Editar Cliente' : 'Nuevo Cliente'}
            </CardTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nombre completo
              </label>
              <Input
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Ej: María González"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Empresa
              </label>
              <Input
                name="company"
                value={formData.company}
                onChange={handleChange}
                required
                placeholder="Ej: TechCorp Solutions"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Industria
              </label>
              <select
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                required
              >
                <option value="">Seleccionar industria</option>
                <option value="Tecnología">Tecnología</option>
                <option value="Fintech">Fintech</option>
                <option value="Marketing">Marketing</option>
                <option value="E-commerce">E-commerce</option>
                <option value="Salud">Salud</option>
                <option value="Educación">Educación</option>
                <option value="Manufactura">Manufactura</option>
                <option value="Servicios">Servicios</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <Input
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="Ej: maria@techcorp.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Teléfono
              </label>
              <Input
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="Ej: +1 (555) 123-4567"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Dirección
              </label>
              <Input
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Ej: Madrid, España"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Estado
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                required
              >
                <option value="prospect">Prospecto</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
              </select>
            </div>

            <div className="flex space-x-3 pt-4">
              <Button type="submit" className="flex-1">
                {cliente ? 'Actualizar' : 'Crear'} Cliente
              </Button>
              <Button type="button" variant="outline" onClick={onClose} className="flex-1">
                Cancelar
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

