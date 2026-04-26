Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Test

Unit testing

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

* Mock chat model
* InMemorySaver checkpointer
* Next steps

Agent development

Test

# Unit testing

Copy page

Test agent logic without API calls using fake chat models and in-memory persistence.

Copy page

Unit tests exercise small, deterministic pieces of your agent in isolation. By replacing the real LLM with an in-memory fake (AKA fixture), you can script exact responses (text, tool calls, and errors) so tests are fast, free, and repeatable without API keys.

## ​ Mock chat model

LangChain provides `GenericFakeChatModel` for mocking text responses. It accepts an iterator of responses (`AIMessage` objects or strings) and returns one per invocation. It supports both regular and streaming usage.

```
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

model = GenericFakeChatModel(messages=iter([
    AIMessage(content="", tool_calls=[ToolCall(name="foo", args={"bar": "baz"}, id="call_1")]),
    "bar"
]))

model.invoke("hello")
# AIMessage(content='', ..., tool_calls=[{'name': 'foo', 'args': {'bar': 'baz'}, 'id': 'call_1', 'type': 'tool_call'}])
```

If we invoke the model again, it will return the next item in the iterator:

```
model.invoke("hello, again!")
# AIMessage(content='bar', ...)
```

## ​ InMemorySaver checkpointer

To enable persistence during testing, you can use the `InMemorySaver` checkpointer. This allows you to simulate multiple turns to test state-dependent behavior:

```
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    tools=[],
    checkpointer=InMemorySaver()
)

# First invocation
agent.invoke(
    {"messages": [HumanMessage(content="I live in Sydney, Australia")]},
    config={"configurable": {"thread_id": "session-1"}}
)

# Second invocation: the first message is persisted (Sydney location), so the model returns GMT+10 time
agent.invoke(
    {"messages": [HumanMessage(content="What's my local time?")]},
    config={"configurable": {"thread_id": "session-1"}}
)
```

## ​ Next steps

Learn how to test your agent with real model provider APIs in Integration testing.


---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Test

Previous

Integration testing

Next

⌘I