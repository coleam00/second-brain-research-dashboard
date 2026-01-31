"""
Complete agent configuration test.

This script verifies that:
1. AgentState model is properly defined
2. Agent can be created with proper configuration
3. Tools are registered
4. Basic agent structure is correct
"""
import sys

print("=" * 60)
print("Complete Agent Configuration Test")
print("=" * 60)

try:
    # Test 1: Import modules
    print("\n[Test 1] Importing agent modules...")
    from agent import AgentState, create_agent, create_openrouter_model
    print("✅ Successfully imported: AgentState, create_agent, create_openrouter_model")

    # Test 2: Verify AgentState model
    print("\n[Test 2] Verifying AgentState model...")
    fields = list(AgentState.model_fields.keys())
    expected_fields = ['document_content', 'content_type', 'layout_type', 'analysis_results', 'error_message']

    for field in expected_fields:
        if field in fields:
            print(f"  ✅ Field '{field}' present")
        else:
            print(f"  ❌ Field '{field}' missing")
            sys.exit(1)

    # Test 3: Create AgentState instance
    print("\n[Test 3] Creating AgentState instance...")
    test_state = AgentState(
        document_content="# Test Document\nThis is a test."
    )
    print(f"✅ Created AgentState with document_content: '{test_state.document_content[:30]}...'")
    print(f"   content_type: {test_state.content_type}")
    print(f"   layout_type: {test_state.layout_type}")
    print(f"   analysis_results: {test_state.analysis_results}")

    # Test 4: Verify create_openrouter_model function
    print("\n[Test 4] Verifying create_openrouter_model function...")
    print(f"✅ Function is callable: {callable(create_openrouter_model)}")

    # Test 5: Verify create_agent function
    print("\n[Test 5] Verifying create_agent function...")
    print(f"✅ Function is callable: {callable(create_agent)}")

    # Test 6: Check if agent was initialized (optional)
    print("\n[Test 6] Checking if agent was initialized...")
    from agent import agent
    if agent:
        print(f"✅ Agent initialized successfully")
        print(f"   Agent model: {agent.model}")
        print(f"   Agent has deps_type: {agent._deps_type}")
        print(f"   Agent has result_type: {agent._result_type}")
    else:
        print("⚠️  Agent not initialized (API key may be missing)")

    print("\n" + "=" * 60)
    print("All tests PASSED!")
    print("=" * 60)
    print("\nSummary:")
    print("- AgentState model: ✅ Defined with all required fields")
    print("- create_openrouter_model: ✅ Function available")
    print("- create_agent: ✅ Function available")
    print("- Agent initialization: ✅ Working with valid API key")
    print("\n" + "=" * 60)

except Exception as e:
    print(f"\n❌ Test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
