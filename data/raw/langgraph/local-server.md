Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Get started

Run a local server

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
* 1. Install the LangGraph CLI
* 2. Create a LangGraph app
* 3. Install dependencies
* 4. Create a .env file
* 5. Launch Agent server
* 6. Test your application in Studio
* 7. Test the API
* Next steps

Get started

# Run a local server

Copy page

Copy page

This guide shows you how to run a LangGraph application locally.

## ​ Prerequisites

Before you begin, ensure you have the following:

* An API key for LangSmith - free to sign up

## ​ 1. Install the LangGraph CLI

pip

uv

```
# Python >= 3.11 is required.
pip install -U "langgraph-cli[inmem]"
```

## ​ 2. Create a LangGraph app

Create a new app from the `new-langgraph-project-python` template. This template demonstrates a single-node application you can extend with your own logic.

```
langgraph new path/to/your/app --template new-langgraph-project-python
```

**Additional templates**
If you use `langgraph new` without specifying a template, you will be presented with an interactive menu that will allow you to choose from a list of available templates.

## ​ 3. Install dependencies

In the root of your new LangGraph app, install the dependencies in `edit` mode so your local changes are used by the server:

pip

uv

```
cd path/to/your/app
pip install -e .
```

## ​ 4. Create a `.env` file

You will find a `.env.example` in the root of your new LangGraph app. Create a `.env` file in the root of your new LangGraph app and copy the contents of the `.env.example` file into it, filling in the necessary API keys:

```
LANGSMITH_API_KEY=lsv2...
```

## ​ 5. Launch Agent server

Start the LangGraph API server locally:

```
langgraph dev
```

Sample output:

```
INFO:langgraph_api.cli:

        Welcome to

╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

This in-memory server is designed for development and testing.
For production use, please use LangSmith Deployment.
```

The `langgraph dev` command starts Agent Server in an in-memory mode. This mode is suitable for development and testing purposes. For production use, deploy Agent Server with access to a persistent storage backend. For more information, see the Platform setup overview.

## ​ 6. Test your application in Studio

Studio is a specialized UI that you can connect to LangGraph API server to visualize, interact with, and debug your application locally. Test your graph in Studio by visiting the URL provided in the output of the `langgraph dev` command:

```
>    - LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

For an Agent Server running on a custom host/port, update the `baseUrl` query parameter in the URL. For example, if your server is running on `http://myhost:3000`:

```
https://smith.langchain.com/studio/?baseUrl=http://myhost:3000
```

Safari compatibility

Use the `--tunnel` flag with your command to create a secure tunnel, as Safari has limitations when connecting to localhost servers:

```
langgraph dev --tunnel
```

## ​ 7. Test the API

* Python SDK (async)
* Python SDK (sync)
* Rest API

1. Install the LangGraph Python SDK:

   ```
   pip install langgraph-sdk
   ```
2. Send a message to the assistant (threadless run):

   ```
   from langgraph_sdk import get_client
   import asyncio

   client = get_client(url="http://localhost:2024")

   async def main():
       async for chunk in client.runs.stream(
           None,  # Threadless run
           "agent", # Name of assistant. Defined in langgraph.json.
           input={
           "messages": [{
               "role": "human",
               "content": "What is LangGraph?",
               }],
           },
       ):
           print(f"Receiving new event of type: {chunk.event}...")
           print(chunk.data)
           print("\n\n")

   asyncio.run(main())
   ```

1. Install the LangGraph Python SDK:

   ```
   pip install langgraph-sdk
   ```
2. Send a message to the assistant (threadless run):

   ```
   from langgraph_sdk import get_sync_client

   client = get_sync_client(url="http://localhost:2024")

   for chunk in client.runs.stream(
       None,  # Threadless run
       "agent", # Name of assistant. Defined in langgraph.json.
       input={
           "messages": [{
               "role": "human",
               "content": "What is LangGraph?",
           }],
       },
       stream_mode="messages-tuple",
   ):
       print(f"Receiving new event of type: {chunk.event}...")
       print(chunk.data)
       print("\n\n")
   ```

```
curl -s --request POST \
    --url "http://localhost:2024/runs/stream" \
    --header 'Content-Type: application/json' \
    --data "{
        \"assistant_id\": \"agent\",
        \"input\": {
            \"messages\": [
                {
                    \"role\": \"human\",
                    \"content\": \"What is LangGraph?\"
                }
            ]
        },
        \"stream_mode\": \"messages-tuple\"
    }"
```

## ​ Next steps

Now that you have a LangGraph app running locally, take your journey further by exploring deployment and advanced features:

* Deployment quickstart: Deploy your LangGraph app using LangSmith.
* LangSmith: Learn about foundational LangSmith concepts.
* SDK Reference: Explore the SDK API Reference.

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Quickstart

Previous

Changelog

Next

⌘I