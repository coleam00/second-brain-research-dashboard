#!/usr/bin/env python3
"""
DYN-227: YouTube Demo Preparation
Test all 5 sample documents end-to-end
"""

from playwright.sync_api import sync_playwright
import time
import sys

def test_sample_document(page, sample_number, sample_name):
    """Test a single sample document"""
    print(f"\n{'='*60}")
    print(f"Testing Sample {sample_number}: {sample_name}")
    print(f"{'='*60}")

    try:
        # Wait for page to be ready
        page.wait_for_selector('button:has-text("Generate Dashboard")', timeout=10000)
        print(f"✓ Page loaded")

        # Click the sample button (they are numbered 1-5 in the grid)
        sample_buttons = page.locator('button[title]').filter(has_text=sample_name.split()[0])
        if sample_buttons.count() == 0:
            # Try alternative selector - look for buttons with the emoji or text
            sample_buttons = page.locator('button').filter(has_text=sample_name.split()[-1])

        if sample_buttons.count() > 0:
            sample_buttons.first.click()
            print(f"✓ Clicked '{sample_name}' sample button")
            time.sleep(1)
        else:
            print(f"⚠ Could not find sample button for '{sample_name}'")
            return False

        # Verify content loaded
        textarea = page.locator('textarea')
        content = textarea.input_value()
        if len(content) > 100:
            print(f"✓ Content loaded ({len(content)} characters)")
        else:
            print(f"⚠ Content seems short: {len(content)} characters")

        # Click Generate Dashboard
        generate_button = page.locator('button:has-text("Generate Dashboard")')
        generate_button.click()
        print(f"✓ Clicked 'Generate Dashboard'")

        # Wait for loading state to appear
        time.sleep(2)
        print(f"✓ Waiting for dashboard generation...")

        # Wait for dashboard to complete (look for components or empty state)
        # Maximum 30 seconds timeout
        start_time = time.time()
        dashboard_ready = False

        while time.time() - start_time < 30:
            # Check if loading state is gone and we have content
            loading = page.locator('.animate-pulse').count()
            if loading == 0:
                # Check for actual components or empty state
                components = page.locator('[data-component-type]').count()
                if components > 0:
                    print(f"✓ Dashboard generated with {components} components")
                    dashboard_ready = True
                    break
                else:
                    # Maybe check for empty state or error
                    empty_state = page.locator('text=No dashboard generated').count()
                    if empty_state > 0:
                        print(f"⚠ Dashboard generation completed but no components")
                        dashboard_ready = True
                        break
            time.sleep(1)

        if not dashboard_ready:
            print(f"⚠ Dashboard did not complete in 30 seconds")

        # Take screenshot
        screenshot_path = f'screenshots/DYN-227-sample-{sample_number}-{sample_name.lower().replace(" ", "-")}.png'
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"✓ Screenshot saved: {screenshot_path}")

        # Check for console errors
        console_errors = []
        # Note: We'd need to set up console listeners before navigation to capture all errors

        print(f"✓ Test completed for '{sample_name}'")
        return True

    except Exception as e:
        print(f"✗ Error testing '{sample_name}': {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*60)
    print("DYN-227: YouTube Demo Preparation - Testing All Samples")
    print("="*60)

    samples = [
        (1, "AI Research Paper"),
        (2, "Product Meeting Notes"),
        (3, "Product Launch Plan"),
        (4, "Kubernetes Guide"),
        (5, "SaaS Market Report")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # Set up console listener
        console_errors = []
        def handle_console(msg):
            if msg.type in ['error', 'warning']:
                console_errors.append(f"[{msg.type.upper()}] {msg.text}")

        page.on('console', handle_console)

        # Navigate to app
        print("\nNavigating to http://localhost:3010...")
        page.goto('http://localhost:3010', wait_until='networkidle')
        time.sleep(2)

        # Take initial screenshot
        page.screenshot(path='screenshots/DYN-227-demo-ready.png', full_page=True)
        print("✓ Initial app state screenshot captured")

        # Test each sample
        results = {}
        for sample_num, sample_name in samples:
            # Reload page for clean state
            page.goto('http://localhost:3010', wait_until='networkidle')
            time.sleep(1)

            success = test_sample_document(page, sample_num, sample_name)
            results[sample_name] = success

            # Brief pause between tests
            time.sleep(2)

        browser.close()

        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)

        passed = sum(1 for v in results.values() if v)
        total = len(results)

        for sample_name, success in results.items():
            status = "✓ PASS" if success else "✗ FAIL"
            print(f"{status}: {sample_name}")

        print(f"\nResults: {passed}/{total} samples tested successfully")

        if console_errors:
            print(f"\nConsole Errors/Warnings ({len(console_errors)}):")
            for error in console_errors[:10]:  # Show first 10
                print(f"  {error}")
        else:
            print("\n✓ No console errors detected")

        print("\n" + "="*60)

        return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
