Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Multi-agent

Skills

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

  + Overview
  + Subagents
  + Handoffs
  + Skills
  + Router
  + Custom workflow
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

* Key characteristics
* When to use
* Basic implementation
* Extending the pattern

Advanced usage

Multi-agent

# Skills

Copy page

Copy page

In the **skills** architecture, specialized capabilities are packaged as invocable “skills” that augment an agent’s behavior. Skills are primarily prompt-driven specializations that an agent can invoke on-demand.
For built-in skill support, see Deep Agents.

This pattern is conceptually identical to Agent Skills and llms.txt (introduced by Jeremy Howard), which uses tool calling for progressive disclosure of documentation. The skills pattern applies progressive disclosure to specialized prompts and domain knowledge rather than just documentation pages.For ready-to-use skills that improve your agent’s performance on LangChain ecosystem tasks, see the LangChain Skills repository.

## ​ Key characteristics

* Prompt-driven specialization: Skills are primarily defined by specialized prompts
* Progressive disclosure: Skills become available based on context or user needs
* Team distribution: Different teams can develop and maintain skills independently
* Lightweight composition: Skills are simpler than full sub-agents
* Reference awareness: Skills can reference scripts, templates, and other resources

## ​ When to use

Use the skills pattern when you want a single agent with many possible specializations, you don’t need to enforce specific constraints between skills, or different teams need to develop capabilities independently. Common examples include coding assistants (skills for different languages or tasks), knowledge bases (skills for different domains), and creative assistants (skills for different formats).

## ​ Basic implementation

```
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt.

    Available skills:
    - write_sql: SQL query writing expert
    - review_legal_doc: Legal document reviewer

    Returns the skill's prompt and context.
    """
    # Load skill content from file/database
    ...

agent = create_agent(
    model="gpt-5.4",
    tools=[load_skill],
    system_prompt=(
        "You are a helpful assistant. "
        "You have access to two skills: "
        "write_sql and review_legal_doc. "
        "Use load_skill to access them."
    ),
)
```

For a complete implementation, see the tutorial below.

## Tutorial: Build a SQL assistant with on-demand skills

Learn how to implement skills with progressive disclosure, where the agent loads specialized prompts and schemas on-demand rather than upfront.

Learn more

## ​ Extending the pattern

When writing custom implementations, you can extend the basic skills pattern in several ways:

* **Dynamic tool registration**: Combine progressive disclosure with state management to register new tools as skills load. For example, loading a “database\_admin” skill could both add specialized context and register database-specific tools (backup, restore, migrate). This uses the same tool-and-state mechanisms used across multi-agent patterns—tools updating state to dynamically change agent capabilities.
* **Hierarchical skills**: Skills can define other skills in a tree structure, creating nested specializations. For instance, loading a “data\_science” skill might make available sub-skills like “pandas\_expert”, “visualization”, and “statistical\_analysis”. Each sub-skill can be loaded independently as needed, allowing for fine-grained progressive disclosure of domain knowledge. This hierarchical approach helps manage large knowledge bases by organizing capabilities into logical groupings that can be discovered and loaded on-demand.
* **Reference awareness**: While each skill only has one prompt, this prompt can reference the location of other assets and provide information on when the agent should use those assets.
  When those assets become relevant, the agent will know that those files exist and read them into memory as needed to complete tasks.
  This also follows the progressive disclosure pattern and limits the information in the context window.

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Handoffs

Previous

Router

Next

⌘I