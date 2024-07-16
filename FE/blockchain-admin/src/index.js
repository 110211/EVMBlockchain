import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom/client'; // Sử dụng ReactDOM từ 'react-dom/client'
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root')); // Tạo root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
