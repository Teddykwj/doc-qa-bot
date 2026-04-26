Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Middleware

Prebuilt middleware

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

* Provider-agnostic middleware
* Summarization
* Human-in-the-loop
* Model call limit
* Tool call limit
* Model fallback
* PII detection
* Custom PII types
* To-do list
* LLM tool selector
* Tool retry
* Model retry
* LLM tool emulator
* Context editing
* Shell tool
* File search
* Filesystem middleware
* Short-term vs. long-term filesystem
* Subagent
* Provider-specific middleware

Middleware

# Prebuilt middleware

Copy page

Prebuilt middleware for common agent use cases

Copy page

LangChain and Deep Agents provide prebuilt middleware for common use cases. Each middleware is production-ready and configurable for your specific needs.

## ​ Provider-agnostic middleware

The following middleware work with any LLM provider:

| Middleware | Description |
| --- | --- |
| Summarization | Automatically summarize conversation history when approaching token limits. |
| Human-in-the-loop | Pause execution for human approval of tool calls. |
| Model call limit | Limit the number of model calls to prevent excessive costs. |
| Tool call limit | Control tool execution by limiting call counts. |
| Model fallback | Automatically fallback to alternative models when primary fails. |
| PII detection | Detect and handle Personally Identifiable Information (PII). |
| To-do list | Equip agents with task planning and tracking capabilities. |
| LLM tool selector | Use an LLM to select relevant tools before calling main model. |
| Tool retry | Automatically retry failed tool calls with exponential backoff. |
| Model retry | Automatically retry failed model calls with exponential backoff. |
| LLM tool emulator | Emulate tool execution using an LLM for testing purposes. |
| Context editing | Manage conversation context by trimming or clearing tool uses. |
| Shell tool | Expose a persistent shell session to agents for command execution. |
| File search | Provide Glob and Grep search tools over filesystem files. |
| Filesystem | Provide agents with a filesystem for storing context and long-term memories. |
| Subagent | Add the ability to spawn subagents. |

### ​ Summarization

Automatically summarize conversation history when approaching token limits, preserving recent messages while compressing older context. Summarization is useful for the following:

* Long-running conversations that exceed context windows.
* Multi-turn dialogues with extensive history.
* Applications where preserving full conversation context matters.

**API reference:** `SummarizationMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)
```

Configuration options

The `fraction` conditions for `trigger` and `keep` (shown below) rely on a chat model’s profile data if using `langchain>=1.1`. If data are not available, use another condition or specify manually:

```
from langchain.chat_models import init_chat_model

custom_profile = {
    "max_input_tokens": 100_000,
    # ...
}
model = init_chat_model("gpt-5.4", profile=custom_profile)
```

​

model

string | BaseChatModel

required

Model for generating summaries. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance. See `init_chat_model` for more information.

​

trigger

ContextSize | list[ContextSize] | None

Condition(s) for triggering summarization. Can be:

* A single `ContextSize` tuple (specified condition must be met)
* A list of `ContextSize` tuples (any condition must be met - OR logic)

Condition should be one of the following:

* `fraction` (float): Fraction of model’s context size (0-1)
* `tokens` (int): Absolute token count
* `messages` (int): Message count

At least one condition must be specified. If not provided, summarization will not trigger automatically.See the API reference for `ContextSize` for more information.

​

keep

ContextSize

default:"('messages', 20)"

How much context to preserve after summarization. Specify exactly one of:

* `fraction` (float): Fraction of model’s context size to keep (0-1)
* `tokens` (int): Absolute token count to keep
* `messages` (int): Number of recent messages to keep

See the API reference for `ContextSize` for more information.

​

token\_counter

function

Custom token counting function. Defaults to character-based counting.

​

summary\_prompt

string

Custom prompt template for summarization. Uses built-in template if not specified. The template should include `{messages}` placeholder where conversation history will be inserted.

​

trim\_tokens\_to\_summarize

number

default:"4000"

Maximum number of tokens to include when generating the summary. Messages will be trimmed to fit this limit before summarization.

​

summary\_prefix

string

deprecated

**Deprecated:** Use `summary_prompt` to provide the full prompt instead.

​

max\_tokens\_before\_summary

number

deprecated

