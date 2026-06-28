# CLAUDE.md — AI Learning Journey project memory

Durable facts only — things to hold in EVERY session. Multi-step procedures
and reference material live in `.claude/skills/site-workflow/SKILL.md`,
loaded only when actually relevant, so this file stays small.

## Project layout

```
/
├── index.html              ← landing page, links to every stage
├── stages/stageN-topic.html
├── glossary.html            ← canonical terms, for readers and for us
├── css/style.css
├── demos/NN-topic-language/ ← redacted real code + README per folder
├── CHANGELOG.md             ← plain log of what changed, when
├── SPEC.md                  ← original v1 brief — historical, never edited (except privacy scrubs)
└── CLAUDE.md                ← this file
```

## Stage registry — current state, update FIRST when adding a stage

| # | Topic | Language(s) | Demo folder(s) | Stage page |
|---|---|---|---|---|
| 01 | Multi-turn chatbot & context window | Python | `demos/01-chatbot-python/` | `stages/stage1-chatbot.html` |
| 02 | Structured output & prompt engineering (code reviewer) | TypeScript | `demos/02-code-reviewer-typescript/` | `stages/stage2-code-reviewer.html` |
| 03 | Tool use / function calling | Python | `demos/03-tool-use-python/` | `stages/stage3-tool-use.html` |
| 04 | RAG & embeddings | Python | `demos/04-rag-python/` | `stages/stage4-rag.html` |
| 05 | MCP — client/server/host, transports | Python | `demos/05-mcp-python/` | `stages/stage5-mcp.html` |
| 06 | ReAct agents & harness engineering | Python | `demos/06-agent-python/` | `stages/stage6-agent.html` |

`stages/stage-next.html` is a non-numbered living "What's next" page that always
sits AFTER the latest stage. When adding a stage: repoint the old last stage's
"next" pager to the new stage, and the new stage's "next" pager to
`stage-next.html`. The index timeline ends with a `.stage-card.next` card linking
to it.

## Security & privacy rules — ALWAYS, regardless of task

- NEVER commit a `.env` file, an API key, or anything that looks like a credential
- NEVER commit an absolute path containing a username (`/Users/<name>/...` etc.)
- Before adding anything to `demos/`, strip `venv/`, `__pycache__/`,
  `node_modules/`, local databases, and personal paths
- `.gitignore` is the enforced backstop — keep it current
- Keep the published site about the **learning, not the person**. Do NOT put
  personal/identifying details in site copy — years of experience, full name,
  employer, location, "I'm an X-year Y engineer." Mentioning a *technology*
  because a demo genuinely uses it (e.g. an Android/Kotlin code reviewer) is
  fine; framing the author with a résumé line is not.

## Where everything else lives

- Adding/updating a stage page, demo READMEs, citing code, deciding what
  belongs on a page vs in a README, visual style, terminology, or folding in
  a future deep-dive → `.claude/skills/site-workflow/SKILL.md`
- The full terminology list → `glossary.html` (always use those exact terms)
- What changed and when → `CHANGELOG.md` — add an entry whenever a stage is
  added or meaningfully changed; newest entry at the top

## Tech constraints

- Plain HTML/CSS/JS only — no build step, must work directly on GitHub Pages
- Mobile responsive
- No external dependency required just to read the content

## Versioning

Follow Semantic Versioning (semver.org), `MAJOR.MINOR.PATCH`. Current: **v1.0.0**.
- **PATCH** (x.y.Z) — typo/wording/factual fixes, small style tweaks; no new content
- **MINOR** (x.Y.0) — backward-compatible additions: a new stage, section, demo, or
  feature (e.g. the theme toggle)
- **MAJOR** (X.0.0) — a breaking restructure of the site or its information architecture

Bump the version in the SAME change, in BOTH places: the CHANGELOG (a new
`## vX.Y.Z — date` header at the top) and the home-page footer in `index.html`.
