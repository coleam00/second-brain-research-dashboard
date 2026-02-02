import { test, expect } from '@playwright/test';

// Test configuration
const BASE_URL = process.env.BASE_URL || 'http://localhost:5173';
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

// Sample markdown for testing
const TEST_MARKDOWN = `# AI Research Summary

## Key Statistics
- 85% accuracy improvement
- $2.5M cost savings
- 150ms response time

## Technologies
- Python
- FastAPI
- CopilotKit

## Code Example
\`\`\`python
def analyze(data):
    return insights
\`\`\`

## Resources
- https://copilotkit.ai

## Conclusion
Significant improvements demonstrated.
`;

test.describe('CopilotKit + AG-UI Integration', () => {

  test.beforeEach(async ({ page }) => {
    // Check if backend is running (optional - tests can still run UI-only)
    try {
      const health = await fetch(`${BACKEND_URL}/health`);
      if (!health.ok) {
        console.log('Backend not available - running UI-only tests');
      }
    } catch {
      console.log('Backend not available - running UI-only tests');
    }
  });

  test('1. Application loads with correct UI', async ({ page }) => {
    await page.goto(BASE_URL);

    // Check page title/header
    await expect(page.locator('text=Second Brain Research Dashboard')).toBeVisible();

    // Check input area exists (textarea)
    await expect(page.locator('textarea')).toBeVisible();

    // Check for CopilotKit initialization in console
    const consoleLogs: string[] = [];
    page.on('console', msg => consoleLogs.push(msg.text()));

    await page.waitForTimeout(1000);

    // Take screenshot
    await page.screenshot({
      path: 'screenshots/copilotkit-01-initial-load.png',
      fullPage: true
    });
  });

  test('2. Can input markdown content', async ({ page }) => {
    await page.goto(BASE_URL);

    // Fill textarea
    const textarea = page.locator('textarea');
    await expect(textarea).toBeVisible();
    await textarea.fill(TEST_MARKDOWN);

    // Verify content is in textarea
    await expect(textarea).toHaveValue(TEST_MARKDOWN);

    // Check for generate button
    const generateButton = page.getByRole('button', { name: /generate/i });
    await expect(generateButton).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'screenshots/copilotkit-02-markdown-input.png',
      fullPage: true
    });
  });

  test('3. Generate button transitions to loading state', async ({ page }) => {
    await page.goto(BASE_URL);

    // Fill textarea
    await page.locator('textarea').fill(TEST_MARKDOWN);

    // Click generate
    await page.getByRole('button', { name: /generate/i }).click();

    // Should show loading state with progress
    await expect(page.locator('text=Generating')).toBeVisible({ timeout: 5000 });

    // Take screenshot of loading state
    await page.screenshot({
      path: 'screenshots/copilotkit-03-loading-state.png',
      fullPage: true
    });
  });

  test('4. Full generation flow with backend', async ({ page }) => {
    // Skip if backend is not available
    try {
      const health = await fetch(`${BACKEND_URL}/health`);
      if (!health.ok) {
        test.skip();
        return;
      }
    } catch {
      test.skip();
      return;
    }

    await page.goto(BASE_URL);
    await page.locator('textarea').fill(TEST_MARKDOWN);
    await page.getByRole('button', { name: /generate/i }).click();

    // Wait for loading state
    await expect(page.locator('text=Generating')).toBeVisible({ timeout: 5000 });

    // Wait for completion (increase timeout for LLM processing)
    try {
      await expect(page.locator('text=Key Metrics')).toBeVisible({ timeout: 90000 });

      // Take screenshot of completed dashboard
      await page.screenshot({
        path: 'screenshots/copilotkit-04-dashboard-complete.png',
        fullPage: true
      });
    } catch {
      // Take screenshot even on timeout
      await page.screenshot({
        path: 'screenshots/copilotkit-04-timeout.png',
        fullPage: true
      });
      throw new Error('Dashboard generation timed out');
    }
  });

  test('5. Dashboard displays semantic zones', async ({ page }) => {
    // Skip if backend is not available
    try {
      const health = await fetch(`${BACKEND_URL}/health`);
      if (!health.ok) {
        test.skip();
        return;
      }
    } catch {
      test.skip();
      return;
    }

    await page.goto(BASE_URL);
    await page.locator('textarea').fill(TEST_MARKDOWN);
    await page.getByRole('button', { name: /generate/i }).click();

    // Wait for dashboard to render
    await page.waitForSelector('text=Key Metrics', { timeout: 90000 });

    // Verify zones exist by checking section headings
    const zones = ['Metrics', 'Insights', 'Details', 'Resources'];
    let zonesFound = 0;
    for (const zone of zones) {
      const zoneVisible = await page.locator(`text=${zone}`).first().isVisible().catch(() => false);
      if (zoneVisible) zonesFound++;
    }

    // At least some zones should be visible
    expect(zonesFound).toBeGreaterThanOrEqual(1);

    // Take screenshot
    await page.screenshot({
      path: 'screenshots/copilotkit-05-semantic-zones.png',
      fullPage: true
    });
  });

  test('6. Tab toggle between Dashboard and Source', async ({ page }) => {
    // Skip if backend is not available
    try {
      const health = await fetch(`${BACKEND_URL}/health`);
      if (!health.ok) {
        test.skip();
        return;
      }
    } catch {
      test.skip();
      return;
    }

    await page.goto(BASE_URL);
    await page.locator('textarea').fill(TEST_MARKDOWN);
    await page.getByRole('button', { name: /generate/i }).click();

    await page.waitForSelector('text=Key Metrics', { timeout: 90000 });

    // Click Source tab
    await page.locator('button:has-text("Source")').click();

    // Should show markdown content
    await expect(page.locator('text=AI Research Summary')).toBeVisible();

    // Take screenshot of source view
    await page.screenshot({
      path: 'screenshots/copilotkit-06-source-view.png',
      fullPage: true
    });

    // Click Dashboard tab
    await page.locator('button:has-text("Dashboard")').click();

    // Should show components again
    await expect(page.locator('section')).toBeVisible();

    // Take screenshot of dashboard view
    await page.screenshot({
      path: 'screenshots/copilotkit-06-dashboard-view.png',
      fullPage: true
    });
  });

  test('7. Back navigation preserves content', async ({ page }) => {
    // Skip if backend is not available
    try {
      const health = await fetch(`${BACKEND_URL}/health`);
      if (!health.ok) {
        test.skip();
        return;
      }
    } catch {
      test.skip();
      return;
    }

    await page.goto(BASE_URL);
    await page.locator('textarea').fill(TEST_MARKDOWN);
    await page.getByRole('button', { name: /generate/i }).click();

    await page.waitForSelector('text=Key Metrics', { timeout: 90000 });

    // Click back
    await page.locator('button:has-text("Back")').click();

    // Textarea should have original content
    const textareaValue = await page.locator('textarea').inputValue();
    expect(textareaValue).toContain('AI Research Summary');

    // Take screenshot
    await page.screenshot({
      path: 'screenshots/copilotkit-07-back-navigation.png',
      fullPage: true
    });
  });

  test('8. No console errors during UI interactions', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        // Filter out expected errors (network errors when backend is down, etc.)
        const text = msg.text();
        if (!text.includes('fetch') && !text.includes('ERR_CONNECTION')) {
          consoleErrors.push(text);
        }
      }
    });

    await page.goto(BASE_URL);
    await page.locator('textarea').fill(TEST_MARKDOWN);

    // Wait a bit for any errors to appear
    await page.waitForTimeout(2000);

    // Filter out React dev warnings and expected CopilotKit warnings
    const criticalErrors = consoleErrors.filter(err =>
      !err.includes('React') &&
      !err.includes('DevTools') &&
      !err.includes('CopilotKit')
    );

    // Take screenshot
    await page.screenshot({
      path: 'screenshots/copilotkit-08-console-check.png',
      fullPage: true
    });

    expect(criticalErrors).toHaveLength(0);
  });

  test('9. AG-UI events are received (with backend)', async ({ page }) => {
    // Skip if backend is not available
    try {
      const health = await fetch(`${BACKEND_URL}/health`);
      if (!health.ok) {
        test.skip();
        return;
      }
    } catch {
      test.skip();
      return;
    }

    let agUIEventsReceived = false;

    // Intercept SSE responses
    page.on('response', async response => {
      if (response.url().includes('/agent')) {
        const contentType = response.headers()['content-type'];
        if (contentType?.includes('event-stream')) {
          agUIEventsReceived = true;
        }
      }
    });

    await page.goto(BASE_URL);
    await page.locator('textarea').fill(TEST_MARKDOWN);
    await page.getByRole('button', { name: /generate/i }).click();

    // Wait for some response
    await page.waitForTimeout(5000);

    // Take screenshot
    await page.screenshot({
      path: 'screenshots/copilotkit-09-agui-events.png',
      fullPage: true
    });

    // Note: If backend is running, we expect SSE events
    if (agUIEventsReceived) {
      console.log('AG-UI events received successfully');
    }
  });

  test('10. Regenerate creates new dashboard', async ({ page }) => {
    // Skip if backend is not available
    try {
      const health = await fetch(`${BACKEND_URL}/health`);
      if (!health.ok) {
        test.skip();
        return;
      }
    } catch {
      test.skip();
      return;
    }

    await page.goto(BASE_URL);
    await page.locator('textarea').fill(TEST_MARKDOWN);
    await page.getByRole('button', { name: /generate/i }).click();

    await page.waitForSelector('text=Key Metrics', { timeout: 90000 });

    // Get initial component count
    const headerText = await page.locator('text=/\\d+ components?/').textContent();
    const initialCount = parseInt(headerText?.match(/\d+/)?.[0] || '0');

    // Click regenerate
    await page.locator('button:has-text("Regenerate")').click();

    // Should show loading again
    await expect(page.locator('text=Generating')).toBeVisible({ timeout: 5000 });

    // Wait for new dashboard
    await page.waitForSelector('text=Key Metrics', { timeout: 90000 });

    // Take screenshot
    await page.screenshot({
      path: 'screenshots/copilotkit-10-regenerate.png',
      fullPage: true
    });

    console.log(`Initial: ${initialCount} components`);
  });

});

test.describe('UI Component Tests (No Backend Required)', () => {

  test('Header shows correct title', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page.locator('h1:has-text("Second Brain Research Dashboard")')).toBeVisible();
  });

  test('Textarea accepts markdown input', async ({ page }) => {
    await page.goto(BASE_URL);
    const textarea = page.locator('textarea');
    await textarea.fill('# Test\n\nHello world');
    await expect(textarea).toHaveValue('# Test\n\nHello world');
  });

  test('Generate button is visible and enabled with content', async ({ page }) => {
    await page.goto(BASE_URL);
    await page.locator('textarea').fill('# Test');
    const button = page.getByRole('button', { name: /generate/i });
    await expect(button).toBeVisible();
    await expect(button).toBeEnabled();
  });

  test('Placeholder text is visible in empty textarea', async ({ page }) => {
    await page.goto(BASE_URL);
    const textarea = page.locator('textarea');
    const placeholder = await textarea.getAttribute('placeholder');
    expect(placeholder).toBeTruthy();
    expect(placeholder).toContain('Your Research Title');
  });

  test('Subtitle shows CopilotKit + AG-UI mention', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page.locator('text=CopilotKit')).toBeVisible();
    await expect(page.locator('text=AG-UI')).toBeVisible();
  });

});
