Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Core components

Structured output

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

* Response format
* Provider strategy
* Tool calling strategy
* Custom tool message content
* Error handling
* Multiple structured outputs error
* Schema validation error
* Error handling strategies

Core components

# Structured output

Copy page

Copy page

Structured output allows agents to return data in a specific, predictable format. Instead of parsing natural language responses, you get structured data in the form of JSON objects, Pydantic models, or dataclasses that your application can use directly.

This page covers structured output with agents using `create_agent`. To use structured output directly on a model (outside of agents), see Models - Structured output.

LangChain’s `create_agent` handles structured output automatically. The user sets their desired structured output schema, and when the model generates the structured data, it’s captured, validated, and returned in the `'structured_response'` key of the agent’s state.

```
def create_agent(
    ...
    response_format: Union[
        ToolStrategy[StructuredResponseT],
        ProviderStrategy[StructuredResponseT],
        type[StructuredResponseT],
        None,
    ]
```

## ​ Response format

Use `response_format` to control how the agent returns structured data:

* **`ToolStrategy[StructuredResponseT]`**: Uses tool calling for structured output
* **`ProviderStrategy[StructuredResponseT]`**: Uses provider-native structured output
* **`type[StructuredResponseT]`**: Schema type - automatically selects best strategy based on model capabilities
* **`None`**: Structured output not explicitly requested

When a schema type is provided directly, LangChain automatically chooses:

* `ProviderStrategy` if the model and provider chosen supports native structured output (e.g. OpenAI, Anthropic (Claude), or xAI (Grok)).
* `ToolStrategy` for all other models.

Support for native structured output features is read dynamically from the model’s profile data if using `langchain>=1.1`. If data are not available, use another condition or specify manually:

```
custom_profile = {
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
```

If tools are specified, the model must support simultaneous use of tools and structured output.

The structured response is returned in the `structured_response` key of the agent’s final state.

## ​ Provider strategy

Some model providers support structured output natively through their APIs (e.g. OpenAI, xAI (Grok), Gemini, Anthropic (Claude)). This is the most reliable method when available.
To use this strategy, configure a `ProviderStrategy`:

```
class ProviderStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    strict: bool | None = None
```

The `strict` param requires `langchain>=1.2`.

​

schema

required

The schema defining the structured output format. Supports:

* **Pydantic models**: `BaseModel` subclasses with field validation. Returns validated Pydantic instance.
* **Dataclasses**: Python dataclasses with type annotations. Returns dict.
* **TypedDict**: Typed dictionary classes. Returns dict.
* **JSON Schema**: Dictionary with JSON schema specification. Returns dict.

​

strict

Optional boolean parameter to enable strict schema adherence. Supported by some providers (e.g., OpenAI and xAI). Defaults to `None` (disabled).

LangChain automatically uses `ProviderStrategy` when you pass a schema type directly to `create_agent.response_format` and the model supports native structured output:

Pydantic Model

Dataclass

TypedDict

JSON Schema

```
from pydantic import BaseModel, Field
from langchain.agents import create_agent


class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

agent = create_agent(
    model="gpt-5.4",
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

Provider-native structured output provides high reliability and strict validation because the model provider enforces the schema. Use it when available.

If the provider natively supports structured output for your model choice, it is functionally equivalent to write `response_format=ProductReview` instead of `response_format=ProviderStrategy(ProductReview)`.In either case, if structured output is not supported, the agent will fall back to a tool calling strategy.

## ​ Tool calling strategy

For models that don’t support native structured output, LangChain uses tool calling to achieve the same result. This works with all models that support tool calling (most modern models).
To use this strategy, configure a `ToolStrategy`:

```
class ToolStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    tool_message_content: str | None
    handle_errors: Union[
        bool,
        str,
        type[Exception],
        tuple[type[Exception], ...],
        Callable[[Exception], str],
    ]
