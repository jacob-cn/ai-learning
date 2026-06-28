# Changelog

A plain-language log of what changed and when — for a quick glance, not a
replacement for git history. Add a new entry whenever a stage is added or
meaningfully changed. Newest entry at the top; tagged releases use a
`## vX.Y.Z — date` header (Semantic Versioning).

## v1.0.0 — 2026-06-28 — First public version
Six stages (multi-turn chatbot & the context window, structured output, tool use,
RAG, MCP, ReAct & harness engineering), each with a runnable demo and README; a
glossary; and a forward-looking "Where this could go" page. Plain HTML/CSS/JS with a
light/dark theme toggle. The dated entries below are the development log behind this
release.

## 2026-06-28 — Pre-commit polish: theme toggle, nav tweaks
- Added a manual light/dark theme toggle (`js/theme.js` + a topbar button on every
  page) that cycles Auto → Light → Dark, persisted in localStorage. "Auto" still
  follows the OS via prefers-color-scheme; Light/Dark set `data-theme` on <html> to
  override. No-flash (script runs in <head>); the button is JS-revealed so no-JS
  readers just get the system theme. CSS restructured so the dark palette serves both
  the manual override and the auto default.
- Home "Start the journey" button now links to Stage 1 (was the stage list anchor).
- Renamed the forward-looking page from "What's next" to "Where this could go"
  (page title/crumb/heading, the home timeline card, and Stage 6's pager) — it's a
  set of directions, not a committed next release.

## 2026-06-28 — Applied the correction-review fixes
- Stage 1 tokenizer rewrite (S1-1): corrected "1 word ≈ 1 token" to subword
  tokenization (BPE/WordPiece/Unigram/SentencePiece, the merge-frequent-pairs
  build), with a real GPT-tokenized colored example (verified via tiktoken), a
  redrawn diagram now ending in the model, and links to live tokenizer
  playgrounds. Updated the Token bullet, glossary entry, and terminology.md.
- Stage 2: added an enforced-structured-output callout (S2-1, Gemini
  responseSchema / JSON mode, with docs link); rewrote the IDE-inspect line to be
  precise (S2-2, VS Code "Show Chat Debug View").
- Stage 6: replaced the unverifiable "30th→5th" figure with a sourced one (S6-1,
  same-model harness swings ~5–20 pts, SWE-bench scaffolding analysis); attributed
  ReAct to Yao et al. 2022 (S6-2, arXiv link).
- Marked CORRECTION_SUGGESTIONS.md as fully applied.

## 2026-06-28 — v1 polish: screenshots, glossary, review
- Blurred the personal path out of every demo screenshot's terminal title bar
  (8 images) and embedded the screenshots in each demo README.
- Glossary: sorted all terms A–Z, added a jump-to index of term chips, and a
  "Back to Home" pager at the bottom. Updated terminology.md's rule to match
  (table stays first-appears order; glossary is alphabetical + indexed).
- Added `CORRECTION_SUGGESTIONS.md` — a page-by-page review with web-checked
  findings (structured-output enforcement, the "30th→5th" claim, ReAct
  attribution, etc.). Review material only; no page content was changed.

## 2026-06-28 — Stage 5 demo: opencode config + run notes
- Scrubbed personal absolute paths out of the Stage 5 `opencode.json` (now uses
  relative paths and clearer entry names: `notes-stdio` / `notes-http`).
- Added a README section on connecting the server from opencode, and clarified the
  run steps: Option B (HTTP) now says to keep the server's terminal open; Option A
  (stdio) clarifies the client launches the script itself, so there's no terminal
  to keep.

## 2026-06-28 — Pinned Python demo dependencies
- Migrated the Stage 3 demo (`dev_assistant.py`) from the deprecated
  `google.generativeai` to `google-genai`, matching Stages 1/4/6; updated its
  README and the Stage 3 page snippets to the new SDK shape.
- Added a pinned `requirements.txt` to every Python demo so they keep working as
  new package versions ship: 01/03/06 → `google-genai==2.10.0` +
  `python-dotenv==1.2.2`; 04 also `chromadb==1.5.9` + `ollama==0.6.2`; 05 →
  `mcp==1.28.1` (was an unpinned `mcp`). The google-genai/dotenv pins are the exact
  versions in the existing 01 & 03 venvs; chromadb/ollama/mcp are current latest.
- Pointed each demo README's install step at `pip install -r requirements.txt`.
- Left the Stage 2 TypeScript demo untouched (Python-only pass).

## 2026-06-28 — Stage 6: define "agent", clearer framing
- Added a "First — what's an 'agent'?" section before ReAct: a bare model does one
  inference pass; an agent wraps it in tools + loop + memory + verification to pursue
  a goal over many steps. Ties back to every prior stage.
- Reframed the loose-terms table into "Reasoning, tool-calling, and inference — three
  different things": confirms extended thinking is the technical name for reasoning
  (a.k.a. deep thinking), and that inference is the umbrella under which reasoning and
  tool-calling happen.
- Renamed "The vocabulary landscape" → "A rapidly evolving vocabulary"; marked on the
  ladder (and in text) that the "agent" concept begins at the harness rung.
- Reworded the model-swap claim from "proof" to an honest first-hand observation that
  the harness made two models interchangeable behind it.
- Shortened the generator/verifier write-up and moved it into Gotchas & lessons.
- Added the actual ReAct system-prompt excerpt to the code section, showing it really
  is one "Thought:" line.

## 2026-06-28 — Stage 5: MCP server reference links
- Added reference links under "Popular MCP servers": the official reference-servers
  repo, the official MCP Registry, and community directories (mcpservers.org, Glama),
  with a note on the ecosystem's scale. Server examples verified against current docs.

## 2026-06-28 — Stage 3: real, attributed tool names
- Replaced the invented snake_case tool examples with real names verified from
  vendor docs, attributed per agent (Claude Code `Read`/`Edit`/`Bash`/`Grep`/
  `Glob`/`WebSearch`/`AskUserQuestion`; Cursor `read_file`/`edit_file`/`list_dir`/
  `codebase_search`/`run_terminal_cmd`; Cline `write_to_file`/`replace_in_file`/
  `execute_command`/`ask_followup_question`; Codex `shell`/`apply_patch`). Added a
  note that even the casing convention differs (Claude Code TitleCase vs snake_case).

## 2026-06-28 — Real-world examples on Stages 3 & 5
- Stage 3: added "The tools most agents share" — a table of common agent
  capabilities (read/edit/list/search/shell/web) and the various names different
  assistants give them, grounding the tool-definition pattern in real tools.
- Stage 5: added "Popular MCP servers" — a categorized sampler (Filesystem, Git,
  GitHub, Postgres, Fetch, Brave Search, Puppeteer, Slack, Notion, Linear, Stripe,
  Memory) showing you rarely build a server yourself, and noting their tools join
  the same flat list as the Stage 3 tool shape.

## 2026-06-28 — Stage 5: clearer framing
- Retitled "MCP — host, client, server" to "MCP — connect any tool to any AI app"
  (page + home card) so the title says what MCP is at a glance.
- Trimmed "What I built" of transport/Docker specifics (they're in the README) and
  removed the Docker-bug pointer paragraph.
- Added a simple Host / Client / Server diagram showing the model + client inside
  the host, the MCP/JSON-RPC link to the server you build, and the server's tools.
- Renamed "How MCP, plain tools, and skills relate" → "MCP, tools, and skills —
  what's the difference?"; fixed the table to say "name, description, and parameter
  schema"; reframed the summary (MCP/tools = capabilities; skills = guidance whose
  steps still call tools).
- Corrected the lifecycle note: add/remove isn't live — some agents need a relaunch,
  some a new session.
- Simplified the code section to show `mcp.run(transport=...)` and what stdio vs
  streamable-http mean, dropping the host/IP detail (README's job).

## 2026-06-28 — Stage 4: reworked the concept section
- Added "Embeddings come from an AI model" — an embedding is produced by a real
  (separate) embedding model, and the SAME model must embed both the documents
  and the query, or "nearest" is meaningless.
- Reframed "what vector search means" into "How RAG does the search"; enhanced the
  2D diagram with a legend, and added a data table mapping each point to its topic,
  distance, and whether it was retrieved.
- Added an "embedding dimensions by model" table (384–3072) before the questions
  part; moved the vectors Q&A below the pipeline; added index/query flow text.
- Rewrote Gotchas around scale: RAG needs many chunks to choose from, and chunking
  needs documents long enough to split — on a few short notes it does nothing.
- Reworked "How RAG hides inside AI web search" to show the keyword search is
  always present while the embedding-RAG step is an optional branch (only when
  digging inside one big page), with an updated diagram.
- Split the coding-agent memory note into its own section (it was misfiled under
  web search).

## 2026-06-27 — Stage 3: the structured tool call
- Added a "The tool call comes back structured" concept to Stage 3 — the model's
  tool request is a structured `function_call` (name + args), which is how the
  agent detects a tool request vs. a final text answer; the result goes back as a
  structured `function_response`. Added a round-trip diagram of the two messages.
- Tied the Part 2 walkthrough to it (detecting `function_call`, returning
  `function_response`). The concept section now covers the full picture:
  declare tools → structured tool call → execute-and-return loop.

## 2026-06-27 — Stage 3: how the model learns a tool exists
- Added a "How the model knows which tools exist" concept to Stage 3 — tool
  definitions (name + description + parameter schema) sent with each request,
  with a diagram of one definition and the point that the description is the
  model's only knowledge of the tool (same shape as MCP).
- Split the Stage 3 "core mechanic" code into Part 1 (declare the tools, attach
  them to the model) and Part 2 (run the loop), each with its own walkthrough.

## 2026-06-27 — Split terminology out of the skill
- Moved the canonical term table out of `SKILL.md` into a sibling
  `terminology.md`, loaded only when terminology actually matters. SKILL.md now
  keeps just a short pointer + the keep-in-sync rule. `terminology.md` is the
  source; `glossary.html` remains its reader-facing mirror (both at 22 terms).

## 2026-06-27 — Stage 3: context compaction
- Reframed Stage 3's "what happens when the window fills up" from a mostly-bad
  outcome (silent forgetting) to a worst-to-best spectrum: hard error → blunt
  truncation → context compaction. Made clear that mature agents/tools summarize
  earlier turns and continue smoothly, losing fidelity rather than the thread.
- Added "Context compaction" as a canonical term (glossary.html + SKILL.md
  terminology table), first appearing in Stage 3.

## 2026-06-27 — Stage 1 demo actually shows multi-turn
- Reworked the Stage 1 chatbot to make the multi-turn mechanic visible instead
  of hiding it behind the SDK's `chats.create` helper. It now holds the
  conversation in a plain `history` list and resends the whole list via
  `client.models.generate_content(contents=history)` every turn, and prints a
  per-turn line showing the messages resent and the context-token count climbing
  (from `response.usage_metadata`). Added a `history` command to dump the exact
  payload resent. Updated the Stage 1 page snippet/walkthrough and the README's
  "What to check" to match.

## 2026-06-27 — Stage 1 SDK migration
- Migrated the Stage 1 chatbot demo from the deprecated `google-generativeai`
  SDK (`import google.generativeai`) to the current `google-genai` SDK
  (`from google import genai`, `client.chats.create(...)`). The demo's README
  already installed `google-genai`, so the old import raised
  `ModuleNotFoundError` — the code now matches its README and Stages 4 & 6.
- Updated the Stage 1 page's cited snippet and walkthrough to match.

## 2026-06-27 — Privacy scrub
- Removed personal/identifying framing from the site: the home page title, meta
  description, and hero no longer mention years of experience or frame the author
  with a résumé line; softened a first-person background line in Stage 1 and
  neutralised the chatbot demo's system-prompt audience. Demo subject-matter that
  genuinely uses a technology (the Android/Kotlin reviewer, the Android RAG docs)
  was intentionally kept.
- Scrubbed the same phrase from SPEC.md (a deliberate, minimal exception to the
  never-edit rule) and updated CLAUDE.md + SKILL.md: added a privacy rule and
  carved out the SPEC exception for personal-info scrubs.

## 2026-06-27 — Revision pass (feedback)
- Refined the theme into a warmer, Claude-like look and replaced the diagrams
  with cleaner hand-authored SVGs (dark-mode aware via shared token classes).
- Redesigned `index.html` into a proper landing page (hero + numbered path);
  stage cards now show title + summary only, no demo language.
- Corrected the registry: Stage 1 is Python only (there is no TypeScript
  chatbot demo); removed all TS-chatbot references from the site.
- Standardised every stage: a demo-link button under "What I built", a short
  "Gotchas & lessons" callout (AI-relevant only; operational details stay in
  READMEs), and a plain-language `.codewalk` walkthrough under each snippet.
- New content per feedback: tokenizer explainer (S1); system-prompt layers +
  inspecting/jailbreaking (S2); clearer loop diagram + context-limit and
  noisy-tool discussion (S3); 2D vector-search diagram, dimensions/DB-growth
  Q&A, and a deeper web-search flow (S4); MCP history + MCP-vs-tools-vs-skills,
  with the Docker saga moved to the README (S5); SDD split into its own section
  and a shortened rate-limit lesson (S6).
- Added `stages/stage-next.html` — a living "What's next" page that always
  follows the latest stage; linked from the index timeline and Stage 6's pager.
- Updated CLAUDE.md (registry fix + stage-next convention) and SKILL.md (stage
  page anatomy, SVG/diagram + codewalk conventions).

## 2026-06-27 — Initial site
- Built the full site from scratch: `index.html` (landing page with a six-stage
  timeline + a "how this site is built" note), `css/style.css` (shared,
  mobile-responsive, dark-mode aware, CSS-only code styling — no JS libraries),
  and `glossary.html` mirroring the canonical terminology table.
- Wrote all six stage pages, each grounded in its `demos/` folder and README,
  with a consistent structure: What I built → Key concepts → The gotcha →
  a short cited code snippet linking to the real file on GitHub.
- Folded `CONTENT_NOTES.md` into the matching pages: the Claude-vs-Gemini
  billing wall and environment traps (Stage 1); where RAG still fits vs. the
  code-search reversal (Stage 4); the JSON-RPC protocol, tool-source-agnostic
  routing, MCP living-with notes, and the full Docker `0.0.0.0` debugging saga
  (Stage 5); and the prompt→context→harness→loop terminology ladder, SDD,
  generator/verifier split, model-swap proof, and the three-cap rate-limit
  story (Stage 6). Operational specifics stayed in the demo READMEs per the
  page-vs-README rule.
