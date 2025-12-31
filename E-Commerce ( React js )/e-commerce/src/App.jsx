import HomePage from './pages/HomePage'
import Checkout from './pages/Checkout'
import Order from "./pages/Order";
import Tracking from "./pages/Tracking";
import { Routes, Route } from 'react-router'
import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css'

function App() {

  const [cart, setCart] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:3000/api/cart-items").then((response) => {
      setCart(response.data);
    });
  }, []);

  return (
    <Routes>
      <Route index element={<HomePage cart={cart} />} />
      <Route path="checkout" element={<Checkout cart={cart} />} />
      <Route path="order" element={<Order cart={cart} />} />
      <Route path="tracking" element={<Tracking cart={cart} />} />
    </Routes>
  );
}

export default App
