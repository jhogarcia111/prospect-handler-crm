import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function OportunidadModal({ isOpen, onClose, oportunidad = null, onSave }) {
  const [formData, setFormData] = useState({
    title: '',
    client: '',
    company: '',
    value: '',
    priority: 'medium',
    status: 'prospecto',
    date: new Date().toISOString().split('T')[0]
  })

  useEffect(() => {
    if (oportunidad) {
      setFormData({
        title: oportunidad.title || '',
        client: oportunidad.client || '',
        company: oportunidad.company || '',
        value: oportunidad.value?.toString() || '',
        priority: oportunidad.priority || 'medium',
        status: oportunidad.status || 'prospecto',
        date: oportunidad.date || new Date().toISOString().split('T')[0]
      })
    } else {
      setFormData({
        title: '',
        client: '',
        company: '',
        value: '',
        priority: 'medium',
        status: 'prospecto',
        date: new Date().toISOString().split('T')[0]
      })
    }
  }, [oportunidad, isOpen])

  const handleSubmit = (e) => {
    e.preventDefault()
    const dataToSave = {
      ...formData,
      value: parseFloat(formData.value) || 0
    }
    onSave(dataToSave)
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
              {oportunidad ? 'Editar Oportunidad' : 'Nueva Oportunidad'}
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
                Título de la oportunidad
              </label>
              <Input
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="Ej: Consultoría Digital - TechCorp"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Cliente contacto
              </label>
              <Input
                name="client"
                value={formData.client}
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
                Valor estimado (USD)
              </label>
              <Input
                name="value"
                type="number"
                value={formData.value}
                onChange={handleChange}
                required
                placeholder="Ej: 15000"
                min="0"
                step="0.01"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Prioridad
              </label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                required
              >
                <option value="low">Baja</option>
                <option value="medium">Media</option>
                <option value="high">Alta</option>
              </select>
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
                <option value="prospecto">Prospecto</option>
                <option value="contactado">Contactado</option>
                <option value="propuesta">Propuesta</option>
                <option value="negociacion">Negociación</option>
                <option value="cerrado">Cerrado</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fecha
              </label>
              <Input
                name="date"
                type="date"
                value={formData.date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="flex space-x-3 pt-4">
              <Button type="submit" className="flex-1">
                {oportunidad ? 'Actualizar' : 'Crear'} Oportunidad
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

