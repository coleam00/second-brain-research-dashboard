import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { CopilotKit } from '@copilotkit/react-core'
import './index.css'
import App from './App.tsx'

// CopilotKit configuration
const COPILOT_CONFIG = {
  publicApiKey: '', // Not needed for self-hosted backend
  runtimeUrl: 'http://localhost:8000/ag-ui/stream',
}

console.log('Initializing CopilotKit with backend:', COPILOT_CONFIG.runtimeUrl)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <CopilotKit runtimeUrl={COPILOT_CONFIG.runtimeUrl}>
      <App />
    </CopilotKit>
  </StrictMode>,
)
