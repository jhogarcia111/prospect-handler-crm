import { useState } from 'react'
import { 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  Calendar,
  Download,
  Filter,
  CreditCard,
  Banknote,
  Wallet
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell,
  LineChart,
  Line,
  Area,
  AreaChart
} from 'recharts'
import '../App.css'

// Datos de ejemplo para los gráficos financieros
const monthlyRevenue = [
  { month: 'Ene', revenue: 18500, expenses: 12000, profit: 6500 },
  { month: 'Feb', revenue: 22000, expenses: 14500, profit: 7500 },
  { month: 'Mar', revenue: 19800, expenses: 13200, profit: 6600 },
  { month: 'Abr', revenue: 28400, expenses: 16800, profit: 11600 },
  { month: 'May', revenue: 35200, expenses: 19500, profit: 15700 },
  { month: 'Jun', revenue: 42100, expenses: 22300, profit: 19800 },
]

const paymentMethods = [
  { name: 'Transferencia', value: 45, amount: 126500, color: '#3b82f6' },
  { name: 'PayPal', value: 30, amount: 84300, color: '#10b981' },
  { name: 'Stripe', value: 15, amount: 42150, color: '#f59e0b' },
  { name: 'Efectivo', value: 10, amount: 28100, color: '#ef4444' },
]

const recentPayments = [
  {
    id: 1,
    client: 'TechCorp Solutions',
    amount: 15000,
    method: 'Transferencia',
    status: 'completed',
    date: '2024-01-20',
    invoice: 'INV-001'
  },
  {
    id: 2,
    client: 'StartupXYZ',
    amount: 8500,
    method: 'PayPal',
    status: 'completed',
    date: '2024-01-19',
    invoice: 'INV-002'
  },
  {
    id: 3,
    client: 'Innovate Inc',
    amount: 12000,
    method: 'Stripe',
    status: 'pending',
    date: '2024-01-18',
    invoice: 'INV-003'
  },
  {
    id: 4,
    client: 'Future Tech',
    amount: 20000,
    method: 'Transferencia',
    status: 'completed',
    date: '2024-01-17',
    invoice: 'INV-004'
  },
  {
    id: 5,
    client: 'Digital Ventures',
    amount: 25000,
    method: 'PayPal',
    status: 'failed',
    date: '2024-01-16',
    invoice: 'INV-005'
  },
]

const getStatusColor = (status) => {
  switch (status) {
    case 'completed': return 'bg-green-100 text-green-800'
    case 'pending': return 'bg-yellow-100 text-yellow-800'
    case 'failed': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'completed': return 'Completado'
    case 'pending': return 'Pendiente'
    case 'failed': return 'Fallido'
    default: return 'Desconocido'
  }
}

const getMethodIcon = (method) => {
  switch (method) {
    case 'Transferencia': return Banknote
    case 'PayPal': return Wallet
    case 'Stripe': return CreditCard
    case 'Efectivo': return DollarSign
    default: return DollarSign
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

export default function Finanzas() {
  const [selectedPeriod, setSelectedPeriod] = useState('6m')

  const totalRevenue = monthlyRevenue.reduce((sum, month) => sum + month.revenue, 0)
  const totalExpenses = monthlyRevenue.reduce((sum, month) => sum + month.expenses, 0)
  const totalProfit = totalRevenue - totalExpenses
  const profitMargin = ((totalProfit / totalRevenue) * 100).toFixed(1)

  const pendingPayments = recentPayments
    .filter(payment => payment.status === 'pending')
    .reduce((sum, payment) => sum + payment.amount, 0)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Finanzas</h1>
          <p className="text-gray-600">Seguimiento de ingresos y pagos</p>
        </div>
        <div className="flex items-center space-x-3">
          <select 
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
          >
            <option value="1m">Último mes</option>
            <option value="3m">Últimos 3 meses</option>
            <option value="6m">Últimos 6 meses</option>
            <option value="1y">Último año</option>
          </select>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Exportar
          </Button>
        </div>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Ingresos Totales
            </CardTitle>
            <DollarSign className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(totalRevenue)}
            </div>
            <p className="text-xs text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +18% desde el período anterior
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Pagos Pendientes
            </CardTitle>
            <Calendar className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(pendingPayments)}
            </div>
            <p className="text-xs text-yellow-600 flex items-center">
              <TrendingDown className="h-3 w-3 mr-1" />
              3 pagos pendientes
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Beneficio Neto
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(totalProfit)}
            </div>
            <p className="text-xs text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              Margen: {profitMargin}%
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Crecimiento Mensual
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-emerald-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">+24.5%</div>
            <p className="text-xs text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              Comparado con el mes anterior
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos principales */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Tendencia de ingresos */}
        <Card>
          <CardHeader>
            <CardTitle>Tendencia de Ingresos</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={monthlyRevenue}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis dataKey="month" />
                <YAxis />
                <Area 
                  type="monotone" 
                  dataKey="revenue" 
                  stroke="#3b82f6" 
                  fill="#3b82f6" 
                  fillOpacity={0.1}
                />
                <Area 
                  type="monotone" 
                  dataKey="profit" 
                  stroke="#10b981" 
                  fill="#10b981" 
                  fillOpacity={0.2}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Métodos de pago */}
        <Card>
          <CardHeader>
            <CardTitle>Métodos de Pago</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={paymentMethods}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {paymentMethods.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {paymentMethods.map((method) => (
                <div key={method.name} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div 
                      className="h-3 w-3 rounded-full" 
                      style={{ backgroundColor: method.color }}
                    />
                    <span className="text-sm text-gray-600">{method.name}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium text-gray-900">
                      {formatCurrency(method.amount)}
                    </div>
                    <div className="text-xs text-gray-500">{method.value}%</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Comparación mensual */}
      <Card>
        <CardHeader>
          <CardTitle>Comparación Mensual</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={monthlyRevenue}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis dataKey="month" />
              <YAxis />
              <Bar dataKey="revenue" fill="#3b82f6" name="Ingresos" radius={[2, 2, 0, 0]} />
              <Bar dataKey="expenses" fill="#ef4444" name="Gastos" radius={[2, 2, 0, 0]} />
              <Bar dataKey="profit" fill="#10b981" name="Beneficio" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Tabla de pagos recientes */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Pagos Recientes</CardTitle>
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Filtrar
            </Button>
          </div>
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
                    Monto
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Método
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Factura
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recentPayments.map((payment) => {
                  const MethodIcon = getMethodIcon(payment.method)
                  return (
                    <tr key={payment.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {payment.client}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-semibold text-gray-900">
                          {formatCurrency(payment.amount)}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          <MethodIcon className="h-4 w-4 text-gray-400" />
                          <span className="text-sm text-gray-900">{payment.method}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Badge className={getStatusColor(payment.status)}>
                          {getStatusText(payment.status)}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(payment.date).toLocaleDateString('es-ES')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 hover:text-blue-800 cursor-pointer">
                        {payment.invoice}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

