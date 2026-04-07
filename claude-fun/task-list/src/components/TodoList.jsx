import { useState } from 'react'

export default function TodoList() {
  const [tasks, setTasks] = useState([])
  const [input, setInput] = useState('')

  function addTask() {
    const text = input.trim()
    if (!text) return
    setTasks([...tasks, { id: Date.now(), text, completed: false }])
    setInput('')
  }

  function toggleTask(id) {
    setTasks(tasks.map(t => t.id === id ? { ...t, completed: !t.completed } : t))
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') addTask()
  }

  return (
    <>
      <div className="todo-form">
        <input
          type="text"
          placeholder="Add a new task..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={addTask}>Add</button>
      </div>

      {tasks.length === 0 ? (
        <p className="empty-state">No tasks yet. Add one above!</p>
      ) : (
        <ul className="todo-list">
          {tasks.map(task => (
            <li
              key={task.id}
              className={`task-item${task.completed ? ' completed' : ''}`}
              onClick={() => toggleTask(task.id)}
            >
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleTask(task.id)}
                onClick={e => e.stopPropagation()}
              />
              <span>{task.text}</span>
            </li>
          ))}
        </ul>
      )}
    </>
  )
}
