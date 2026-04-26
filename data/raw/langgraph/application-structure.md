Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Production

Application structure

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

* Key concepts
* File structure
* Configuration file
* Examples
* Dependencies
* Graphs
* Environment variables

Production

# Application structure

Copy page

Copy page

A LangGraph application consists of one or more graphs, a configuration file (`langgraph.json`), a file that specifies dependencies, and an optional `.env` file that specifies environment variables.
This guide shows a typical structure of an application and shows you how to provide the required configuration to deploy an application with LangSmith Deployment.

LangSmith Deployment is a managed hosting platform for deploying and scaling LangGraph agents. It handles the infrastructure, scaling, and operational concerns so you can deploy your stateful, long-running agents directly from your repository. Learn more in the Deployment documentation.

## ​ Key concepts

To deploy using the LangSmith, the following information should be provided:

1. A LangGraph configuration file (`langgraph.json`) that specifies the dependencies, graphs, and environment variables to use for the application.
2. The graphs that implement the logic of the application.
3. A file that specifies dependencies required to run the application.
4. Environment variables that are required for the application to run.

## ​ File structure

Below are examples of directory structures for applications:

* Python (requirements.txt)
* Python (pyproject.toml)

```
my-app/
├── my_agent # all project code lies within here
│   ├── utils # utilities for your graph
│   │   ├── __init__.py
│   │   ├── tools.py # tools for your graph
│   │   ├── nodes.py # node functions for your graph
│   │   └── state.py # state definition of your graph
│   ├── __init__.py
│   └── agent.py # code for constructing your graph
├── .env # environment variables
├── requirements.txt # package dependencies
└── langgraph.json # configuration file for LangGraph
```

```
my-app/
├── my_agent # all project code lies within here
│   ├── utils # utilities for your graph
│   │   ├── __init__.py
│   │   ├── tools.py # tools for your graph
│   │   ├── nodes.py # node functions for your graph
│   │   └── state.py # state definition of your graph
│   ├── __init__.py
│   └── agent.py # code for constructing your graph
├── .env # environment variables
├── langgraph.json  # configuration file for LangGraph
└── pyproject.toml # dependencies for your project
```

The directory structure of a LangGraph application can vary depending on the programming language and the package manager used.

## ​ Configuration file

The `langgraph.json` file is a JSON file that specifies the dependencies, graphs, environment variables, and other settings required to deploy a LangGraph application.
See the LangGraph configuration file reference for details on all supported keys in the JSON file.

The LangGraph CLI defaults to using the configuration file `langgraph.json` in the current directory.

### ​ Examples

* The dependencies involve a custom local package and the `langchain_openai` package.
* A single graph will be loaded from the file `./your_package/your_file.py` with the variable `variable`.
* The environment variables are loaded from the `.env` file.

```
{
  "dependencies": ["langchain_openai", "./your_package"],
  "graphs": {
    "my_agent": "./your_package/your_file.py:agent"
  },
  "env": "./.env"
}
```

## ​ Dependencies

A LangGraph application may depend on other Python packages.
You will generally need to specify the following information for dependencies to be set up correctly:

1. A file in the directory that specifies the dependencies (e.g. `requirements.txt`, `pyproject.toml`, or `package.json`).
2. A `dependencies` key in the LangGraph configuration file that specifies the dependencies required to run the LangGraph application.
3. Any additional binaries or system libraries can be specified using `dockerfile_lines` key in the LangGraph configuration file.

## ​ Graphs

Use the `graphs` key in the LangGraph configuration file to specify which graphs will be available in the deployed LangGraph application.
You can specify one or more graphs in the configuration file. Each graph is identified by a name (which should be unique) and a path for either: (1) the compiled graph or (2) a function that makes a graph is defined.

## ​ Environment variables

If you’re working with a deployed LangGraph application locally, you can configure environment variables in the `env` key of the LangGraph configuration file.
For a production deployment, you will typically want to configure the environment variables in the deployment environment.


---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Subgraphs

Previous

Test

Next

⌘I