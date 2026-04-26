Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Conceptual overviews

Component architecture

Deep AgentsLangChainLangGraphIntegrationsLearnReferenceContribute

Python



* Learn

##### Tutorials

* Deep Agents
* LangChain
* Multi-agent
* LangGraph

##### Conceptual overviews

* LangChain vs. LangGraph vs. Deep Agents
* Providers and models
* Component architecture
* Memory
* Context
* Graph API
* Functional API

##### Additional resources

* LangChain Academy
* Case studies
* Get help

On this page

* Core component ecosystem
* How components connect
* Component categories
* Common patterns
* RAG (Retrieval-Augmented generation)
* Agent with tools
* Multi-agent system
* Learn more

Conceptual overviews

# Component architecture

Copy page

Copy page

LangChain’s power comes from how its components work together to create sophisticated AI applications. This page provides diagrams showcasing the relationships between different components.

## ​ Core component ecosystem

The diagram below shows how LangChain’s major components connect to form complete AI applications:


### ​ How components connect

Each component layer builds on the previous ones:

1. **Input processing** – Transform raw data into structured documents
2. **Embedding & storage** – Convert text into searchable vector representations
3. **Retrieval** – Find relevant information based on user queries
4. **Generation** – Use AI models to create responses, optionally with tools
5. **Orchestration** – Coordinate everything through agents and memory systems

## ​ Component categories

LangChain organizes components into these main categories:

| Category | Purpose | Key Components | Use Cases |
| --- | --- | --- | --- |
| **Models** | AI reasoning and generation | Chat models, LLMs, Embedding models | Text generation, reasoning, semantic understanding |
| **Tools** | External capabilities | APIs, databases, etc. | Web search, data access, computations |
| **Agents** | Orchestration and reasoning | ReAct agents, tool calling agents | Nondeterministic workflows, decision making |
| **Memory** | Context preservation | Message history, custom state | Conversations, stateful interactions |
| **Retrievers** | Information access | Vector retrievers, web retrievers | RAG, knowledge base search |
| **Document processing** | Data ingestion | Loaders, splitters, transformers | PDF processing, web scraping |
| **Vector Stores** | Semantic search | Chroma, Pinecone, FAISS | Similarity search, embeddings storage |

## ​ Common patterns

### ​ RAG (Retrieval-Augmented generation)

### ​ Agent with tools

### ​ Multi-agent system

## ​ Learn more

* Creating agents
* Working with tools
* Browse integrations

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Providers and models

Previous

Memory overview

Next

⌘I