**Deprecated:** Use `trigger: ("tokens", value)` instead. Token threshold for triggering summarization.

​

messages\_to\_keep

number

deprecated

**Deprecated:** Use `keep: ("messages", value)` instead. Recent messages to preserve.



Full example

The summarization middleware monitors message token counts and automatically summarizes older messages when thresholds are reached.**Trigger conditions** control when summarization runs:

* Single condition object (specified must be met)
* Array of conditions (any condition must be met - OR logic)
* Each condition can use `fraction` (of model’s context size), `tokens` (absolute count), or `messages` (message count)

**Keep condition** control how much context to preserve (specify exactly one):

* `fraction` - Fraction of model’s context size to keep
* `tokens` - Absolute token count to keep
* `messages` - Number of recent messages to keep

```
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware


# Single condition: trigger if tokens >= 4000
agent = create_agent(
    model="gpt-5.4",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)

# Multiple conditions: trigger if number of tokens >= 3000 OR messages >= 6
agent2 = create_agent(
    model="gpt-5.4",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=[
                ("tokens", 3000),
                ("messages", 6),
            ],
            keep=("messages", 20),
        ),
    ],
)

# Using fractional limits
agent3 = create_agent(
    model="gpt-5.4",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("fraction", 0.8),
            keep=("fraction", 0.3),
        ),
    ],
)
```

### ​ Human-in-the-loop

Pause agent execution for human approval, editing, or rejection of tool calls before they execute. Human-in-the-loop is useful for the following:

* High-stakes operations requiring human approval (e.g. database writes, financial transactions).
* Compliance workflows where human oversight is mandatory.
* Long-running conversations where human feedback guides the agent.

**API reference:** `HumanInTheLoopMiddleware`

Human-in-the-loop middleware requires a checkpointer to maintain state across interruptions.

```
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver


def your_read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

def your_send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

agent = create_agent(
    model="gpt-5.4",
    tools=[your_read_email_tool, your_send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "your_send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_read_email_tool": False,
            }
        ),
    ],
)
```

For complete examples, configuration options, and integration patterns, see the Human-in-the-loop documentation.

Watch this video guide demonstrating Human-in-the-loop middleware behavior.

### ​ Model call limit

Limit the number of model calls to prevent infinite loops or excessive costs. Model call limit is useful for the following:

* Preventing runaway agents from making too many API calls.
* Enforcing cost controls on production deployments.
* Testing agent behavior within specific call budgets.

**API reference:** `ModelCallLimitMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="gpt-5.4",
    checkpointer=InMemorySaver(),  # Required for thread limiting
    tools=[],
    middleware=[
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
    ],
)
```

Watch this video guide demonstrating Model Call Limit middleware behavior.

Configuration options

​

thread\_limit

number

Maximum model calls across all runs in a thread. Defaults to no limit.

​

run\_limit

number

Maximum model calls per single invocation. Defaults to no limit.

​

exit\_behavior

string

default:"end"

Behavior when limit is reached. Options: `'end'` (graceful termination) or `'error'` (raise exception)

### ​ Tool call limit

Control agent execution by limiting the number of tool calls, either globally across all tools or for specific tools. Tool call limits are useful for the following:

* Preventing excessive calls to expensive external APIs.
* Limiting web searches or database queries.
* Enforcing rate limits on specific tool usage.
* Protecting against runaway agent loops.

**API reference:** `ToolCallLimitMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool, database_tool],
    middleware=[
        # Global limit
        ToolCallLimitMiddleware(thread_limit=20, run_limit=10),
        # Tool-specific limit
        ToolCallLimitMiddleware(
            tool_name="search",
            thread_limit=5,
            run_limit=3,
        ),
    ],
)
```

Watch this video guide demonstrating Tool Call Limit middleware behavior.

Configuration options

​

tool\_name

string

Name of specific tool to limit. If not provided, limits apply to **all tools globally**.

​

thread\_limit

number

Maximum tool calls across all runs in a thread (conversation). Persists across multiple invocations with the same thread ID. Requires a checkpointer to maintain state. `None` means no thread limit.

​

run\_limit

number

Maximum tool calls per single invocation (one user message → response cycle). Resets with each new user message. `None` means no run limit.**Note:** At least one of `thread_limit` or `run_limit` must be specified.

