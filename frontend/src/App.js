import logo from './logo.svg';

import './App.css';
import{useEffect,useState} from 'react'

function App() {
  useEffect(() =>{fetch('http://localhost:8000/api/users') 
  .then(res =>res.json())
.then(res =>console.log(res)) },[])
  return (
    <div>
        <h1>hola, soy el frontend</h1>
    </div>
  );
}

export default App;