```

​

schema

required

The schema defining the structured output format. Supports:

* **Pydantic models**: `BaseModel` subclasses with field validation. Returns validated Pydantic instance.
* **Dataclasses**: Python dataclasses with type annotations. Returns dict.
* **TypedDict**: Typed dictionary classes. Returns dict.
* **JSON Schema**: Dictionary with JSON schema specification. Returns dict.
* **Union types**: Multiple schema options. The model will choose the most appropriate schema based on the context.

​

tool\_message\_content

Custom content for the tool message returned when structured output is generated.
If not provided, defaults to a message showing the structured response data.

​

handle\_errors

Error handling strategy for structured output validation failures. Defaults to `True`.

* **`True`**: Catch all errors with default error template
* **`str`**: Catch all errors with this custom message
* **`type[Exception]`**: Only catch this exception type with default message
* **`tuple[type[Exception], ...]`**: Only catch these exception types with default message
* **`Callable[[Exception], str]`**: Custom function that returns error message
* **`False`**: No retry, let exceptions propagate

Pydantic Model

Dataclass

TypedDict

JSON Schema

Union Types

```
from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int | None = Field(description="The rating of the product", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review")
    key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.")

agent = create_agent(
    model="gpt-5.4",
    tools=tools,
    response_format=ToolStrategy(ProductReview)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})
result["structured_response"]
# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])
```

### ​ Custom tool message content

The `tool_message_content` parameter allows you to customize the message that appears in the conversation history when structured output is generated:

```
from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class MeetingAction(BaseModel):
    """Action items extracted from a meeting transcript."""
    task: str = Field(description="The specific task to be completed")
    assignee: str = Field(description="Person responsible for the task")
    priority: Literal["low", "medium", "high"] = Field(description="Priority level")

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    response_format=ToolStrategy(
        schema=MeetingAction,
        tool_message_content="Action item captured and added to meeting notes!"
    )
)

agent.invoke({
    "messages": [{"role": "user", "content": "From our meeting: Sarah needs to update the project timeline as soon as possible"}]
})
```

```
================================ Human Message =================================

From our meeting: Sarah needs to update the project timeline as soon as possible
================================== Ai Message ==================================
Tool Calls:
  MeetingAction (call_1)
 Call ID: call_1
  Args:
    task: Update the project timeline
    assignee: Sarah
    priority: high
================================= Tool Message =================================
Name: MeetingAction

Action item captured and added to meeting notes!
```

Without `tool_message_content`, our final `ToolMessage` would be:

```
================================= Tool Message =================================
Name: MeetingAction

Returning structured response: {'task': 'update the project timeline', 'assignee': 'Sarah', 'priority': 'high'}
```

### ​ Error handling

Models can make mistakes when generating structured output via tool calling. LangChain provides intelligent retry mechanisms to handle these errors automatically.

#### ​ Multiple structured outputs error

When a model incorrectly calls multiple structured output tools, the agent provides error feedback in a `ToolMessage` and prompts the model to retry:

```
from pydantic import BaseModel, Field
from typing import Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ContactInfo(BaseModel):
    name: str = Field(description="Person's name")
    email: str = Field(description="Email address")

class EventDetails(BaseModel):
    event_name: str = Field(description="Name of the event")
    date: str = Field(description="Event date")

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    response_format=ToolStrategy(Union[ContactInfo, EventDetails])  # Default: handle_errors=True
)

agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})
```

```
================================ Human Message =================================

Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th
None
================================== Ai Message ==================================
Tool Calls:
  ContactInfo (call_1)
 Call ID: call_1
  Args:
    name: John Doe
    email: john@email.com
  EventDetails (call_2)
 Call ID: call_2
  Args:
    event_name: Tech Conference
    date: March 15th
================================= Tool Message =================================
Name: ContactInfo

Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.
 Please fix your mistakes.
================================= Tool Message =================================
Name: EventDetails

Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.
 Please fix your mistakes.
================================== Ai Message ==================================
Tool Calls:
  ContactInfo (call_3)
 Call ID: call_3
  Args:
    name: John Doe
    email: john@email.com
================================= Tool Message =================================
Name: ContactInfo