​

exit\_behavior

string

default:"continue"

Behavior when limit is reached:

* `'continue'` (default) - Block exceeded tool calls with error messages, let other tools and the model continue. The model decides when to end based on the error messages.
* `'error'` - Raise a `ToolCallLimitExceededError` exception, stopping execution immediately
* `'end'` - Stop execution immediately with a `ToolMessage` and AI message for the exceeded tool call. Only works when limiting a single tool; raises `NotImplementedError` if other tools have pending calls.



Full example

Specify limits with:

* **Thread limit** - Max calls across all runs in a conversation (requires checkpointer)
* **Run limit** - Max calls per single invocation (resets each turn)

Exit behaviors:

* `'continue'` (default) - Block exceeded calls with error messages, agent continues
* `'error'` - Raise exception immediately
* `'end'` - Stop with ToolMessage + AI message (single-tool scenarios only)

```
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware


global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)
search_limiter = ToolCallLimitMiddleware(tool_name="search", thread_limit=5, run_limit=3)
database_limiter = ToolCallLimitMiddleware(tool_name="query_database", thread_limit=10)
strict_limiter = ToolCallLimitMiddleware(tool_name="scrape_webpage", run_limit=2, exit_behavior="error")

agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool, database_tool, scraper_tool],
    middleware=[global_limiter, search_limiter, database_limiter, strict_limiter],
)
```

### ​ Model fallback

Automatically fallback to alternative models when the primary model fails. Model fallback is useful for the following:

* Building resilient agents that handle model outages.
* Cost optimization by falling back to cheaper models.
* Provider redundancy across OpenAI, Anthropic, etc.

**API reference:** `ModelFallbackMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        ModelFallbackMiddleware(
            "gpt-5.4-mini",
            "claude-3-5-sonnet-20241022",
        ),
    ],
)
```

Watch this video guide demonstrating Model Fallback middleware behavior.

Configuration options

​

first\_model

string | BaseChatModel

required

First fallback model to try when the primary model fails. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance.

​

\*additional\_models

string | BaseChatModel

Additional fallback models to try in order if previous models fail

### ​ PII detection

Detect and handle Personally Identifiable Information (PII) in conversations using configurable strategies. PII detection is useful for the following:

* Healthcare and financial applications with compliance requirements.
* Customer service agents that need to sanitize logs.
* Any application handling sensitive user data.

**API reference:** `PIIMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
)
```

#### ​ Custom PII types

You can create custom PII types by providing a `detector` parameter. This allows you to detect patterns specific to your use case beyond the built-in types.
**Three ways to create custom detectors:**

1. **Regex pattern string** - Simple pattern matching
2. **Custom function** - Complex detection logic with validation

```
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
import re


# Method 1: Regex pattern string
agent1 = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
        ),
    ],
)

# Method 2: Compiled regex pattern
agent2 = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        PIIMiddleware(
            "phone_number",
            detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"),
            strategy="mask",
        ),
    ],
)

# Method 3: Custom detector function
def detect_ssn(content: str) -> list[dict[str, str | int]]:
    """Detect SSN with validation.

    Returns a list of dictionaries with 'text', 'start', and 'end' keys.
    """
    import re
    matches = []
    pattern = r"\d{3}-\d{2}-\d{4}"
    for match in re.finditer(pattern, content):
        ssn = match.group(0)
        # Validate: first 3 digits shouldn't be 000, 666, or 900-999
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "text": ssn,
                "start": match.start(),
                "end": match.end(),
            })
    return matches

agent3 = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        PIIMiddleware(
            "ssn",
            detector=detect_ssn,
            strategy="hash",
        ),
    ],
)
```

**Custom detector function signature:**
The detector function must accept a string (content) and return matches:
Returns a list of dictionaries with `text`, `start`, and `end` keys:

```
def detector(content: str) -> list[dict[str, str | int]]:
    return [
        {"text": "matched_text", "start": 0, "end": 12},
        # ... more matches
    ]
```

For custom detectors:

* Use regex strings for simple patterns
* Use RegExp objects when you need flags (e.g., case-insensitive matching)
* Use custom functions when you need validation logic beyond pattern matching
* Custom functions give you full control over detection logic and can implement complex validation rules

