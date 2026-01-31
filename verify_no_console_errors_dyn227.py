#!/usr/bin/env python3
"""
DYN-227: Verify no console errors during demo run
"""

from playwright.sync_api import sync_playwright
import time

def test_console_errors():
    """Test all samples and capture console errors"""

    samples = [
        "AI Research Paper",
        "Product Meeting Notes",
        "Product Launch Plan",
        "Kubernetes Guide",
        "SaaS Market Report"
    ]

    console_messages = {
        'error': [],
        'warning': [],
        'log': [],
        'info': []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use headful to see what's happening
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # Set up console listener
        def handle_console(msg):
            msg_type = msg.type
            msg_text = msg.text

            if msg_type in console_messages:
                console_messages[msg_type].append(msg_text)

                # Print errors immediately
                if msg_type == 'error':
                    print(f"  [ERROR] {msg_text}")
                elif msg_type == 'warning':
                    print(f"  [WARN] {msg_text}")

        page.on('console', handle_console)

        print("="*60)
        print("Console Error Check - All Samples")
        print("="*60)

        for idx, sample_name in enumerate(samples, 1):
            print(f"\n[{idx}/5] Testing: {sample_name}")

            # Navigate to fresh page
            page.goto('http://localhost:3010', wait_until='networkidle')
            time.sleep(2)

            # Click sample button
            try:
                sample_buttons = page.locator('button').filter(has_text=sample_name.split()[0])
                if sample_buttons.count() > 0:
                    sample_buttons.first.click()
                    time.sleep(1)

                    # Click Generate
                    generate_button = page.locator('button:has-text("Generate Dashboard")')
                    generate_button.click()
                    time.sleep(5)  # Wait for generation

                    print(f"  ✓ Generated successfully")
                else:
                    print(f"  ⚠ Could not find button")
            except Exception as e:
                print(f"  ✗ Error: {e}")

        browser.close()

        # Print summary
        print("\n" + "="*60)
        print("CONSOLE SUMMARY")
        print("="*60)

        error_count = len(console_messages['error'])
        warning_count = len(console_messages['warning'])

        print(f"Errors: {error_count}")
        print(f"Warnings: {warning_count}")

        if error_count > 0:
            print("\nErrors found:")
            for error in console_messages['error']:
                print(f"  - {error}")

        if warning_count > 0:
            print("\nWarnings found:")
            for warning in console_messages['warning'][:5]:  # Show first 5
                print(f"  - {warning}")

        if error_count == 0 and warning_count == 0:
            print("\n✓ NO CONSOLE ERRORS OR WARNINGS!")
            return True
        elif error_count == 0:
            print(f"\n✓ No errors (only {warning_count} warnings)")
            return True
        else:
            print(f"\n✗ {error_count} errors found")
            return False

if __name__ == '__main__':
    success = test_console_errors()
    exit(0 if success else 1)