Returning structured response: {'name': 'John Doe', 'email': 'john@email.com'}
```

#### ​ Schema validation error

When structured output doesn’t match the expected schema, the agent provides specific error feedback:

```
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ProductRating(BaseModel):
    rating: int | None = Field(description="Rating from 1-5", ge=1, le=5)
    comment: str = Field(description="Review comment")

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    response_format=ToolStrategy(ProductRating),  # Default: handle_errors=True
    system_prompt="You are a helpful assistant that parses product reviews. Do not make any field or value up."
)

agent.invoke({
    "messages": [{"role": "user", "content": "Parse this: Amazing product, 10/10!"}]
})
```

```
================================ Human Message =================================

Parse this: Amazing product, 10/10!
================================== Ai Message ==================================
Tool Calls:
  ProductRating (call_1)
 Call ID: call_1
  Args:
    rating: 10
    comment: Amazing product
================================= Tool Message =================================
Name: ProductRating

Error: Failed to parse structured output for tool 'ProductRating': 1 validation error for ProductRating.rating
  Input should be less than or equal to 5 [type=less_than_equal, input_value=10, input_type=int].
 Please fix your mistakes.
================================== Ai Message ==================================
Tool Calls:
  ProductRating (call_2)
 Call ID: call_2
  Args:
    rating: 5
    comment: Amazing product
================================= Tool Message =================================
Name: ProductRating

Returning structured response: {'rating': 5, 'comment': 'Amazing product'}
```

#### ​ Error handling strategies

You can customize how errors are handled using the `handle_errors` parameter:
**Custom error message:**

```
ToolStrategy(
    schema=ProductRating,
    handle_errors="Please provide a valid rating between 1-5 and include a comment."
)
```

If `handle_errors` is a string, the agent will *always* prompt the model to re-try with a fixed tool message:

```
================================= Tool Message =================================
Name: ProductRating

Please provide a valid rating between 1-5 and include a comment.
```

**Handle specific exceptions only:**

```
ToolStrategy(
    schema=ProductRating,
    handle_errors=ValueError  # Only retry on ValueError, raise others
)
```

If `handle_errors` is an exception type, the agent will only retry (using the default error message) if the exception raised is the specified type. In all other cases, the exception will be raised.
**Handle multiple exception types:**

```
ToolStrategy(
    schema=ProductRating,
    handle_errors=(ValueError, TypeError)  # Retry on ValueError and TypeError
)
```

If `handle_errors` is a tuple of exceptions, the agent will only retry (using the default error message) if the exception raised is one of the specified types. In all other cases, the exception will be raised.
**Custom error handler function:**

```
from langchain.agents.structured_output import StructuredOutputValidationError
from langchain.agents.structured_output import MultipleStructuredOutputsError

def custom_error_handler(error: Exception) -> str:
    if isinstance(error, StructuredOutputValidationError):
        return "There was an issue with the format. Try again."
    elif isinstance(error, MultipleStructuredOutputsError):
        return "Multiple structured outputs were returned. Pick the most relevant one."
    else:
        return f"Error: {str(error)}"


agent = create_agent(
    model="gpt-5.4",
    tools=[],
    response_format=ToolStrategy(
                        schema=Union[ContactInfo, EventDetails],
                        handle_errors=custom_error_handler
                    )  # Default: handle_errors=True
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})

for msg in result['messages']:
    # If message is actually a ToolMessage object (not a dict), check its class name
    if type(msg).__name__ == "ToolMessage":
        print(msg.content)
    # If message is a dictionary or you want a fallback
    elif isinstance(msg, dict) and msg.get('tool_call_id'):
        print(msg['content'])
```

On `StructuredOutputValidationError`:

```
================================= Tool Message =================================
Name: ToolStrategy

There was an issue with the format. Try again.
```

On `MultipleStructuredOutputsError`:

```
================================= Tool Message =================================
Name: ToolStrategy

Multiple structured outputs were returned. Pick the most relevant one.
```

On other errors:

```
================================= Tool Message =================================
Name: ToolStrategy

Error: <error message>
```

**No error handling:**

```
response_format = ToolStrategy(
    schema=ProductRating,
    handle_errors=False  # All errors raised
)
```

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Streaming

Previous

Overview

Next

⌘I