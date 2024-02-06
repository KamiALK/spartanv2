import React from 'react'
import { useForm } from 'react-hook-form'

function App() {
  const{register,handleSubmit,formState:{errors},watch,reset}=useForm()

  const onSubmit = handleSubmit((data)=>
    {
      // alert('se esta enviadando');
      console.log(data);
      
      
      reset();

    })
  return (
    <form  onSubmit={onSubmit}>

      {/*username*/}
      <label htmlFor='username'>username</label>
      <input type="text" {...register("username",{
        required:{value:true,message:"username requerido"},
        minLength:{value:2,message:"tiene que ser mas largo el name"},
        maxLength:{value:20 ,message:"el valor supero el lorgo maximo"}
      })}/>
      {errors.username &&<span>{errors.username.message}</span>}
      

      {/*nombre*/}
      <label htmlFor='nombre'>Nombre</label>
      <input type="text" {...register("nombre",{
        required:{value:true,message:"nombre requerido"},
        minLength:{value:2,message:"tiene que ser mas largo el name"},
        maxLength:{value:20 ,message:"el valor supero el lorgo maximo"}
        })}/>
      {errors.nombre &&<span>{errors.nombre.message}</span>}

      {/*apellido*/}
      <label htmlFor='apellido'>apellido</label>
      <input type="text" {...register("apellido",{
        required:{value:true,message:"apellido requerido"},
        minLength:{value:2,message:"tiene que ser mas largo el name"},
        maxLength:{value:20 ,message:"el valor supero el lorgo maximo"}
        })}/>
      {errors.apellido &&<span>{errors.apellido.message}</span>}

      {/*celular */}
      <label htmlFor='celular'>celular</label>
      <input type="number" {...register("celular",{
        required:{value:true,message:"celular requerido"},
        minLength:{value:2,message:"tiene que ser mas largo el celular"},
        maxLength:{value:20 ,message:"el valor supero el lorgo maximo"}
      })}/>
      {errors.celular &&<span>{errors.celular.message}</span>}

      {/*edad*/}
      <label htmlFor='edad'>edad</label>
      <input type="number" {...register("edad",{
        required:{value:true,message:"edad requerida"},
        maxLength:{value:2 ,message:"el valor supero el lorgo maximo"}        
      })}/>
      {errors.edad &&<span>{errors.edad.message}</span>}

      {/*cedula*/}
      <label htmlFor='cedula'>cedula</label>
      <input type="number" {...register("cedula",{
        required:{value:true,message:"cedula requerido"},
        minLength:{value:7,message:"tiene que ser mas largo el documento"},
        maxLength:{value:20 ,message:"el valor supero el largo maximo"}        
      })}/>
      {errors.cedula &&<span>{errors.cedula.message}</span>}

      {/*genero*/}
      <label htmlFor='genero'>Genero</label>
      <select {...register("genero",{
        required:{value:true,message:"Gender requerido"},
        // minLength:{value:2,message:"tiene que ser mas largo el name"},
        // maxLength:{value:20 ,message:"el valor supero el lorgo maximo"}        
      })}>
        <option value="masculino">Masculino</option>
        <option value="femenino">Femenino</option>
      </select>
      {errors.genero &&<span>Casilla de genero no esta marcada</span>}
      

      {/*email*/}
      <label htmlFor='email'>email</label>
      <input type="text" {...register("email",{
        required:{value:true,message:"email requerido"},
        pattern:{value:/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,message:"Email inválido"}
      })}/>
      {errors.email &&<span>{errors.email.message}</span>}

      {/*password*/}
      <label htmlFor='password'>Password</label>
      <input type="password" {...register("password",{
        required:{value:true,message:"contraseña requerido"},
        minLength:{value:8,message:"contraseña debe tener minimo 8 caracteres"}        
      })}/>
      {errors.password&&<span>{errors.password.message}</span>}


      {/*confirmarPassword*/}
      <label htmlFor='confirmarpassword'>Confirmar password</label>
      <input type="password" {...register("confirmarpassword",{
        required:{value:true,message:"confirmar contraseña requerido"},
        validate:(value)=>{value===watch('password') || 'las contraseñas no coinciden'}
        })}/>
      {errors.confirmarpassword &&<span>es necesario confirmar la contraseña</span>}
      

      {/*fechaNacimiento*/}
      {/* <label htmlFor='fechaNacimiento'>Fecha de Nacimiento</label>
      <input type='date'{...register("fechaNacimiento",{
        required:{value:true,message:"Fecha de nacimiento requerido"},
        validate:(value)=>{
          const fechaNacimiento = new Date(value)
          const fechaActual =new Date()
          const edad=fechaActual.getFullYear()-fechaNacimiento.getFullYear()
          return edad >= 18 || "debe ser mayor de edad"}
      })}/>   
      {errors.fechaNacimiento &&<span>{errors.fechaNacimiento.message}</span>} */}


      {/*file */}
      {/* <label htmlFor="file">foto de perfil</label>
      <input type="file"{...register("file")}/> */}

      
      {/*terminos */}
      {/* <label htmlFor="terminos">acepto terminos y condiciones</label>
      <input type="checkbox" {...register("terminos")}/> */}


      <button>
        Enviar
      </button>
      <pre>
        {JSON.stringify(watch(),null,2)}
      </pre>
    </form>
  )
}

export default App