Configuration options

​

pii\_type

string

required

Type of PII to detect. Can be a built-in type (`email`, `credit_card`, `ip`, `mac_address`, `url`) or a custom type name.

​

strategy

string

default:"redact"

How to handle detected PII. Options:

* `'block'` - Raise exception when detected
* `'redact'` - Replace with `[REDACTED_{PII_TYPE}]`
* `'mask'` - Partially mask (e.g., `****-****-****-1234`)
* `'hash'` - Replace with deterministic hash

​

detector

function | regex

Custom detector function or regex pattern. If not provided, uses built-in detector for the PII type.

​

apply\_to\_input

boolean

default:"True"

Check user messages before model call

​

apply\_to\_output

boolean

default:"False"

Check AI messages after model call

​

apply\_to\_tool\_results

boolean

default:"False"

Check tool result messages after execution

### ​ To-do list

Equip agents with task planning and tracking capabilities for complex multi-step tasks. To-do lists are useful for the following:

* Complex multi-step tasks requiring coordination across multiple tools.
* Long-running operations where progress visibility is important.

This middleware automatically provides agents with a `write_todos` tool and system prompts to guide effective task planning.

**API reference:** `TodoListMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[read_file, write_file, run_tests],
    middleware=[TodoListMiddleware()],
)
```

Watch this video guide demonstrating To-do List middleware behavior.

Configuration options

​

system\_prompt

string

Custom system prompt for guiding todo usage. Uses built-in prompt if not specified.

​

tool\_description

string

Custom description for the `write_todos` tool. Uses built-in description if not specified.

### ​ LLM tool selector

Use an LLM to intelligently select relevant tools before calling the main model. LLM tool selectors are useful for the following:

* Agents with many tools (10+) where most aren’t relevant per query.
* Reducing token usage by filtering irrelevant tools.
* Improving model focus and accuracy.

This middleware uses structured output to ask an LLM which tools are most relevant for the current query. The structured output schema defines the available tool names and descriptions. Model providers often add this structured output information to the system prompt behind the scenes.
**API reference:** `LLMToolSelectorMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolSelectorMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[tool1, tool2, tool3, tool4, tool5, ...],
    middleware=[
        LLMToolSelectorMiddleware(
            model="gpt-5.4-mini",
            max_tools=3,
            always_include=["search"],
        ),
    ],
)
```

Configuration options

​

model

string | BaseChatModel

Model for tool selection. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance. See `init_chat_model` for more information.Defaults to the agent’s main model.

​

system\_prompt

string

Instructions for the selection model. Uses built-in prompt if not specified.

​

max\_tools

number

Maximum number of tools to select. If the model selects more, only the first max\_tools will be used. No limit if not specified.

​

always\_include

list[string]

Tool names to always include regardless of selection. These do not count against the max\_tools limit.

### ​ Tool retry

Automatically retry failed tool calls with configurable exponential backoff. Tool retry is useful for the following:

* Handling transient failures in external API calls.
* Improving reliability of network-dependent tools.
* Building resilient agents that gracefully handle temporary errors.

**API reference:** `ToolRetryMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool, database_tool],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```

Configuration options

​

max\_retries

number

default:"2"

Maximum number of retry attempts after the initial call (3 total attempts with default)

​

tools

list[BaseTool | str]

Optional list of tools or tool names to apply retry logic to. If `None`, applies to all tools.

​

retry\_on

tuple[type[Exception], ...] | callable

default:"(Exception,)"

Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried.

​

on\_failure

string | callable

default:"return\_message"

Behavior when all retries are exhausted. Options:

* `'return_message'` - Return a `ToolMessage` with error details (allows LLM to handle failure)
* `'raise'` - Re-raise the exception (stops agent execution)
* Custom callable - Function that takes the exception and returns a string for the `ToolMessage` content

​

backoff\_factor

number

default:"2.0"

Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.

​

initial\_delay

number

default:"1.0"

Initial delay in seconds before first retry

​

max\_delay

number

default:"60.0"

Maximum delay in seconds between retries (caps exponential backoff growth)

​

jitter

boolean

default:"true"

Whether to add random jitter (`±25%`) to delay to avoid thundering herd



Full example

