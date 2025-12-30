import HomePage from './pages/HomePage'
import Checkout from './pages/Checkout'
import Order from "./pages/Order";
import Tracking from "./pages/Tracking";
import { Routes, Route } from 'react-router'
import './App.css'

function App() {
  return (
    <Routes>
      <Route index element={<HomePage />} />
      <Route path="checkout" element={<Checkout />} />
      <Route path="order" element={<Order />} />
      <Route path="tracking" element={<Tracking />} />
    </Routes>
  );
}

export default App
