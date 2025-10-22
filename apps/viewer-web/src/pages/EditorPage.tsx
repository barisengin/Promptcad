import { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Box } from '@react-three/drei'
import axios from 'axios'

export default function EditorPage() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [geometry, setGeometry] = useState<any>(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      const response = await axios.post('/api/prompt', { prompt })
      setGeometry(response.data.geometry)
    } catch (err) {
      setError('Failed to generate model: ' + (err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ width: '300px', padding: '20px', background: '#2a2a2a' }}>
        <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>PromptCAD</h1>
        
        <form onSubmit={handleSubmit}>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your 3D model..."
            style={{
              width: '100%',
              height: '150px',
              padding: '10px',
              background: '#1a1a1a',
              border: '1px solid #444',
              color: '#fff',
              borderRadius: '4px',
              marginBottom: '10px',
            }}
          />
          
          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '10px',
              background: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Generating...' : 'Generate Model'}
          </button>
        </form>
        
        {error && (
          <div style={{ color: '#ff6b6b', marginTop: '10px', fontSize: '14px' }}>
            {error}
          </div>
        )}
        
        {geometry && (
          <div style={{ marginTop: '20px', fontSize: '12px', color: '#aaa' }}>
            <pre>{JSON.stringify(geometry, null, 2)}</pre>
          </div>
        )}
      </div>
      
      <div style={{ flex: 1 }}>
        <Canvas camera={{ position: [5, 5, 5] }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Box args={[1, 1, 1]}>
            <meshStandardMaterial color="orange" />
          </Box>
          <OrbitControls />
          <gridHelper args={[10, 10]} />
        </Canvas>
      </div>
    </div>
  )
}