The middleware automatically retries failed tool calls with exponential backoff.**Key configuration:**

* `max_retries` - Number of retry attempts (default: 2)
* `backoff_factor` - Multiplier for exponential backoff (default: 2.0)
* `initial_delay` - Starting delay in seconds (default: 1.0)
* `max_delay` - Cap on delay growth (default: 60.0)
* `jitter` - Add random variation (default: True)

**Failure handling:**

* `on_failure='return_message'` - Return error message
* `on_failure='raise'` - Re-raise exception
* Custom function - Function returning error message

```
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware


agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool, database_tool, api_tool],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
            max_delay=60.0,
            jitter=True,
            tools=["api_tool"],
            retry_on=(ConnectionError, TimeoutError),
            on_failure="continue",
        ),
    ],
)
```

### ​ Model retry

Automatically retry failed model calls with configurable exponential backoff. Model retry is useful for the following:

* Handling transient failures in model API calls.
* Improving reliability of network-dependent model requests.
* Building resilient agents that gracefully handle temporary model errors.

**API reference:** `ModelRetryMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool, database_tool],
    middleware=[
        ModelRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```

Configuration options

​

max\_retries

number

default:"2"

Maximum number of retry attempts after the initial call (3 total attempts with default)

​

retry\_on

tuple[type[Exception], ...] | callable

default:"(Exception,)"

Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried.

​

on\_failure

string | callable

default:"continue"

Behavior when all retries are exhausted. Options:

* `'continue'` (default) - Return an `AIMessage` with error details, allowing the agent to potentially handle the failure gracefully
* `'error'` - Re-raise the exception (stops agent execution)
* Custom callable - Function that takes the exception and returns a string for the `AIMessage` content

​

backoff\_factor

number

default:"2.0"

Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.

​

initial\_delay

number

default:"1.0"

Initial delay in seconds before first retry

​

max\_delay

number

default:"60.0"

Maximum delay in seconds between retries (caps exponential backoff growth)

​

jitter

boolean

default:"true"

Whether to add random jitter (`±25%`) to delay to avoid thundering herd



Full example

The middleware automatically retries failed model calls with exponential backoff.

```
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware


# Basic usage with default settings (2 retries, exponential backoff)
agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool],
    middleware=[ModelRetryMiddleware()],
)

# Custom exception filtering
class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

class ConnectionError(Exception):
    """Custom exception for connection errors."""
    pass

# Retry specific exceptions only
retry = ModelRetryMiddleware(
    max_retries=4,
    retry_on=(TimeoutError, ConnectionError),
    backoff_factor=1.5,
)


def should_retry(error: Exception) -> bool:
    # Only retry on rate limit errors
    if isinstance(error, TimeoutError):
        return True
    # Or check for specific HTTP status codes
    if hasattr(error, "status_code"):
        return error.status_code in (429, 503)
    return False

retry_with_filter = ModelRetryMiddleware(
    max_retries=3,
    retry_on=should_retry,
)

# Return error message instead of raising
retry_continue = ModelRetryMiddleware(
    max_retries=4,
    on_failure="continue",  # Return AIMessage with error instead of raising
)

# Custom error message formatting
def format_error(error: Exception) -> str:
    return f"Model call failed: {error}. Please try again later."

retry_with_formatter = ModelRetryMiddleware(
    max_retries=4,
    on_failure=format_error,
)

# Constant backoff (no exponential growth)
constant_backoff = ModelRetryMiddleware(
    max_retries=5,
    backoff_factor=0.0,  # No exponential growth
    initial_delay=2.0,  # Always wait 2 seconds
)

# Raise exception on failure
strict_retry = ModelRetryMiddleware(
    max_retries=2,
    on_failure="error",  # Re-raise exception instead of returning message
)
```

### ​ LLM tool emulator

Emulate tool execution using an LLM for testing purposes, replacing actual tool calls with AI-generated responses. LLM tool emulators are useful for the following:

* Testing agent behavior without executing real tools.
* Developing agents when external tools are unavailable or expensive.
* Prototyping agent workflows before implementing actual tools.

**API reference:** `LLMToolEmulator`

```
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator

agent = create_agent(
    model="gpt-5.4",
    tools=[get_weather, search_database, send_email],
    middleware=[
        LLMToolEmulator(),  # Emulate all tools
    ],
)
```

