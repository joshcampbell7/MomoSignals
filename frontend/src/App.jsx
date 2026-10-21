import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    const url = message.trim()
    if (!url) return

    try {
      const response = await fetch('http://127.0.0.1:8000/momo-signals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      })
      const body = await response.json()
      console.log(body.output ?? body)
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <form className="composer" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        placeholder="Paste a Valorant Polymarket link"
        aria-label="Polymarket link"
      />
      <button type="submit" disabled={!message.trim()}>
        Send
      </button>
    </form>
  )
}

export default App
