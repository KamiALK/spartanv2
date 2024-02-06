
import { BrowserRouter,Route,Routes } from 'react-router-dom';
import users from './components/users'

function App() {
 
  return (
    
    <BrowserRouter>
      <Routes>
        <Route path='/' element={users}>
           
        </Route>
      </Routes>
     
    </BrowserRouter>

  )
}

export default App
