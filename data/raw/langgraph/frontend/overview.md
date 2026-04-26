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
* Local server
* Changelog
* Thinking in LangGraph
* Workflows + agents

##### Capabilities

* Persistence
* Durable execution
* Streaming
* Interrupts
* Time travel
* Memory
* Subgraphs

##### Production

* Application structure
* Test
* LangSmith Studio
* Agent Chat UI
* LangSmith Deployment
* LangSmith Observability

##### Frontend

* Overview
* Graph execution

##### LangGraph APIs

* Graph API
* Functional API
* Runtime

On this page

* Architecture
* Patterns
* Related patterns

Frontend

# Overview

Copy page

Render LangGraph agents to the frontend

Copy page

Build frontends that visualize LangGraph pipelines in real time. These patterns show how to render multi-step graph execution with per-node status and streaming content from custom `StateGraph` workflows.

## ​ Architecture

LangGraph graphs are composed of named nodes connected by edges. Each node executes a step (classify, research, analyze, synthesize) and writes output to a specific state key. On the frontend, `useStream` provides reactive access to node outputs, streaming tokens, and graph metadata so you can map each node to a UI card.


```
from langgraph.graph import StateGraph, MessagesState, START, END

class State(MessagesState):
    classification: str
    research: str
    analysis: str

graph = StateGraph(State)
graph.add_node("classify", classify_node)
graph.add_node("research", research_node)
graph.add_node("analyze", analyze_node)
graph.add_edge(START, "classify")
graph.add_edge("classify", "research")
graph.add_edge("research", "analyze")
graph.add_edge("analyze", END)

app = graph.compile()
```

On the frontend, `useStream` exposes `stream.values` for completed node outputs and `getMessagesMetadata` for identifying which node produced each streaming token.

```
import { useStream } from "@langchain/react";

function Pipeline() {
  const stream = useStream<typeof graph>({
    apiUrl: "http://localhost:2024",
    assistantId: "pipeline",
  });

  const classification = stream.values?.classification;
  const research = stream.values?.research;
  const analysis = stream.values?.analysis;
}
```

## ​ Patterns

## Graph execution

Visualize multi-step graph pipelines with per-node status and streaming content.

## ​ Related patterns

The LangChain frontend patterns—markdown messages, tool calling, optimistic updates, and more—work with any LangGraph graph. The `useStream` hook provides the same core API whether you use `createAgent`, `createDeepAgent`, or a custom `StateGraph`.


---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

LangSmith Observability

Previous

Graph execution

Next

⌘I