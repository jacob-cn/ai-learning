# Canonical terminology

This table is the **canonical source** for every term used across the site.
`glossary.html` is the reader-facing mirror of it — the two must always agree.

Rules:
- Use these exact terms everywhere on the site. Mention a common synonym once on
  first use, then stick to the canonical term.
- Whenever a new term is introduced anywhere, add it to BOTH this table and
  `glossary.html` in the same edit. This table stays in first-appears order;
  `glossary.html` is sorted A–Z and carries a jump-to index — when adding a term
  there, insert the `<dt>`/`<dd>` in alphabetical position AND add its link to the
  `.gloss-index` nav.

| Term | Canonical meaning | First appears |
|---|---|---|
| Token | The basic unit an LLM reads — a subword piece from a fixed vocabulary (~4 chars of English on average). | Stage 1 |
| Context window | The total text a model can consider in one request. | Stage 1 |
| System prompt | A persistent instruction set, separate from the conversation. | Stage 1 |
| Prompt engineering | Wording instructions so a model behaves predictably. | Stage 2 |
| Structured output | Asking a model to return data in a defined format (e.g. JSON). | Stage 2 |
| Tool use (a.k.a. function calling) | Giving a model described functions it can request; it never executes them itself. | Stage 3 |
| Agent loop | Send request → model requests a tool → execute → return result → repeat. | Stage 3 |
| Context compaction | Summarizing earlier context as the window fills, to continue smoothly instead of erroring or dropping history. Also "context compression." | Stage 3 |
| Embedding | A numeric vector representation of text; similar meanings → similar numbers. | Stage 4 |
| Chunking | Splitting a long document into smaller overlapping pieces before embedding. | Stage 4 |
| RAG | Retrieving the most relevant chunks of your data, injecting only those into the prompt. | Stage 4 |
| MCP | An open standard letting any AI app connect to any tool/data server without custom code. | Stage 5 |
| MCP host / client / server | Host = the app; client = built-in, speaks the protocol; server = what you build. | Stage 5 |
| Transport (stdio / HTTP) | stdio launches a local process; HTTP connects to an independently-running server. | Stage 5 |
| ReAct | "Reason + Act" — a prompted pattern making the model's reasoning visible before each tool call. | Stage 6 |
| Extended thinking | A trained model capability producing private reasoning before any answer; a toggle, not a prompt. | Stage 6 |
| Inference | Running a trained model to produce any output — opposite of "training," not of "thinking." | Stage 6 |
| Harness | Everything around a model that makes it a working agent: tools, memory, loop, verification, guardrails. | Stage 6 |
| Loop engineering | An outer system running an agent's harness on a schedule across many runs. Very new, contested. | Stage 6 |
| Generator/verifier split | A separate, skeptical model checks whether a claimed "done" is actually correct. | Stage 6 |
| Spec-Driven Development | Writing a structured, testable specification of intent before an agent acts. | Stage 6 |
| Rate limits (RPM / TPM / RPD) | Three independent API caps, each failing and fixed differently. | Stage 6 |