Configuration options

​

tools

list[str | BaseTool]

List of tool names (str) or BaseTool instances to emulate. If `None` (default), ALL tools will be emulated. If empty list `[]`, no tools will be emulated. If array with tool names/instances, only those tools will be emulated.

​

model

string | BaseChatModel

Model to use for generating emulated tool responses. Can be a model identifier string (e.g., `'google_genai:gemini-3.1-pro-preview'`) or a `BaseChatModel` instance. Defaults to the agent’s model if not specified. See `init_chat_model` for more information.



Full example

The middleware uses an LLM to generate plausible responses for tool calls instead of executing the actual tools.

```
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator
from langchain.tools import tool


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return "Email sent"


# Emulate all tools (default behavior)
agent = create_agent(
    model="gpt-5.4",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator()],
)

# Emulate specific tools only
agent2 = create_agent(
    model="gpt-5.4",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator(tools=["get_weather"])],
)

# Use custom model for emulation
agent4 = create_agent(
    model="gpt-5.4",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator(model="claude-sonnet-4-6")],
)
```

### ​ Context editing

Manage conversation context by clearing older tool call outputs when token limits are reached, while preserving recent results. This helps keep context windows manageable in long conversations with many tool calls. Context editing is useful for the following:

* Long conversations with many tool calls that exceed token limits
* Reducing token costs by removing older tool outputs that are no longer relevant
* Maintaining only the most recent N tool results in context

**API reference:** `ContextEditingMiddleware`, `ClearToolUsesEdit`

```
from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=100000,
                    keep=3,
                ),
            ],
        ),
    ],
)
```

Configuration options

​

edits

list[ContextEdit]

default:"[ClearToolUsesEdit()]"

List of `ContextEdit` strategies to apply

​

token\_count\_method

string

default:"approximate"

Token counting method. Options: `'approximate'` or `'model'`

**`ClearToolUsesEdit` options:**

​

trigger

number

default:"100000"

Token count that triggers the edit. When the conversation exceeds this token count, older tool outputs will be cleared.

​

clear\_at\_least

number

default:"0"

Minimum number of tokens to reclaim when the edit runs. If set to 0, clears as much as needed.

​

keep

number

default:"3"

Number of most recent tool results that must be preserved. These will never be cleared.

​

clear\_tool\_inputs

boolean

default:"False"

Whether to clear the originating tool call parameters on the AI message. When `True`, tool call arguments are replaced with empty objects.

​

exclude\_tools

list[string]

default:"()"

List of tool names to exclude from clearing. These tools will never have their outputs cleared.

​

placeholder

string

default:"[cleared]"

Placeholder text inserted for cleared tool outputs. This replaces the original tool message content.



Full example

The middleware applies context editing strategies when token limits are reached. The most common strategy is `ClearToolUsesEdit`, which clears older tool results while preserving recent ones.**How it works:**

1. Monitor token count in conversation
2. When threshold is reached, clear older tool outputs
3. Keep most recent N tool results
4. Optionally preserve tool call arguments for context

```
from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit


agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool, your_calculator_tool, database_tool],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=2000,
                    keep=3,
                    clear_tool_inputs=False,
                    exclude_tools=[],
                    placeholder="[cleared]",
                ),
            ],
        ),
    ],
)
```

### ​ Shell tool

Expose a persistent shell session to agents for command execution. Shell tool middleware is useful for the following:

* Agents that need to execute system commands
* Development and deployment automation tasks
* Testing and validation workflows
* File system operations and script execution

**Security consideration**: Use appropriate execution policies (`HostExecutionPolicy`, `DockerExecutionPolicy`, or `CodexSandboxExecutionPolicy`) to match your deployment’s security requirements.

**Limitation**: Persistent shell sessions do not currently work with interrupts (human-in-the-loop). We anticipate adding support for this in the future.

**API reference:** `ShellToolMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
)

agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            execution_policy=HostExecutionPolicy(),
        ),
    ],
)
```

Configuration options

​

workspace\_root

str | Path | None

Base directory for the shell session. If omitted, a temporary directory is created when the agent starts and removed when it ends.

​

startup\_commands

