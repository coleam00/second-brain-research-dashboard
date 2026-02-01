import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { CopilotKit } from '@copilotkit/react-core'
import './index.css'
import App from './App.tsx'
import A2UITestPage from './A2UITestPage.tsx'
import NewsComponentsTestPage from './pages/NewsComponentsTestPage.tsx'
import TestPeopleComponents from './pages/TestPeopleComponents.tsx'
import SummaryComponentsTestPage from './pages/SummaryComponentsTestPage.tsx'
import MediaComponentsTest from './pages/MediaComponentsTest.tsx'
import DataComponentsTest from './pages/DataComponentsTest.tsx'
import ResourceTest from './pages/ResourceTest.tsx'
import A2UIValidatorTest from './pages/A2UIValidatorTest.tsx'
import ComponentShowcase from './pages/ComponentShowcase.tsx'

// Use test pages based on query params (check specific tests first to avoid conflicts)
const USE_SHOWCASE = window.location.search.includes('showcase');
const USE_VALIDATOR_TEST_PAGE = window.location.search.includes('validator-test');
const USE_RESOURCE_TEST_PAGE = window.location.search.includes('resource-test');
const USE_DATA_TEST_PAGE = window.location.search.includes('data-test');
const USE_MEDIA_TEST_PAGE = window.location.search.includes('media-test');
const USE_SUMMARY_TEST_PAGE = window.location.search.includes('summary-test');
const USE_PEOPLE_TEST_PAGE = window.location.search.includes('people-test');
const USE_NEWS_TEST_PAGE = window.location.search.includes('news-test');
const USE_TEST_PAGE = window.location.search === '?test' || window.location.search.startsWith('?test&');

// CopilotKit configuration
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
const COPILOT_CONFIG = {
  publicApiKey: '', // Not needed for self-hosted backend
  runtimeUrl: `${BACKEND_URL}/ag-ui/stream`,
}

console.log('Initializing CopilotKit with backend:', COPILOT_CONFIG.runtimeUrl)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {USE_SHOWCASE ? (
      <ComponentShowcase />
    ) : USE_VALIDATOR_TEST_PAGE ? (
      <A2UIValidatorTest />
    ) : USE_RESOURCE_TEST_PAGE ? (
      <ResourceTest />
    ) : USE_DATA_TEST_PAGE ? (
      <DataComponentsTest />
    ) : USE_MEDIA_TEST_PAGE ? (
      <MediaComponentsTest />
    ) : USE_SUMMARY_TEST_PAGE ? (
      <SummaryComponentsTestPage />
    ) : USE_PEOPLE_TEST_PAGE ? (
      <TestPeopleComponents />
    ) : USE_NEWS_TEST_PAGE ? (
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
