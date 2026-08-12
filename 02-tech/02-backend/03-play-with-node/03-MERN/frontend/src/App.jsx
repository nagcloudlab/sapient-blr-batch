import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

import {
  useEffect,
} from 'react'

function App() {
  const [todos, setTodos] = useState([])
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetch('http://localhost:3000/api/v1/todos', {
      headers: {
        Authorization: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2YTdhYmQzYTg1OGNmNmIwNGFjMzQxODEiLCJmb28iOiJiYXIiLCJpYXQiOjE3ODY0Mjk0MDMsImV4cCI6MTc4NjQzMzAwM30.62lA4R5uw7P5Bbhh1imEEaVKd3BTWYu5z3clNiHLwP8`
      }
    })
      .then((response) => response.json())
      .then((data) => setTodos(data))
      .catch((error) => setMessage(error.message))
  }, [])

  return (
    <div className="container">
      <div>
        <div className="display-1">Todos</div>
        <hr />
        <ul className="list-group">
          {todos.map((todo) => (
            <li className='list-group-item' key={todo.id}>{todo.title}</li>
          ))}
        </ul>
        {message && <div className="alert alert-danger mt-3">{message}</div>}
      </div>
    </div>
  )
}

export default App
