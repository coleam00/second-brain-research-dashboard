import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { CopilotKit } from '@copilotkit/react-core'
import './index.css'
import App from './App.tsx'
import A2UITestPage from './A2UITestPage.tsx'
import NewsComponentsTestPage from './pages/NewsComponentsTestPage.tsx'

// Use test pages based on query params
const USE_TEST_PAGE = window.location.search.includes('test');
const USE_NEWS_TEST_PAGE = window.location.search.includes('news-test');

// CopilotKit configuration
const COPILOT_CONFIG = {
  publicApiKey: '', // Not needed for self-hosted backend
  runtimeUrl: 'http://localhost:8000/ag-ui/stream',
}

console.log('Initializing CopilotKit with backend:', COPILOT_CONFIG.runtimeUrl)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {USE_NEWS_TEST_PAGE ? (
      <NewsComponentsTestPage />
    ) : USE_TEST_PAGE ? (
      <A2UITestPage />
    ) : (
      // Temporarily render without CopilotKit to test layout
      // CopilotKit will be re-enabled when backend agent is properly configured
      <App />
    )}
  </StrictMode>,
)
