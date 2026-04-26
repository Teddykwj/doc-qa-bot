Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Production

LangSmith Studio

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
* Set up local Agent server
* 1. Install the LangGraph CLI
* 2. Prepare your agent
* 3. Environment variables
* 4. Create a LangGraph config file
* 5. Install dependencies
* 6. View your agent in Studio
* Video guide

Production

# LangSmith Studio

Copy page

Copy page

When building agents with LangChain locally, it’s helpful to visualize what’s happening inside your agent, interact with it in real-time, and debug issues as they occur. **LangSmith Studio** is a free visual interface for developing and testing your LangChain agents from your local machine.
Studio connects to your locally running agent to show you each step your agent takes: the prompts sent to the model, tool calls and their results, and the final output. You can test different inputs, inspect intermediate states, and iterate on your agent’s behavior without additional code or deployment.
This pages describes how to set up Studio with your local LangChain agent.

## ​ Prerequisites

Before you begin, ensure you have the following:

* **A LangSmith account**: Sign up (for free) or log in at smith.langchain.com.
* **A LangSmith API key**: Follow the Create an API key guide.
* If you don’t want data traced to LangSmith, set `LANGSMITH_TRACING=false` in your application’s `.env` file. With tracing disabled, no data leaves your local server.

## ​ Set up local Agent server

### ​ 1. Install the LangGraph CLI

The LangGraph CLI provides a local development server (also called Agent Server) that connects your agent to Studio.

```
# Python >= 3.11 is required.
pip install --upgrade "langgraph-cli[inmem]"
```

### ​ 2. Prepare your agent

If you already have a LangChain agent, you can use it directly. This example uses a simple email agent:

agent.py

```
from langchain.agents import create_agent

def send_email(to: str, subject: str, body: str):
    """Send an email"""
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... email sending logic

    return f"Email sent to {to}"

agent = create_agent(
    "gpt-5.4",
    tools=[send_email],
    system_prompt="You are an email assistant. Always use the send_email tool.",
)
```

### ​ 3. Environment variables

Studio requires a LangSmith API key to connect your local agent. Create a `.env` file in the root of your project and add your API key from LangSmith.

Ensure your `.env` file is not committed to version control, such as Git.

.env

```
LANGSMITH_API_KEY=lsv2...
```

### ​ 4. Create a LangGraph config file

The LangGraph CLI uses a configuration file to locate your agent and manage dependencies. Create a `langgraph.json` file in your app’s directory:

langgraph.json

```
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.py:agent"
  },
  "env": ".env"
}
```

The `create_agent` function automatically returns a compiled LangGraph graph, which is what the `graphs` key expects in the configuration file.

For detailed explanations of each key in the JSON object of the configuration file, refer to the LangGraph configuration file reference.

At this point, the project structure will look like this:

```
my-app/
├── src
│   └── agent.py
├── .env
└── langgraph.json
```

### ​ 5. Install dependencies

Install your project dependencies from the root directory:

pip

uv

```
pip install langchain langchain-openai
```

### ​ 6. View your agent in Studio

Start the development server to connect your agent to Studio:

```
langgraph dev
```

Safari blocks `localhost` connections to Studio. To work around this, run the above command with `--tunnel` to access Studio via a secure tunnel. You’ll need to manually add the tunnel URL to allowed origins by clicking **Connect to a local server** in the Studio UI. See the troubleshooting guide for steps.

Once the server is running, your agent is accessible both via API at `http://127.0.0.1:2024` and through the Studio UI at `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`:

![Agent view in the Studio UI](https://mintcdn.com/langchain-5e9cc07a/TCDks4pdsHdxWmuJ/oss/images/studio_create-agent.png?fit=max&auto=format&n=TCDks4pdsHdxWmuJ&q=85&s=ebd259e9fa24af7d011dfcc568f74be2)

With Studio connected to your local agent, you can iterate quickly on your agent’s behavior. Run a test input, inspect the full execution trace including prompts, tool arguments, return values, and token/latency metrics in LangSmith. When something goes wrong, Studio captures exceptions with the surrounding state to help you understand what happened.
The development server supports hot-reloading—make changes to prompts or tool signatures in your code, and Studio reflects them immediately. Re-run conversation threads from any step to test your changes without starting over. This workflow scales from simple single-tool agents to complex multi-node graphs.
For more information on how to run Studio, refer to the following guides in the LangSmith docs:

* Run application
* Manage assistants
* Manage threads
* Iterate on prompts
* Debug LangSmith traces
* Add node to dataset

## ​ Video guide

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Test

Previous

Agent Chat UI

Next

⌘I