tuple[str, ...] | list[str] | str | None

Optional commands executed sequentially after the session starts

​

shutdown\_commands

tuple[str, ...] | list[str] | str | None

Optional commands executed before the session shuts down

​

execution\_policy

BaseExecutionPolicy | None

Execution policy controlling timeouts, output limits, and resource configuration. Options:

* `HostExecutionPolicy` - Full host access (default); best for trusted environments where the agent already runs inside a container or VM
* `DockerExecutionPolicy` - Launches a separate Docker container for each agent run, providing harder isolation
* `CodexSandboxExecutionPolicy` - Reuses the Codex CLI sandbox for additional syscall/filesystem restrictions

​

redaction\_rules

tuple[RedactionRule, ...] | list[RedactionRule] | None

Optional redaction rules to sanitize command output before returning it to the model.

Redaction rules are applied post execution and do not prevent exfiltration of secrets or sensitive data when using `HostExecutionPolicy`.

​

tool\_description

str | None

Optional override for the registered shell tool description

​

shell\_command

Sequence[str] | str | None

Optional shell executable (string) or argument sequence used to launch the persistent session. Defaults to `/bin/bash`.

​

env

Mapping[str, Any] | None

Optional environment variables to supply to the shell session. Values are coerced to strings before command execution.



Full example

The middleware provides a single persistent shell session that agents can use to execute commands sequentially.**Execution policies:**

* `HostExecutionPolicy` (default) - Native execution with full host access
* `DockerExecutionPolicy` - Isolated Docker container execution
* `CodexSandboxExecutionPolicy` - Sandboxed execution via Codex CLI

```
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
    DockerExecutionPolicy,
    RedactionRule,
)


# Basic shell tool with host execution
agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            execution_policy=HostExecutionPolicy(),
        ),
    ],
)

# Docker isolation with startup commands
agent_docker = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            startup_commands=["pip install requests", "export PYTHONPATH=/workspace"],
            execution_policy=DockerExecutionPolicy(
                image="python:3.11-slim",
                command_timeout=60.0,
            ),
        ),
    ],
)

# With output redaction (applied post execution)
agent_redacted = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            redaction_rules=[
                RedactionRule(pii_type="api_key", detector=r"sk-[a-zA-Z0-9]{32}"),
            ],
        ),
    ],
)
```

### ​ File search

Provide Glob and Grep search tools over a filesystem. File search middleware is useful for the following:

* Code exploration and analysis
* Finding files by name patterns
* Searching code content with regex
* Large codebases where file discovery is needed

**API reference:** `FilesystemFileSearchMiddleware`

```
from langchain.agents import create_agent
from langchain.agents.middleware import FilesystemFileSearchMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
        ),
    ],
)
```

Configuration options

​

root\_path

str

required

Root directory to search. All file operations are relative to this path.

​

use\_ripgrep

bool

default:"True"

Whether to use ripgrep for search. Falls back to Python regex if ripgrep is unavailable.

​

max\_file\_size\_mb

int

default:"10"

Maximum file size to search in MB. Files larger than this are skipped.



Full example

The middleware adds two search tools to agents:**Glob tool** - Fast file pattern matching:

* Supports patterns like `**/*.py`, `src/**/*.ts`
* Returns matching file paths sorted by modification time

**Grep tool** - Content search with regex:

* Full regex syntax support
* Filter by file patterns with `include` parameter
* Three output modes: `files_with_matches`, `content`, `count`

```
from langchain.agents import create_agent
from langchain.agents.middleware import FilesystemFileSearchMiddleware
from langchain.messages import HumanMessage


agent = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
            max_file_size_mb=10,
        ),
    ],
)

# Agent can now use glob_search and grep_search tools
result = agent.invoke({
    "messages": [HumanMessage("Find all Python files containing 'async def'")]
})

# The agent will use:
# 1. glob_search(pattern="**/*.py") to find Python files
# 2. grep_search(pattern="async def", include="*.py") to find async functions
```

### ​ Filesystem middleware

Context engineering is a main challenge in building effective agents. This is particularly difficult when using tools that return variable-length results (for example, `web_search` and RAG), as long tool results can quickly fill your context window.
`FilesystemMiddleware` from Deep Agents provides four tools for interacting with both short-term and long-term memory:

