Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Production

LangSmith Deployment

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
* Deploy your agent
* 1. Create a repository on GitHub
* 2. Deploy to LangSmith
* 3. Test your application in Studio
* 4. Get the API URL for your deployment
* 5. Test the API

Production

# LangSmith Deployment

Copy page

Copy page

This guide shows you how to deploy your agent to **LangSmith Cloud**, a fully managed hosting platform designed for agent workloads. With Cloud deployment, you can deploy directly from your GitHub repository—LangSmith handles the infrastructure, scaling, and operational concerns.
Traditional hosting platforms are built for stateless, short-lived web applications. LangSmith Cloud is **purpose-built for stateful, long-running agents** that require persistent state and background execution.

LangSmith offers multiple deployment options beyond Cloud, including deploying with a control plane (hybrid/self-hosted) or as standalone servers. For more information, refer to the Deployment overview.

## ​ Prerequisites

Before you begin, ensure you have the following:

* A GitHub account
* A LangSmith account (free to sign up)

## ​ Deploy your agent

### ​ 1. Create a repository on GitHub

Your application’s code must reside in a GitHub repository to be deployed on LangSmith. Both public and private repositories are supported. For this quickstart, first make sure your app is LangGraph-compatible by following the local server setup guide. Then, push your code to the repository.

### ​ 2. Deploy to LangSmith

1

Navigate to LangSmith Deployment

Log in to LangSmith. In the left sidebar, select **Deployments**.

2

Create new deployment

Click the **+ New Deployment** button. A pane will open where you can fill in the required fields.

3

Link repository

If you are a first time user or adding a private repository that has not been previously connected, click the **Add new account** button and follow the instructions to connect your GitHub account.

4

Deploy repository

Select your application’s repository. Click **Submit** to deploy. This may take about 15 minutes to complete. You can check the status in the **Deployment details** view.

### ​ 3. Test your application in Studio

Once your application is deployed:

1. Select the deployment you just created to view more details.
2. Click the **Studio** button in the top right corner. Studio will open to display your graph.

### ​ 4. Get the API URL for your deployment

1. In the **Deployment details** view in LangGraph, click the **API URL** to copy it to your clipboard.
2. Click the `URL` to copy it to the clipboard.

### ​ 5. Test the API

You can now test the API:

* Python
* Rest API

1. Install LangGraph SDK:

```
pip install langgraph-sdk
```

2. Send a message to the agent:

```
from langgraph_sdk import get_sync_client # or get_client for async

client = get_sync_client(url="your-deployment-url", api_key="your-langsmith-api-key")

for chunk in client.runs.stream(
    None,    # Threadless run
    "agent", # Name of agent. Defined in langgraph.json.
    input={
        "messages": [{
            "role": "human",
            "content": "What is LangGraph?",
        }],
    },
    stream_mode="updates",
):
    print(f"Receiving new event of type: {chunk.event}...")
    print(chunk.data)
    print("\n\n")
```

```
curl -s --request POST \
    --url <DEPLOYMENT_URL>/runs/stream \
    --header 'Content-Type: application/json' \
    --header "X-Api-Key: <LANGSMITH API KEY> \
    --data "{
        \"assistant_id\": \"agent\", `# Name of agent. Defined in langgraph.json.`
        \"input\": {
            \"messages\": [
                {
                    \"role\": \"human\",
                    \"content\": \"What is LangGraph?\"
                }
            ]
        },
        \"stream_mode\": \"updates\"
    }"
```

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Agent Chat UI

Previous

LangSmith Observability

Next

⌘I