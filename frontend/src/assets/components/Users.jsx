import React, {useEffect,useState}from 'react';
import axios from 'axios';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { show_alerta } from '../../funtions';

const users = () => {
  
  const url='http://127.0.0.1/api/users/';
  const[Users,setUsers]=useState('[]')  ;
  const[username,setUsername]=useState('')  ;
  const[nombre,setNombre]=useState('')  ;
  const[apellido,setApellido]=useState('')  ;
  const[celular,setCelular]=useState('')  ;
  const[edad,setEdad]=useState('')  ;
  const[cedula,setCedula]=useState('')  ;
  const[genero,setGenero]=useState('')  ;
  const[email,setEmail]=useState('')  ;
  const[passwd,setPasswd]=useState('')  ;
  const[Id,setId]=useState('')  ;
  const[operation,setOperation]=useState('')  ;
  const[title,setTitle]=useState('')  ;

  useEffect(  
      async ()=>{
      const respuesta= await axios.get(url);
      setUsers(respuesta.data);
      }


  )

  return (
    <div className='app'>
      <div className='container-fluid'>
        <div className='row mt-3'>
          <div className='col-md-4 offset-4'>
            <div className='d-grid mx-auto'>
              <button className='btn btn-dark'data-bs-toggle='modal' data-bs-target='#modalUsers'>
                <i className='fa-solid fa-circle-plus'></i> Agregar
              </button>
            </div>
          </div>
          <div className='row mt-3'>
          <div className='col-12 col-lg-8 offset-0 offset-lg-12'>
            <div className='table-responsible'>
              <table className='table table-bordered'>
                <thead>
                  <tr><th>#</th><th>username</th><th>celualar</th><th>genero</th><th></th></tr>
                </thead>
              </table>
            </div>
          </div>  
        </div>
      </div>
    </div>
    

  )
}

export default users