* `ls`: List the files in the filesystem
* `read_file`: Read an entire file or a certain number of lines from a file
* `write_file`: Write a new file to the filesystem
* `edit_file`: Edit an existing file in the filesystem

```
from langchain.agents import create_agent
from deepagents.middleware.filesystem import FilesystemMiddleware

# FilesystemMiddleware is included by default in create_deep_agent
# You can customize it if building a custom agent
agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        FilesystemMiddleware(
            backend=None,  # Optional: custom backend (defaults to StateBackend)
            system_prompt="Write to the filesystem when...",  # Optional custom addition to the system prompt
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            }  # Optional: Custom descriptions for filesystem tools
        ),
    ],
)
```

#### ​ Short-term vs. long-term filesystem

By default, these tools write to a local “filesystem” in your graph state. To enable persistent storage across threads, configure a `CompositeBackend` that routes specific paths (like `/memories/`) to a `StoreBackend`.

```
from langchain.agents import create_agent
from deepagents.middleware import FilesystemMiddleware
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

agent = create_agent(
    model="claude-sonnet-4-6",
    store=store,
    middleware=[
        FilesystemMiddleware(
            backend=CompositeBackend(
                default=StateBackend(),
                routes={"/memories/": StoreBackend()}
            ),
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            }  # Optional: Custom descriptions for filesystem tools
        ),
    ],
)
```

When you configure a `CompositeBackend` with a `StoreBackend` for `/memories/`, any files prefixed with **/memories/** are saved to persistent storage and survive across different threads. Files without this prefix remain in ephemeral state storage.

### ​ Subagent

Handing off tasks to subagents isolates context, keeping the main (supervisor) agent’s context window clean while still going deep on a task.
The subagents middleware from Deep Agents allows you to supply subagents through a `task` tool.

```
from langchain.tools import tool
from langchain.agents import create_agent
from deepagents.middleware.subagents import SubAgentMiddleware


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."

agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        SubAgentMiddleware(
            default_model="claude-sonnet-4-6",
            default_tools=[],
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": "Use the get_weather tool to get the weather in a city.",
                    "tools": [get_weather],
                    "model": "gpt-5.4",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

A subagent is defined with a **name**, **description**, **system prompt**, and **tools**. You can also provide a subagent with a custom **model**, or with additional **middleware**. This can be particularly useful when you want to give the subagent an additional state key to share with the main agent.
For more complex use cases, you can also provide your own prebuilt LangGraph graph as a subagent.

```
from langchain.agents import create_agent
from deepagents.middleware.subagents import SubAgentMiddleware
from deepagents import CompiledSubAgent
from langgraph.graph import StateGraph

# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(...)
    # Build your custom graph
    return workflow.compile()

weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph
)

agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        SubAgentMiddleware(
            default_model="claude-sonnet-4-6",
            default_tools=[],
            subagents=[weather_subagent],
        )
    ],
)
```

In addition to any user-defined subagents, the main agent has access to a `general-purpose` subagent at all times. This subagent has the same instructions as the main agent and all the tools it has access to. The primary purpose of the `general-purpose` subagent is context isolation—the main agent can delegate a complex task to this subagent and get a concise answer back without bloat from intermediate tool calls.

## ​ Provider-specific middleware

These middleware are optimized for specific LLM providers. See each provider’s documentation for full details and examples.

![https://mintcdn.com/langchain-5e9cc07a/y4fKEo7ANyWBQMjp/images/providers/anthropic-icon.svg?fit=max&auto=format&n=y4fKEo7ANyWBQMjp&q=85&s=9212db764598a2d3f02f471b5436ae9e](https://mintcdn.com/langchain-5e9cc07a/y4fKEo7ANyWBQMjp/images/providers/anthropic-icon.svg?fit=max&auto=format&n=y4fKEo7ANyWBQMjp&q=85&s=9212db764598a2d3f02f471b5436ae9e)

## Anthropic

Prompt caching, bash tool, text editor, memory, and file search middleware for Claude models.

## AWS

Prompt caching middleware for Amazon Bedrock models.

## OpenAI

Content moderation middleware for OpenAI models.

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Overview

Previous

Custom middleware

Next

⌘I