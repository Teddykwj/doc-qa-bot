Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Integrations

assistant-ui

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

  + Overview
  + CopilotKit
  + AI Elements
  + assistant-ui
  + OpenUI

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

* How it works
* Installation
* Wiring useStream
* Converting messages
* Customising the thread UI
* Best practices

Frontend

Integrations

# assistant-ui

Copy page

Headless React AI chat framework with a full runtime layer, bridged to useStream

Copy page

assistant-ui is a headless React UI framework for AI chat. It provides a full runtime layer—thread management, message branching, attachment handling—that connects to `useStream` via the `useExternalStoreRuntime` adapter.


Clone and run the full assistant-ui example to see a Claude-style chat interface wired to a LangChain agent with `useExternalStoreRuntime`.

## ​ How it works

1. **Stream with `useStream`** — connect to your agent and get reactive messages, loading state, and submit/cancel callbacks
2. **Adapt with `useExternalStoreRuntime`** — bridge `stream.messages` into assistant-ui’s runtime format by converting `BaseMessage[]` to `ThreadMessageLike[]`
3. **Provide the runtime** — wrap your UI in `AssistantRuntimeProvider` and render any assistant-ui thread component

## ​ Installation

```
bun add @assistant-ui/react @assistant-ui/react-markdown
```

## ​ Wiring useStream

The `useExternalStoreRuntime` adapter bridges `stream.messages` into the assistant-ui runtime. Pass it to `AssistantRuntimeProvider` and render any thread component:

```
import { useCallback, useMemo } from "react";
import {
  AssistantRuntimeProvider,
  useExternalStoreRuntime,
  type AppendMessage,
  type ThreadMessageLike,
} from "@assistant-ui/react";
import { useStream } from "@langchain/react";
import { Thread } from "@assistant-ui/react";

export function Chat() {
  const stream = useStream({
    apiUrl: "http://localhost:2024",
    assistantId: "agent",
  });

  const onNew = useCallback(
    async (message: AppendMessage) => {
      const text = message.content
        .filter((c) => c.type === "text")
        .map((c) => c.text)
        .join("");
      await stream.submit({ messages: [{ type: "human", content: text }] });
    },
    [stream],
  );

  // Convert LangChain messages to assistant-ui's ThreadMessageLike format
  const messages = useMemo(
    () => toThreadMessages(stream.messages),
    [stream.messages],
  );

  const runtime = useExternalStoreRuntime<ThreadMessageLike>({
    messages,
    onNew,
    onCancel: () => stream.stop(),
    convertMessage: (m) => m,
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  );
}
```

### ​ Converting messages

`toThreadMessages` maps LangChain `BaseMessage[]` to the `ThreadMessageLike[]` format assistant-ui expects. Handle each message type — human, AI, and tool — and convert content blocks, tool calls, and reasoning tokens:

```
import { AIMessage, HumanMessage, ToolMessage } from "@langchain/core/messages";
import type { ThreadMessageLike } from "@assistant-ui/react";

export function toThreadMessages(messages: BaseMessage[]): ThreadMessageLike[] {
  const result: ThreadMessageLike[] = [];

  for (const msg of messages) {
    if (HumanMessage.isInstance(msg)) {
      result.push({
        role: "user",
        content: [{ type: "text", text: getTextContent(msg.content) }],
      });
    } else if (AIMessage.isInstance(msg)) {
      const parts: ThreadMessageLike["content"] = [];

      // Reasoning tokens
      const reasoning = getReasoningText(msg);
      if (reasoning) parts.push({ type: "reasoning", reasoning });

      // Tool calls
      for (const tc of msg.tool_calls ?? []) {
        parts.push({
          type: "tool-call",
          toolCallId: tc.id ?? "",
          toolName: tc.name,
          args: tc.args,
        });
      }

      // Text response
      const text = getTextContent(msg.content);
      if (text) parts.push({ type: "text", text });

      result.push({ role: "assistant", content: parts });
    } else if (ToolMessage.isInstance(msg)) {
      // Attach tool results to the preceding assistant message
      const last = result[result.length - 1];
      if (last?.role === "assistant") {
        for (const part of last.content) {
          if (
            part.type === "tool-call" &&
            part.toolCallId === msg.tool_call_id
          ) {
            (part as { result?: string }).result = getTextContent(msg.content);
          }
        }
      }
    }
  }

  return result;
}
```

See all 52 lines

## ​ Customising the thread UI

`<Thread />` ships a complete default thread UI including message list, composer, and scroll management. Customise individual parts by overriding component slots:

```
import { Thread, ThreadMessages, Composer } from "@assistant-ui/react";

function CustomThread() {
  return (
    <Thread.Root>
      <ThreadMessages
        components={{
          UserMessage: MyUserMessage,
          AssistantMessage: MyAssistantMessage,
          ToolFallback: MyToolCard,
        }}
      />
      <Composer />
    </Thread.Root>
  );
}
```

## ​ Best practices

* **Memoise message conversion:** wrap `toThreadMessages(stream.messages)` in `useMemo` to avoid re-running the conversion on every render
* **Handle attachments:** use `CompositeAttachmentAdapter` with `SimpleImageAttachmentAdapter` for image uploads; extend with custom adapters for files
* **Use branching:** assistant-ui has built-in message branching support via `MessageBranch`; edit a message to regenerate from that point
* **Thread persistence:** `useStream` with `fetchStateHistory: true` and `reconnectOnMount: true` gives assistant-ui access to the full thread history on page load

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

AI Elements

Previous

OpenUI

Next

⌘I