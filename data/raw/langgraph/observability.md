Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Production

LangSmith Observability

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

* Prerequisites
* Enable tracing
* Trace selectively
* Log to a project
* Add metadata to traces
* Use anonymizers to prevent logging of sensitive data in traces

Production

# LangSmith Observability

Copy page

Copy page

Traces are a series of steps that your application takes to go from input to output. Each of these individual steps is represented by a run. You can use LangSmith to visualize these execution steps. To use it, enable tracing for your application. This enables you to do the following:

* Debug a locally running application.
* Evaluate the application performance.
* Monitor the application.

## ​ Prerequisites

Before you begin, ensure you have the following:

* **A LangSmith account**: Sign up (for free) or log in at smith.langchain.com.
* **A LangSmith API key**: Follow the Create an API key guide.

## ​ Enable tracing

To enable tracing for your application, set the following environment variables:

```
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

By default, the trace will be logged to the project with the name `default`. To configure a custom project name, see Log to a project.
For more information, see Trace with LangGraph.

## ​ Trace selectively

You may opt to trace specific invocations or parts of your application using LangSmith’s `tracing_context` context manager:

```
import langsmith as ls

# This WILL be traced
with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Send a test email to alice@example.com"}]})

# This will NOT be traced (if LANGSMITH_TRACING is not set)
agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})
```

## ​ Log to a project

Statically

You can set a custom project name for your entire application by setting the `LANGSMITH_PROJECT` environment variable:

```
export LANGSMITH_PROJECT=my-agent-project
```



Dynamically

You can set the project name programmatically for specific operations:

```
import langsmith as ls

with ls.tracing_context(project_name="email-agent-test", enabled=True):
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Send a welcome email"}]
    })
```

## ​ Add metadata to traces

You can annotate your traces with custom metadata and tags:

```
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Send a welcome email"}]},
    config={
        "tags": ["production", "email-assistant", "v1.0"],
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "environment": "production"
        }
    }
)
```

`tracing_context` also accepts tags and metadata for fine-grained control:

```
with ls.tracing_context(
    project_name="email-agent-test",
    enabled=True,
    tags=["production", "email-assistant", "v1.0"],
    metadata={"user_id": "user_123", "session_id": "session_456", "environment": "production"}):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Send a welcome email"}]}
    )
```

This custom metadata and tags will be attached to the trace in LangSmith.

To learn more about how to use traces to debug, evaluate, and monitor your agents, see the LangSmith documentation.

## ​ Use anonymizers to prevent logging of sensitive data in traces

You may want to mask sensitive data to prevent it from being logged to LangSmith. You can create anonymizers and apply them to
your graph using configuration. This example will redact anything matching the Social Security Number format XXX-XX-XXXX from traces sent to LangSmith.

Python

```
from langchain_core.tracers.langchain import LangChainTracer
from langgraph.graph import StateGraph, MessagesState
from langsmith import Client
from langsmith.anonymizer import create_anonymizer

anonymizer = create_anonymizer([
    # Matches SSNs
    { "pattern": r"\b\d{3}-?\d{2}-?\d{4}\b", "replace": "<ssn>" }
])

tracer_client = Client(anonymizer=anonymizer)
tracer = LangChainTracer(client=tracer_client)
# Define the graph
graph = (
    StateGraph(MessagesState)
    ...
    .compile()
    .with_config({'callbacks': [tracer]})
)
```

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

LangSmith Deployment

Previous

Overview

Next

⌘I