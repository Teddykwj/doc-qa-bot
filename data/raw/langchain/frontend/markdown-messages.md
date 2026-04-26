Skip to main content

Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. Buy tickets >

Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

Search...

Navigation

Patterns

Markdown messages

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

  + Markdown messages
  + Tool calling
  + Human-in-the-Loop
  + Branching chat
  + Reasoning tokens
  + Structured output
  + Message queues
  + Join & rejoin streams
  + Time travel
  + Generative UI
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

* How markdown rendering works
* Setting up useStream
* Choosing a markdown library
* Building the Markdown component
* Sanitizing HTML output
* Streaming considerations
* Styling markdown content
* Best practices

Frontend

Patterns

# Markdown messages

Copy page

Render LLM responses as rich, formatted markdown with proper streaming support

Copy page

LLMs naturally produce markdown-formatted text, including headings, lists, code blocks,
tables, and inline formatting. Rendering this content as plain text wastes the
structure the model is providing. This pattern shows you how to parse and render
markdown in real time as it streams from the agent, across all major frontend
frameworks.


## ​ How markdown rendering works

The rendering pipeline has three steps:

1. **Receive:** `useStream` accumulates the streamed text into `msg.text` on
   each AI message, updating reactively as new tokens arrive.
2. **Parse:** A markdown parser converts the raw text to HTML (or a React
   element tree). This runs on every update but is fast enough for chat-length
   content (< 5ms for a 5 KB message).
3. **Render:** The parsed output is rendered into the DOM. React uses virtual
   DOM diffing; Vue and Svelte use `v-html` / `{@html}` with sanitized HTML.

## ​ Setting up useStream

The markdown pattern uses a simple chat agent with no special configuration.
Wire up `useStream` with your agent URL and assistant ID.
Define a TypeScript interface matching your agent’s state schema and pass it as a type parameter to `useStream` for type-safe access to state values. In the examples below, replace `typeof myAgent` with your interface name:

```
import type { BaseMessage } from "@langchain/core/messages";

interface AgentState {
  messages: BaseMessage[];
}
```

React

Vue

Svelte

Angular

```
import { useStream } from "@langchain/react";
import { AIMessage, HumanMessage } from "@langchain/core/messages";

const AGENT_URL = "http://localhost:2024";

export function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });

  return (
    <div>
      {stream.messages.map((msg) => {
        if (AIMessage.isInstance(msg)) {
          return <Markdown key={msg.id}>{msg.text}</Markdown>;
        }
        if (HumanMessage.isInstance(msg)) {
          return <p key={msg.id}>{msg.text}</p>;
        }
      })}
    </div>
  );
}
```

## ​ Choosing a markdown library

Each framework has a natural choice for markdown rendering:

| Framework | Library | Output | Why |
| --- | --- | --- | --- |
| React | `react-markdown` + `remark-gfm` | React elements | Component-based, virtual DOM diffing, no `dangerouslySetInnerHTML` |
| Vue | `marked` + `dompurify` | Sanitized HTML via `v-html` | Lightweight, fast, GFM built-in |
| Svelte | `marked` + `dompurify` | Sanitized HTML via `{@html}` | Same as Vue, consistent API |
| Angular | `marked` + `dompurify` | Sanitized HTML via `[innerHTML]` | Same as Vue/Svelte |

React’s `react-markdown` converts markdown directly to React elements, so it
doesn’t need HTML sanitization. There’s no `dangerouslySetInnerHTML` involved.
For Vue, Svelte, and Angular, always sanitize the parsed HTML with `dompurify`
before rendering.

## ​ Building the Markdown component

React

Vue

Svelte

Angular

```
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function Markdown({ children }: { children: string }) {
  return (
    <div className="markdown-content">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {children}
      </ReactMarkdown>
    </div>
  );
}
```

## ​ Sanitizing HTML output

When rendering parsed markdown as raw HTML (`v-html`, `{@html}`, `[innerHTML]`),
you must sanitize the output to prevent cross-site scripting (XSS). LLM
responses may contain arbitrary text, including markup that a markdown parser
could turn into executable HTML.
Use `dompurify` to strip dangerous elements:

```
import DOMPurify from "dompurify";

const safeHtml = DOMPurify.sanitize(rawHtml);
```

DOMPurify removes `<script>` tags, `onclick` attributes, `javascript:` URLs,
and other XSS vectors while preserving safe markdown output like headings,
lists, code blocks, tables, and links.

React’s `react-markdown` does not need `dompurify` because it produces React
elements directly, no raw HTML injection is involved.

## ​ Streaming considerations

`useStream` updates `msg.text` reactively as each token arrives. The markdown
component re-parses on every update. For typical chat messages, this is
performant:

* `marked` parses at ~1 MB/s. A 5 KB message takes < 5ms
* `react-markdown` + remark pipeline is similarly fast for chat-length content
* The browser’s layout engine handles the DOM update efficiently

For very long responses (> 50 KB), consider these optimizations:

* **Throttle renders:** use `requestAnimationFrame` to batch updates at 60fps
  instead of re-rendering on every token
* **Incremental parsing:** parse only new content and append to a rendered
  buffer (advanced, typically not needed for chat UIs)

For most chat applications, the simple approach of re-parsing the full message
on each token is sufficient. Only optimize if you observe janky scrolling or
dropped frames with very long messages.

## ​ Styling markdown content

Apply styles to the `.markdown-content` class to control the appearance of
rendered markdown. These are the essential styles:

```
.markdown-content p {
  margin: 0.4em 0;
}

.markdown-content ul,
.markdown-content ol {
  margin: 0.4em 0;
  padding-left: 1.4em;
}

.markdown-content pre {
  overflow-x: auto;
  border-radius: 0.375rem;
  background: rgba(0, 0, 0, 0.05);
  padding: 0.5rem;
  font-size: 0.75rem;
}

.markdown-content code {
  border-radius: 0.25rem;
  background: rgba(0, 0, 0, 0.08);
  padding: 0.125rem 0.25rem;
  font-size: 0.75rem;
}

.markdown-content blockquote {
  margin: 0.4em 0;
  padding-left: 0.75em;
  border-left: 3px solid currentColor;
  opacity: 0.8;
}

.markdown-content table {
  border-collapse: collapse;
  margin: 0.4em 0;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #e5e7eb;
  padding: 0.25em 0.5em;
}
```

Keep markdown styles compact for chat bubbles. Chat messages are smaller than
blog posts, so use tighter margins and smaller font sizes than a typical prose
stylesheet.

## ​ Best practices

* **Always sanitize:** when using `v-html`, `{@html}`, or `[innerHTML]`,
  always run the parsed output through `dompurify`. Never trust raw HTML from a
  markdown parser fed with LLM output.
* **Enable GFM:** GitHub Flavored Markdown adds tables, strikethrough, task
  lists, and autolinks. These features are commonly used by LLMs.
* **Handle empty content:** check for empty strings before parsing to avoid
  rendering empty containers.
* **Use `breaks: true`:** enable line break conversion so single newlines in
  LLM output render as `<br>` rather than being ignored. LLMs often use single
  newlines for visual separation.
* **Style for chat context:** use compact margins and sizes appropriate for
  chat bubbles, not full-width article layouts.
* **Test with rich content:** verify rendering with headings, nested lists,
  code blocks with long lines, wide tables, and blockquotes to catch overflow
  or layout issues.

---

Connect these docs to Claude, VSCode, and more via MCP for real-time answers.

Edit this page on GitHub or file an issue.

Was this page helpful?

YesNo

Overview

Previous

Tool calling

Next

⌘I