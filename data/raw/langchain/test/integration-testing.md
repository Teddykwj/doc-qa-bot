Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Test

Integration testing

Deep AgentsLangChainLangGraphIntegrationsLearnReferenceContribute

Python



* Overview

##### Get started

* Install
* Quickstart
* Changelog
* Philosophy

##### Core components

* Agents
* Models
* Messages
* Tools
* Short-term memory
* Streaming
* Structured output

##### Middleware

* Overview
* Prebuilt middleware
* Custom middleware

##### Frontend

* Overview
* Patterns
* Integrations

##### Advanced usage

* Guardrails
* Runtime
* Context engineering
* Model Context Protocol (MCP)
* Human-in-the-loop
* Multi-agent
* Retrieval
* Long-term memory

##### Agent development

* LangSmith Studio
* Test

  + Overview
  + Unit testing
  + Integration testing
  + Agent Evals
* Agent Chat UI

##### Deploy with LangSmith

* Deployment
* Observability

On this page

* Separate unit and integration tests
* Manage API keys
* Assert on structure, not content
* Reduce cost and latency
* Record and replay HTTP calls
* Next steps

Agent development

Test

# Integration testing

Copy page

Test agents with real LLM APIs by organizing tests, managing keys, handling flakiness, and controlling costs.

Copy page

Integration tests verify that your agent works correctly with model APIs and external services. Unlike unit tests that use fakes and mocks, integration tests make actual network calls to confirm that components work together, credentials are valid, and latency is acceptable.
Because LLM responses are nondeterministic, integration tests require different strategies than traditional software tests. This guide covers how to organize, write, and run integration tests for your agents. For general test infrastructure when contributing to LangChain itself, see Contributing to code.

## ​ Separate unit and integration tests

Integration tests are slower and require API credentials, so keep them separate from unit tests. This lets you run fast unit tests on every change and reserve integration tests for CI or pre-deploy checks.
Use pytest markers to tag integration tests:

```
import pytest

@pytest.mark.integration
def test_agent_with_real_model():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })
    assert len(result["messages"]) > 1
```

Configure pytest to recognize the marker and exclude integration tests from default runs:

pytest.ini

pyproject.toml

```
[pytest]
markers =
    integration: tests that call real LLM APIs
addopts = -m "not integration"
```

Run integration tests explicitly:

```
pytest -m integration
```

## ​ Manage API keys

Integration tests require real API credentials. Load them from environment variables so keys stay out of source control.
Use a `conftest.py` fixture to validate that required keys are available:

```
import os
import pytest

@pytest.fixture(autouse=True)
def check_api_keys():
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
```

For local development, store keys in a `.env` file and load them with `python-dotenv`:

.env

```
OPENAI_API_KEY=sk-...
```

conftest.py

```
from dotenv import load_dotenv

load_dotenv()
```

Add `.env` to your `.gitignore` to avoid committing credentials. In CI, inject secrets through your provider’s secrets management (e.g., GitHub Actions secrets).

## ​ Assert on structure, not content

LLM responses vary between runs. Instead of asserting on exact output strings, verify the structural properties of the response: message types, tool call names, argument shapes, and message count.

```
def test_agent_calls_weather_tool():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })

    messages = result["messages"]
    tool_calls = [
        tc
        for msg in messages
        if hasattr(msg, "tool_calls")
        for tc in (msg.tool_calls or [])
    ]

    assert any(tc["name"] == "get_weather" for tc in tool_calls)
    assert isinstance(messages[-1], AIMessage)
    assert len(messages[-1].content) > 0
```

For more rigorous trajectory assertions, use the AgentEvals evaluators which support fuzzy matching modes like `unordered` and `superset`.

## ​ Reduce cost and latency

Integration tests that call LLM APIs incur real costs. A few practices help keep test suites fast and affordable:

* **Use smaller models**: `gemini-3.1-flash-lite-preview` or equivalent for tests that only need to verify tool calling and response structure.
* **Set `maxTokens`**: Cap response length to avoid long, expensive completions.
* **Limit test scope**: Test one behavior per test. Avoid end-to-end scenarios that chain many LLM calls when a single-turn test suffices.
* **Run selectively**: Use the test separation from above to run integration tests only in CI or before deploy, not on every file save.

```
agent = create_agent(
    "gemini-3.1-flash-lite-preview",
    tools=[get_weather],
    model_kwargs={"max_tokens": 256},
)
```

## ​ Record and replay HTTP calls

For tests that run frequently in CI, you can record HTTP interactions on the first run and replay them on subsequent runs without making real API calls. This eliminates cost and latency after the initial recording.
`vcrpy` records HTTP request/response pairs into YAML “cassette” files. The `pytest-recording` plugin integrates this with pytest.
Set up your `conftest.py` to filter sensitive information from cassettes:

conftest.py

```
import pytest

@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": [
            ("authorization", "XXXX"),
            ("x-api-key", "XXXX"),
        ],
        "filter_query_parameters": [
            ("api_key", "XXXX"),
            ("key", "XXXX"),
        ],
    }
```

Configure your project to recognize the `vcr` marker:

pytest.ini

pyproject.toml

```
[pytest]
markers =
    vcr: record/replay HTTP via VCR
addopts = --record-mode=once
```

The `--record-mode=once` option records HTTP interactions on the first run and replays them on subsequent runs.

Decorate your tests with the `vcr` marker:

```
@pytest.mark.vcr()
def test_agent_trajectory():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })
    assert any(
        tc["name"] == "get_weather"
        for msg in result["messages"]
        if hasattr(msg, "tool_calls")
        for tc in (msg.tool_calls or [])
    )
```

The first run makes real network calls and generates a cassette file in `tests/cassettes/`. Subsequent runs replay the recorded responses.

When you modify prompts, add new tools, or change expected trajectories, your saved cassettes will become outdated and your existing tests **will fail**. Delete the corresponding cassette files and rerun the tests to record fresh interactions.

## ​ Next steps

Learn how to evaluate agent trajectories with deterministic matching or LLM-as-judge evaluators in Evals.


---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Unit testing

Previous

Agent Evals

Next

⌘I