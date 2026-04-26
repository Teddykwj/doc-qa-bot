Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Agent development

Agent Chat UI

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

* Quick start
* Local development
* Connect to your agent

Agent development

# Agent Chat UI

Copy page

Copy page

Agent Chat UI is a Next.js application that provides a conversational interface for interacting with any LangChain agent. It supports real-time chat, tool visualization, and advanced features like time-travel debugging and state forking. Agent Chat UI works seamlessly with agents created using `create_agent` and provides interactive experiences for your agents with minimal setup, whether you’re running locally or in a deployed context (such as LangSmith).
Agent Chat UI is open source and can be adapted to your application needs.

You can use generative UI in the Agent Chat UI. For more information, see Implement generative user interfaces with LangGraph.

### ​ Quick start

The fastest way to get started is using the hosted version:

1. **Visit Agent Chat UI**
2. **Connect your agent** by entering your deployment URL or local server address
3. **Start chatting** - the UI will automatically detect and render tool calls and interrupts

### ​ Local development

For customization or local development, you can run Agent Chat UI locally:

Use npx

Clone repository

```
# Create a new Agent Chat UI project
npx create-agent-chat-app --project-name my-chat-ui
cd my-chat-ui

# Install dependencies and start
pnpm install
pnpm dev
```

### ​ Connect to your agent

Agent Chat UI can connect to both local and deployed agents.
After starting Agent Chat UI, you’ll need to configure it to connect to your agent:

1. **Graph ID**: Enter your graph name (find this under `graphs` in your `langgraph.json` file)
2. **Deployment URL**: Your Agent server’s endpoint (e.g., `http://localhost:2024` for local development, or your deployed agent’s URL)
3. **LangSmith API key (optional)**: Add your LangSmith API key (not required if you’re using a local Agent server)

Once configured, Agent Chat UI will automatically fetch and display any interrupted threads from your agent.

Agent Chat UI has out-of-the-box support for rendering tool calls and tool result messages. To customize what messages are shown, see Hiding Messages in the Chat.

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Agent Evals

Previous

LangSmith Deployment

Next

⌘I