# Building Agentic AI Workflows: A Comprehensive Tutorial

*Level: Intermediate to Advanced | Est. Time: 3-4 hours*

## Table of Contents

1. [Introduction to Agentic AI](#introduction)
2. [Prerequisites](#prerequisites)
3. [Understanding Agentic Workflows](#understanding-agentic-workflows)
4. [Setting Up Your Environment](#setup)
5. [Building Your First Agent](#first-agent)
6. [Advanced Agent Patterns](#advanced-patterns)
7. [Real-World Applications](#applications)
8. [Troubleshooting & Best Practices](#troubleshooting)
9. [Next Steps](#next-steps)

---

## Introduction to Agentic AI

**What are Agentic AI Workflows?**

Agentic AI represents a paradigm shift from traditional chatbots to autonomous systems capable of:
- Making decisions independently
- Using tools and APIs
- Breaking down complex tasks into steps
- Learning from feedback
- Collaborating with other agents

**Why Build Agentic Workflows?**

Traditional AI assistants respond to prompts. Agentic AI **takes action**:

| Traditional AI | Agentic AI |
|----------------|------------|
| Answers questions | Completes tasks |
| Provides information | Executes workflows |
| Single interaction | Multi-step processes |
| Requires explicit instructions | Plans independently |
| No tool usage | Uses external tools |

**Real-World Example:**

*Traditional:* "How do I deploy my app?"
→ AI provides deployment instructions

*Agentic:* "Deploy my app to production"
→ AI runs tests, builds container, deploys to cloud, monitors health, sends confirmation

---

## Prerequisites

### Required Knowledge

✅ **Essential:**
- Python programming (intermediate level)
- Basic understanding of APIs
- Familiarity with LLMs (GPT, Claude, etc.)
- Command line basics

✅ **Helpful:**
- REST API design
- Async programming in Python
- Docker basics
- Cloud platforms (AWS, GCP, Azure)

### Required Software

```bash
# Python 3.10 or higher
python --version  # Should be 3.10+

# pip package manager
pip --version

# Git for version control
git --version

# Optional: Docker for containerization
docker --version
```

### Accounts Needed

- OpenAI API key (or Anthropic, Google, etc.)
- GitHub account
- Cloud provider account (optional for deployment)

---

## Understanding Agentic Workflows

### Core Concepts

#### 1. Agents

An **agent** is an AI system that can:
- Perceive its environment
- Make decisions
- Take actions
- Work toward goals

```python
class Agent:
    def __init__(self, name, tools, llm):
        self.name = name
        self.tools = tools  # Available tools
        self.llm = llm      # Language model
        self.memory = []    # Conversation history

    def run(self, task):
        """Execute a task autonomously"""
        while not task.is_complete():
            # Perceive: Understand current state
            state = task.get_state()

            # Decide: Choose next action
            action = self.llm.decide(state, self.tools)

            # Act: Execute the action
            result = self.execute(action)

            # Learn: Update memory
            self.memory.append((action, result))

        return task.result()
```

#### 2. Tools

**Tools** are functions agents can call to interact with the world:

```python
# Example: Web search tool
def web_search(query: str) -> str:
    """Search the web and return results"""
    results = search_api.query(query)
    return format_results(results)

# Example: File write tool
def write_file(path: str, content: str) -> bool:
    """Write content to a file"""
    with open(path, 'w') as f:
        f.write(content)
    return True

# Example: API call tool
def call_api(endpoint: str, data: dict) -> dict:
    """Make an API request"""
    response = requests.post(endpoint, json=data)
    return response.json()
```

#### 3. Planning

Agents break complex tasks into steps:

```
User Task: "Create a blog post about AI and publish it"

Agent Plan:
1. Research AI trends (use web_search)
2. Generate outline (use LLM)
3. Write content (use LLM)
4. Create images (use image_gen)
5. Format as HTML (use formatter)
6. Publish to CMS (use cms_api)
7. Share on social media (use twitter_api)
8. Confirm completion (return result)
```

#### 4. Memory

Agents maintain context across interactions:

```python
class AgentMemory:
    def __init__(self):
        self.short_term = []   # Recent interactions
        self.long_term = {}    # Persistent knowledge
        self.working = {}      # Current task state

    def remember(self, key, value):
        """Store information"""
        self.long_term[key] = value

    def recall(self, key):
        """Retrieve information"""
        return self.long_term.get(key)

    def update_context(self, interaction):
        """Add to short-term memory"""
        self.short_term.append(interaction)
        # Prune if too long
        if len(self.short_term) > 10:
            self.short_term = self.short_term[-10:]
```

---

## Setting Up Your Environment

### Step 1: Create Project Directory

```bash
# Create and navigate to project directory
mkdir agentic-workflow-tutorial
cd agentic-workflow-tutorial

# Initialize git repository
git init

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 2: Install Dependencies

Create `requirements.txt`:

```txt
openai>=1.12.0
anthropic>=0.18.0
langchain>=0.1.0
langgraph>=0.0.20
python-dotenv>=1.0.0
requests>=2.31.0
pydantic>=2.5.0
fastapi>=0.109.0
uvicorn>=0.27.0
pytest>=7.4.0
```

Install packages:

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys

Create `.env` file:

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional
TAVILY_API_KEY=your-search-api-key
SERP_API_KEY=your-serp-key
```

Create `.gitignore`:

```bash
# .gitignore
venv/
.env
__pycache__/
*.pyc
.pytest_cache/
```

### Step 4: Project Structure

```bash
agentic-workflow-tutorial/
├── .env                    # API keys (secret)
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── agents/                # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py
│   └── research_agent.py
├── tools/                 # Agent tools
│   ├── __init__.py
│   ├── web_search.py
│   └── file_ops.py
├── workflows/             # Workflow definitions
│   ├── __init__.py
│   └── blog_writer.py
└── tests/                # Unit tests
    └── test_agents.py
```

Create structure:

```bash
mkdir -p agents tools workflows tests
touch agents/__init__.py tools/__init__.py workflows/__init__.py
```

---

## Building Your First Agent

### Step 1: Create Base Agent

Create `agents/base_agent.py`:

```python
"""
Base Agent Implementation
Provides foundation for all specialized agents
"""

from typing import List, Dict, Any, Callable
import openai
from pydantic import BaseModel

class Tool(BaseModel):
    """Tool definition for agents"""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]

class BaseAgent:
    """
    Base agent with tool-calling capabilities

    Example:
        agent = BaseAgent(
            name="Assistant",
            model="gpt-4",
            tools=[search_tool, calculator_tool]
        )
        result = agent.run("What's the population of Tokyo?")
    """

    def __init__(
        self,
        name: str,
        model: str = "gpt-4-turbo-preview",
        tools: List[Tool] = None,
        system_prompt: str = None
    ):
        self.name = name
        self.model = model
        self.tools = tools or []
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.conversation_history = []
        self.client = openai.OpenAI()

    def _default_system_prompt(self) -> str:
        """Default system prompt for agents"""
        return f"""You are {self.name}, an AI agent that can use tools to accomplish tasks.

When given a task:
1. Break it down into steps
2. Use available tools when needed
3. Reason through each step
4. Provide clear, accurate results

Available tools: {[tool.name for tool in self.tools]}
"""

    def run(self, task: str, max_iterations: int = 10) -> str:
        """
        Execute a task with the agent

        Args:
            task: The task to accomplish
            max_iterations: Maximum planning/execution loops

        Returns:
            Final result of the task
        """
        self.conversation_history.append({
            "role": "user",
            "content": task
        })

        for iteration in range(max_iterations):
            # Get next action from LLM
            response = self._get_llm_response()

            # Check if task is complete
            if self._is_complete(response):
                return response.choices[0].message.content

            # Execute tool calls if any
            if response.choices[0].message.tool_calls:
                self._execute_tools(response.choices[0].message.tool_calls)
            else:
                # No tools needed, task complete
                return response.choices[0].message.content

        return "Task did not complete within iteration limit"

    def _get_llm_response(self):
        """Get response from language model"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history
        ]

        # Convert tools to OpenAI format
        tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools
        ]

        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tool_definitions if tool_definitions else None,
            tool_choice="auto"
        )

    def _execute_tools(self, tool_calls):
        """Execute the tools requested by the LLM"""
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = eval(tool_call.function.arguments)

            # Find and execute the tool
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if tool:
                result = tool.function(**tool_args)

                # Add result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": str(result)
                })

    def _is_complete(self, response) -> bool:
        """Check if the task is complete"""
        return not response.choices[0].message.tool_calls
```

> **💡 Expert Tip:** Always implement proper error handling in production agents. This example omits it for clarity, but you should wrap tool executions in try/except blocks.

---

### Step 2: Create Agent Tools

Create `tools/web_search.py`:

```python
"""
Web Search Tool
Allows agents to search the internet for information
"""

import os
import requests
from typing import List, Dict

def web_search(query: str, num_results: int = 5) -> str:
    """
    Search the web and return formatted results

    Args:
        query: Search query
        num_results: Number of results to return

    Returns:
        Formatted search results
    """
    # Using Tavily API (you can use any search API)
    api_key = os.getenv("TAVILY_API_KEY")

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": api_key,
            "query": query,
            "max_results": num_results
        }
    )

    results = response.json().get("results", [])

    # Format results
    formatted = f"Search results for '{query}':\n\n"
    for i, result in enumerate(results, 1):
        formatted += f"{i}. {result['title']}\n"
        formatted += f"   {result['snippet']}\n"
        formatted += f"   Source: {result['url']}\n\n"

    return formatted

# Tool definition for agents
WEB_SEARCH_TOOL = {
    "name": "web_search",
    "description": "Search the internet for current information",
    "function": web_search,
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query"
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return (default: 5)",
                "default": 5
            }
        },
        "required": ["query"]
    }
}
```

Create `tools/file_ops.py`:

```python
"""
File Operations Tools
Allow agents to read and write files
"""

import os
from pathlib import Path

def read_file(file_path: str) -> str:
    """
    Read contents of a file

    Args:
        file_path: Path to the file

    Returns:
        File contents
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file

    Args:
        file_path: Path to the file
        content: Content to write

    Returns:
        Success message
    """
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)

        return f"Successfully wrote to '{file_path}'"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Tool definitions
READ_FILE_TOOL = {
    "name": "read_file",
    "description": "Read the contents of a file",
    "function": read_file,
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read"
            }
        },
        "required": ["file_path"]
    }
}

WRITE_FILE_TOOL = {
    "name": "write_file",
    "description": "Write content to a file",
    "function": write_file,
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to write"
            },
            "content": {
                "type": "string",
                "description": "Content to write to the file"
            }
        },
        "required": ["file_path", "content"]
    }
}
```

---

### Step 3: Build a Research Agent

Create `agents/research_agent.py`:

```python
"""
Research Agent
Specializes in gathering and synthesizing information
"""

from agents.base_agent import BaseAgent, Tool
from tools.web_search import web_search, WEB_SEARCH_TOOL
from tools.file_ops import write_file, WRITE_FILE_TOOL

class ResearchAgent(BaseAgent):
    """
    Agent specialized in research tasks

    Capabilities:
    - Web search and information gathering
    - Synthesizing information from multiple sources
    - Creating structured research reports
    - Saving results to files
    """

    def __init__(self, model: str = "gpt-4-turbo-preview"):
        tools = [
            Tool(**WEB_SEARCH_TOOL),
            Tool(**WRITE_FILE_TOOL)
        ]

        system_prompt = """You are a Research Agent specialized in gathering and analyzing information.

Your workflow:
1. **Understand** the research question
2. **Search** for relevant information using web_search
3. **Analyze** and synthesize findings
4. **Structure** information clearly
5. **Save** results using write_file if requested

Best practices:
- Use multiple searches to get comprehensive information
- Cross-reference sources for accuracy
- Cite sources in your reports
- Organize information logically
- Highlight key insights and takeaways
"""

        super().__init__(
            name="Research Agent",
            model=model,
            tools=tools,
            system_prompt=system_prompt
        )

# Example usage
if __name__ == "__main__":
    agent = ResearchAgent()

    task = """
    Research the current state of AI agents in 2026.
    Focus on:
    1. Major companies building agent platforms
    2. Key capabilities and use cases
    3. Market size and growth

    Save a comprehensive report to 'research/ai_agents_2026.md'
    """

    result = agent.run(task)
    print(result)
```

---

### Step 4: Test Your Agent

Create `test_agent.py`:

```python
"""
Test script for research agent
"""

from agents.research_agent import ResearchAgent

def test_simple_research():
    """Test basic research capability"""
    agent = ResearchAgent()

    task = "What are the top 3 AI agent platforms in 2026?"
    result = agent.run(task)

    print("=" * 60)
    print("TASK:", task)
    print("=" * 60)
    print("RESULT:")
    print(result)
    print("=" * 60)

def test_research_with_save():
    """Test research with file saving"""
    agent = ResearchAgent()

    task = """
    Research the benefits of agentic AI workflows.
    Create a summary with:
    - Top 5 benefits
    - Real-world examples
    - Potential challenges

    Save to 'output/agentic_benefits.txt'
    """

    result = agent.run(task)
    print(result)

if __name__ == "__main__":
    print("Testing Research Agent...\n")
    test_simple_research()
    # test_research_with_save()
```

Run the test:

```bash
python test_agent.py
```

> **⚠️ Important:** Make sure your API keys are set in `.env` before running!

---

## Advanced Agent Patterns

### Multi-Agent Systems

Multiple agents working together:

```python
"""
Multi-Agent Collaboration Example
"""

class AgentOrchestrator:
    """Coordinates multiple specialized agents"""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.writer_agent = WriterAgent()
        self.editor_agent = EditorAgent()

    def create_blog_post(self, topic: str) -> str:
        """
        Coordinate agents to create a blog post

        Workflow:
        1. Research Agent gathers information
        2. Writer Agent creates draft
        3. Editor Agent refines and polishes
        """
        # Step 1: Research
        research_task = f"Research {topic} and create a detailed outline"
        research_result = self.research_agent.run(research_task)

        # Step 2: Write
        write_task = f"Write a blog post using this research:\n{research_result}"
        draft = self.writer_agent.run(write_task)

        # Step 3: Edit
        edit_task = f"Edit and improve this blog post:\n{draft}"
        final_post = self.editor_agent.run(edit_task)

        return final_post

# Usage
orchestrator = AgentOrchestrator()
blog_post = orchestrator.create_blog_post("AI Agents in Healthcare")
```

### ReAct Pattern (Reasoning + Acting)

Agents that explain their reasoning:

```python
class ReActAgent(BaseAgent):
    """Agent using ReAct pattern for transparent reasoning"""

    def run(self, task: str) -> str:
        thought_process = []

        while not self.is_task_complete():
            # Thought: Reason about what to do
            thought = self._think()
            thought_process.append(f"Thought: {thought}")

            # Action: Decide on action
            action = self._decide_action(thought)
            thought_process.append(f"Action: {action}")

            # Observation: Execute and observe result
            observation = self._execute_action(action)
            thought_process.append(f"Observation: {observation}")

        return "\n".join(thought_process)
```

### Planning Agents

Agents that create and execute plans:

```python
class PlanningAgent(BaseAgent):
    """Agent that creates detailed plans before executing"""

    def run(self, task: str) -> str:
        # Step 1: Create plan
        plan = self._create_plan(task)
        print(f"Plan:\n{plan}\n")

        # Step 2: Execute each step
        results = []
        for step in plan.steps:
            result = self._execute_step(step)
            results.append(result)

            # Re-plan if step failed
            if not result.success:
                plan = self._replan(plan, step, result)

        # Step 3: Synthesize results
        return self._synthesize_results(results)
```

---

## Real-World Applications

### Application 1: Customer Support Agent

```python
class CustomerSupportAgent(BaseAgent):
    """Handles customer support inquiries"""

    def __init__(self):
        tools = [
            Tool(**SEARCH_KNOWLEDGE_BASE_TOOL),
            Tool(**CHECK_ORDER_STATUS_TOOL),
            Tool(**CREATE_TICKET_TOOL),
            Tool(**SEND_EMAIL_TOOL)
        ]

        super().__init__(
            name="Support Agent",
            tools=tools,
            system_prompt="""You are a customer support agent.

Workflow:
1. Understand the customer's issue
2. Search knowledge base for solutions
3. Check order status if relevant
4. Provide clear, helpful responses
5. Escalate to human if needed (create ticket)
6. Send confirmation email

Be empathetic, professional, and solution-focused.
"""
        )
```

### Application 2: Code Review Agent

```python
class CodeReviewAgent(BaseAgent):
    """Reviews code and provides feedback"""

    def __init__(self):
        tools = [
            Tool(**READ_FILE_TOOL),
            Tool(**RUN_LINTER_TOOL),
            Tool(**RUN_TESTS_TOOL),
            Tool(**SECURITY_SCAN_TOOL),
            Tool(**CREATE_REVIEW_TOOL)
        ]

        super().__init__(
            name="Code Reviewer",
            tools=tools
        )

    def review_pr(self, pr_number: int) -> str:
        """
        Comprehensive code review

        Checks:
        - Code quality and style
        - Test coverage
        - Security vulnerabilities
        - Best practices
        - Documentation
        """
        # Implementation here
        pass
```

### Application 3: Data Analysis Agent

```python
class DataAnalysisAgent(BaseAgent):
    """Analyzes data and generates insights"""

    def __init__(self):
        tools = [
            Tool(**LOAD_DATA_TOOL),
            Tool(**QUERY_DATA_TOOL),
            Tool(**VISUALIZE_TOOL),
            Tool(**STATISTICAL_TEST_TOOL),
            Tool(**GENERATE_REPORT_TOOL)
        ]

        super().__init__(
            name="Data Analyst",
            tools=tools
        )

    def analyze_dataset(self, dataset_path: str, questions: List[str]) -> str:
        """
        Analyze dataset and answer specific questions

        Capabilities:
        - Exploratory data analysis
        - Statistical testing
        - Visualization generation
        - Insight extraction
        - Report creation
        """
        # Implementation here
        pass
```

---

## Troubleshooting & Best Practices

### Common Issues

#### Issue 1: Agent Gets Stuck in Loops

**Problem:** Agent repeatedly tries the same action

**Solution:**
```python
class LoopPreventionAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.action_history = []

    def run(self, task: str) -> str:
        for iteration in range(self.max_iterations):
            action = self._get_next_action()

            # Check for loops
            if self._is_repeating(action):
                # Try alternative approach
                action = self._get_alternative_action()

            self.action_history.append(action)
            result = self._execute(action)

            if self._is_complete(result):
                return result
```

#### Issue 2: Token Limit Exceeded

**Problem:** Conversation history grows too large

**Solution:**
```python
def _manage_context(self):
    """Keep conversation history within limits"""
    if self._count_tokens(self.conversation_history) > 50000:
        # Summarize old conversations
        summary = self._summarize_history(self.conversation_history[:-10])
        self.conversation_history = [
            {"role": "system", "content": f"Previous context: {summary}"},
            *self.conversation_history[-10:]  # Keep recent 10
        ]
```

#### Issue 3: Tool Execution Fails

**Problem:** Tools throw errors, breaking the agent

**Solution:**
```python
def _execute_tools(self, tool_calls):
    """Execute tools with error handling"""
    for tool_call in tool_calls:
        try:
            tool = self._get_tool(tool_call.function.name)
            result = tool.function(**tool_call.function.arguments)

            self.conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
        except Exception as e:
            # Report error to agent so it can try alternative
            self.conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error executing {tool_call.function.name}: {str(e)}"
            })
```

### Best Practices

✅ **DO:**
- Use clear, specific tool descriptions
- Implement proper error handling
- Set reasonable iteration limits
- Log agent actions for debugging
- Test with diverse inputs
- Monitor token usage
- Use structured outputs (JSON)
- Implement safety guardrails

❌ **DON'T:**
- Give agents unrestricted system access
- Skip input validation
- Ignore error states
- Use agents for time-critical tasks without fallbacks
- Expose sensitive credentials in prompts
- Deploy without testing edge cases
- Let conversation history grow unbounded

---

## Next Steps

### Level Up Your Skills

**1. Explore Frameworks:**
- LangChain / LangGraph
- AutoGPT
- CrewAI
- Microsoft AutoGen

**2. Advanced Topics:**
- Multi-agent communication protocols
- Agent memory systems (vector databases)
- Fine-tuning agents for specific domains
- Human-in-the-loop workflows
- Agent evaluation and benchmarking

**3. Production Deployment:**
- Containerization with Docker
- API deployment with FastAPI
- Monitoring and observability
- Rate limiting and cost control
- Security hardening

### Resources

**📚 Further Reading:**
- "Building LLM-Powered Applications" by O'Reilly
- LangChain documentation
- OpenAI Cookbook
- Anthropic's Claude documentation

**🎓 Courses:**
- DeepLearning.AI - "AI Agents in LangGraph"
- "Building Production-Ready AI Agents"
- Advanced RAG techniques

**🧑‍💻 Community:**
- r/LangChain subreddit
- LangChain Discord
- AI Agents community forums
- GitHub discussions

---

## Q&A

**Q: How much do API calls cost for agents?**
A: Depends on usage. A research agent making 5-10 tool calls might cost $0.10-$0.50 per task with GPT-4. Use cheaper models (GPT-3.5, Claude Haiku) for development.

**Q: Can agents make mistakes?**
A: Yes! Always implement verification steps and human oversight for critical decisions. Agents can hallucinate, misunderstand tasks, or use tools incorrectly.

**Q: How do I make agents faster?**
A: Use parallel tool calls, faster models (GPT-3.5-turbo), caching, and limit conversation history. Consider streaming responses.

**Q: Are agents safe for production?**
A: With proper safeguards, yes. Implement rate limiting, input validation, output verification, and human-in-the-loop for critical actions.

**Q: What's the difference between agents and chatbots?**
A: Chatbots respond to messages. Agents execute multi-step tasks, use tools, make decisions, and work toward goals autonomously.

---

## Conclusion

You've now learned the fundamentals of building agentic AI workflows:

✅ Understanding agent architecture
✅ Creating base agents with tool-calling
✅ Implementing specialized agents
✅ Building multi-agent systems
✅ Deploying real-world applications

**Next Challenge:** Build your own agent! Ideas:
- Personal assistant that manages your calendar
- Code documentation generator
- Social media content creator
- Data analysis automation
- Customer support chatbot

---

*Tutorial created by AI Engineering Team | Last updated: January 2026*
*Questions? Open an issue on our GitHub or join the community Discord.*

**Share your agent creations with #AgenticAI on social media!**
