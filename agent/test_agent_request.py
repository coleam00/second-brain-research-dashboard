"""Test script to send a request to the AG-UI streaming endpoint."""
import httpx
import json
import asyncio

async def test_agent_endpoint():
    """Test the /ag-ui/stream endpoint with sample markdown."""

    sample_markdown = """
# Machine Learning Fundamentals

## Introduction

Machine learning is a subset of artificial intelligence that enables computers to learn from data.

> "The key to artificial intelligence has always been the representation." - Jeff Hawkins

## Key Concepts

### Supervised Learning

In supervised learning, we train models with labeled data.

### Statistics

- 95% accuracy on test set
- 10000 training samples
- 3 different algorithms tested

### Code Example

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## Conclusion

Machine learning continues to evolve and transform industries worldwide.
"""

    url = "http://localhost:8000/ag-ui/stream"
    data = {
        "markdown": sample_markdown,
        "user_id": "test_user"
    }

    print("=" * 60)
    print("Testing AG-UI Stream Endpoint")
    print("=" * 60)
    print(f"\nSending request to: {url}")
    print(f"Markdown length: {len(sample_markdown)} characters\n")

    async with httpx.AsyncClient() as client:
        try:
            async with client.stream('POST', url, json=data, timeout=30.0) as response:
                print(f"Response status: {response.status_code}\n")
                print("Streaming events:")
                print("-" * 60)

                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        event_data = line[6:]  # Remove 'data: ' prefix
                        try:
                            parsed = json.loads(event_data)
                            print(f"Event: {json.dumps(parsed, indent=2)}")
                        except json.JSONDecodeError:
                            print(f"Raw: {event_data}")

                print("-" * 60)
                print("\n✅ Test completed successfully!")

        except httpx.ConnectError:
            print("❌ Could not connect to server. Is it running on port 8000?")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent_endpoint())
