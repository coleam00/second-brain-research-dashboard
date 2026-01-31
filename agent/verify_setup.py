"""Verification script for Python agent setup."""
import sys

print("=" * 60)
print("Python Agent Setup Verification")
print("=" * 60)

print(f"\nPython version: {sys.version}")

# Test imports
try:
    import pydantic_ai
    print(f"✅ pydantic-ai: {pydantic_ai.__version__}")
except ImportError as e:
    print(f"❌ pydantic-ai: {e}")

try:
    import fastapi
    print(f"✅ fastapi: {fastapi.__version__}")
except ImportError as e:
    print(f"❌ fastapi: {e}")

try:
    import uvicorn
    print(f"✅ uvicorn: {uvicorn.__version__}")
except ImportError as e:
    print(f"❌ uvicorn: {e}")

try:
    import httpx
    print(f"✅ httpx: {httpx.__version__}")
except ImportError as e:
    print(f"❌ httpx: {e}")

try:
    import ag_ui
    print(f"✅ ag-ui-protocol: installed")
except ImportError as e:
    print(f"❌ ag-ui-protocol: {e}")

print("\n" + "=" * 60)
print("Setup verification complete!")
print("=" * 60)
