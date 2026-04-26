Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Test

Test

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

Agent development

Test

# Test

Copy page

Strategies for testing LangChain agents, including unit tests, integration tests, and trajectory evaluations.

Copy page

Agentic applications let an LLM decide its own next steps to solve a problem. That flexibility is powerful, but the model’s black-box nature makes it hard to predict how a tweak in one part of your agent will affect the whole. To build production-ready agents, thorough testing is essential.
There are a few approaches to testing your agents:

* **Unit tests** exercise small, deterministic pieces of your agent in isolation using in-memory fakes so you can assert exact behavior quickly and deterministically.
* **Integration tests** test the agent using real network calls to confirm that components work together, credentials and schemas line up, and latency is acceptable.
* **Evals** use evaluators to assess your agent’s execution trajectory, either via deterministic matching or an LLM judge.

Agentic applications tend to lean more on integration because they chain multiple components together and must deal with flakiness due to the nondeterministic nature of LLMs.

## Unit testing

Mock chat models and use in-memory persistence to test agent logic without API calls.

## Integration testing

Test your agent with real LLM APIs. Organize tests, manage keys, handle flakiness, and control costs.

## Evals

Evaluate agent trajectories with deterministic matching or LLM-as-judge evaluators.

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

LangSmith Studio

Previous

Unit testing

Next

⌘I