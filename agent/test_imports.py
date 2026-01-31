"""Test script to verify all required imports."""
import pydantic_ai
import fastapi
import uvicorn
import httpx

print("✅ All imports successful!")
print(f"pydantic-ai version: {pydantic_ai.__version__}")
print(f"fastapi version: {fastapi.__version__}")
print(f"uvicorn version: {uvicorn.__version__}")
print(f"httpx version: {httpx.__version__}")
