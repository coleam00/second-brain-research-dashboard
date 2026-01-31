"""Test script to verify agent import and initialization."""
import sys

print("=" * 60)
print("Agent Import Test")
print("=" * 60)

try:
    from agent import agent, AgentState, create_openrouter_model
    print("✅ Agent module imported successfully")

    if agent:
        print(f"   Agent model: {agent.model}")
    else:
        print("   Agent: Not initialized (API key missing)")

    print(f"   AgentState fields: {list(AgentState.model_fields.keys())}")

    # Test creating a basic state
    test_state = AgentState(document_content="# Test\nThis is a test.")
    print(f"✅ AgentState instance created: {test_state.document_content[:20]}...")

    # Test that create_openrouter_model function exists
    print(f"✅ create_openrouter_model function available: {callable(create_openrouter_model)}")

    print("\n" + "=" * 60)
    print("Agent configuration test PASSED")
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
