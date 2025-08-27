import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Oportunidades from './pages/Oportunidades'
import Clientes from './pages/Clientes'
import Finanzas from './pages/Finanzas'
import Empleados from './pages/admin/Empleados'
import Servicios from './pages/admin/Servicios'
import './App.css'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/oportunidades" element={<Oportunidades />} />
          <Route path="/clientes" element={<Clientes />} />
          <Route path="/finanzas" element={<Finanzas />} />
          <Route path="/admin/empleados" element={<Empleados />} />
          <Route path="/admin/servicios" element={<Servicios />} />
          <Route path="/admin/industrias" element={<div className="p-6"><h1 className="text-2xl font-bold">Industrias</h1><p className="text-gray-600">Página en desarrollo...</p></div>} />
          <Route path="/admin/fuentes" element={<div className="p-6"><h1 className="text-2xl font-bold">Fuentes</h1><p className="text-gray-600">Página en desarrollo...</p></div>} />
          <Route path="/admin/plataformas" element={<div className="p-6"><h1 className="text-2xl font-bold">Plataformas</h1><p className="text-gray-600">Página en desarrollo...</p></div>} />
          <Route path="/admin/actividades" element={<div className="p-6"><h1 className="text-2xl font-bold">Actividades</h1><p className="text-gray-600">Página en desarrollo...</p></div>} />
          <Route path="/admin/resultados" element={<div className="p-6"><h1 className="text-2xl font-bold">Resultados</h1><p className="text-gray-600">Página en desarrollo...</p></div>} />
          <Route path="/admin/medios-pago" element={<div className="p-6"><h1 className="text-2xl font-bold">Medios de Pago</h1><p className="text-gray-600">Página en desarrollo...</p></div>} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

