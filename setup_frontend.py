import os

files = {
    "apps/viewer-web/package.json": '''{
  "name": "promptcad-viewer",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.92.0",
    "three": "^0.159.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@types/three": "^0.159.0",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.8"
  }
}''',

    "apps/viewer-web/tsconfig.json": '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}''',

    "apps/viewer-web/tsconfig.node.json": '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}''',

    "apps/viewer-web/vite.config.ts": '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
''',

    "apps/viewer-web/index.html": '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PromptCAD</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''',

    "apps/viewer-web/src/main.tsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
''',

    "apps/viewer-web/src/index.css": '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: #1a1a1a;
  color: #fff;
}

#root {
  width: 100vw;
  height: 100vh;
}
''',

    "apps/viewer-web/src/App.tsx": '''import { useState } from 'react'
import EditorPage from './pages/EditorPage'

function App() {
  return <EditorPage />
}

export default App
''',

    "apps/viewer-web/src/pages/EditorPage.tsx": '''import { useState } from 'react'
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
''',

    "apps/viewer-web/src/api/client.ts": '''import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
''',

    "apps/viewer-web/src/api/types.ts": '''export interface DSLDocument {
  version: string
  operations: Operation[]
}

export interface Operation {
  id: string
  type: string
  params?: Record<string, any>
  inputs?: string[]
}

export interface PromptResponse {
  dsl: DSLDocument
  geometry: any
}
''',
}

base_path = r"C:\Users\baris\Downloads\promptcad"
for file_path, content in files.items():
    full_path = os.path.join(base_path, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {file_path}")

print("\nViewer Web frontend created successfully!")
