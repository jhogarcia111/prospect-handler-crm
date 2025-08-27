import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function ActividadModal({ isOpen, onClose, oportunidad = null, onSave }) {
  const [formData, setFormData] = useState({
    tipo: '',
    descripcion: '',
    fecha: new Date().toISOString().split('T')[0],
    hora: new Date().toTimeString().slice(0, 5),
    resultado: '',
    proximaAccion: '',
    fechaProximaAccion: ''
  })

  useEffect(() => {
    if (isOpen) {
      setFormData({
        tipo: '',
        descripcion: '',
        fecha: new Date().toISOString().split('T')[0],
        hora: new Date().toTimeString().slice(0, 5),
        resultado: '',
        proximaAccion: '',
        fechaProximaAccion: ''
      })
    }
  }, [isOpen])

  const handleSubmit = (e) => {
    e.preventDefault()
    const actividadData = {
      ...formData,
      oportunidadId: oportunidad?.id,
      clienteNombre: oportunidad?.client,
      empresaNombre: oportunidad?.company,
      fechaCreacion: new Date().toISOString()
    }
    onSave(actividadData)
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
      <Card className="relative z-50 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>
              Nueva Actividad
            </CardTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
          {oportunidad && (
            <div className="text-sm text-gray-600">
              <p><strong>Oportunidad:</strong> {oportunidad.title}</p>
              <p><strong>Cliente:</strong> {oportunidad.client} - {oportunidad.company}</p>
            </div>
          )}
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tipo de actividad
                </label>
                <select
                  name="tipo"
                  value={formData.tipo}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  required
                >
                  <option value="">Seleccionar tipo</option>
                  <option value="llamada">Llamada telefónica</option>
                  <option value="email">Email</option>
                  <option value="reunion">Reunión</option>
                  <option value="presentacion">Presentación</option>
                  <option value="propuesta">Envío de propuesta</option>
                  <option value="seguimiento">Seguimiento</option>
                  <option value="negociacion">Negociación</option>
                  <option value="cierre">Cierre</option>
                  <option value="otro">Otro</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fecha
                </label>
                <Input
                  name="fecha"
                  type="date"
                  value={formData.fecha}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Hora
                </label>
                <Input
                  name="hora"
                  type="time"
                  value={formData.hora}
                  onChange={handleChange}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Resultado
                </label>
                <select
                  name="resultado"
                  value={formData.resultado}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  required
                >
                  <option value="">Seleccionar resultado</option>
                  <option value="exitoso">Exitoso</option>
                  <option value="pendiente">Pendiente</option>
                  <option value="no_contacto">No hubo contacto</option>
                  <option value="rechazado">Rechazado</option>
                  <option value="interesado">Interesado</option>
                  <option value="necesita_tiempo">Necesita tiempo</option>
                  <option value="derivado">Derivado</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Descripción de la actividad
              </label>
              <textarea
                name="descripcion"
                value={formData.descripcion}
                onChange={handleChange}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                placeholder="Describe los detalles de la actividad realizada..."
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Próxima acción
              </label>
              <Input
                name="proximaAccion"
                value={formData.proximaAccion}
                onChange={handleChange}
                placeholder="Ej: Enviar propuesta comercial, Agendar reunión de seguimiento..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fecha de próxima acción
              </label>
              <Input
                name="fechaProximaAccion"
                type="date"
                value={formData.fechaProximaAccion}
                onChange={handleChange}
              />
            </div>

            <div className="flex space-x-3 pt-4">
              <Button type="submit" className="flex-1">
                Guardar Actividad
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

