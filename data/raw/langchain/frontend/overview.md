Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Frontend

Overview

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
* Agent Chat UI

##### Deploy with LangSmith

* Deployment
* Observability

On this page

* Architecture
* Patterns
* Render messages and output
* Display agent actions
* Manage conversations
* Advanced streaming
* Integrations

Frontend

# Overview

Copy page

Build generative UIs with real-time streaming from LangChain agents

Copy page

Build rich, interactive frontends for agents created with `createAgent`. These patterns cover everything from basic message rendering to advanced workflows like human-in-the-loop approval and time travel debugging.

## ​ Architecture

Every pattern follows the same architecture: a `createAgent` backend streams state to a frontend via the `useStream` hook.

On the backend, `createAgent` produces a compiled LangGraph graph that exposes a streaming API. On the frontend, the `useStream` hook connects to that API and provides reactive state — messages, tool calls, interrupts, history, and more — that you render with any framework.

agent.py

types.ts

Chat.tsx

```
from langchain import create_agent
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather, search_web],
    checkpointer=MemorySaver(),
)
```

`useStream` is available for React, Vue, Svelte, and Angular:

```
import { useStream } from "@langchain/react";   // React
import { useStream } from "@langchain/vue";      // Vue
import { useStream } from "@langchain/svelte";   // Svelte
import { useStream } from "@langchain/angular";  // Angular
```

## ​ Patterns

### ​ Render messages and output

## Markdown messages

Parse and render streamed markdown with proper formatting and code highlighting.

## Structured output

Render typed agent responses as custom UI components instead of plain text.

## Reasoning tokens

Display model thinking processes in collapsible blocks.

## Generative UI

Render AI-generated user interfaces from natural language prompts using json-render.

### ​ Display agent actions

## Tool calling

Show tool calls as rich, type-safe UI cards with loading and error states.

## Human-in-the-loop

Pause the agent for human review with approve, reject, and edit workflows.

### ​ Manage conversations

## Branching chat

Edit messages, regenerate responses, and navigate conversation branches.

## Message queues

Queue multiple messages while the agent processes them sequentially.

### ​ Advanced streaming

## Join & rejoin streams

Disconnect from and reconnect to running agent streams without losing progress.

## Time travel

Inspect, navigate, and resume from any checkpoint in the conversation history.

## ​ Integrations

`useStream` is UI-agnostic. Use it to any component library or generative UI framework.

## AI Elements

Composable shadcn/ui components for AI chat: `Conversation`, `Message`, `Tool`, `Reasoning`.

## assistant-ui

Headless React framework with built-in thread management, branching, and attachment support.

## OpenUI

Generative UI library for data-rich reports and dashboards using the openui-lang component DSL.

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Custom middleware

Previous

Markdown messages

Next

⌘I