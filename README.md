# AI Learning Journey

Notes from learning AI development by building — one small project per stage, from a
first API call to a working autonomous agent. It's a plain static site (no build
step) with a runnable demo behind every stage.

**Live site → https://jacob-cn.github.io/ai-learning/**

## The six stages
1. **Multi-turn chatbot & the context window** — why a model is stateless, and what a token really is
2. **Structured output & prompt engineering** — getting strict JSON back, not prose
3. **Tool use / function calling** — letting the model act through tools, in a loop
4. **RAG & embeddings** — answering from your own documents
5. **MCP** — the open standard for connecting tools to AI apps
6. **ReAct agents & harness engineering** — an autonomous agent checked by a separate verifier

Plus a glossary of every term and a short "where this could go" page.

## Repo layout
- `index.html`, `stages/`, `css/`, `js/` — the site (plain HTML/CSS/JS)
- `glossary.html` — canonical terms, A–Z
- `demos/NN-topic-language/` — a runnable, redacted demo + its own README per stage

## Running a demo
Each `demos/` folder has a README with **Setup / Run / What to check**. In short: the
Python demos use a virtualenv + `pip install -r requirements.txt` and a `GEMINI_API_KEY`
in a local `.env` (a free key from Google AI Studio); the TypeScript demo uses
`npm install`. No keys are committed.

## Built with
Plain HTML, CSS, and a little vanilla JavaScript — no framework, no build step, served
straight from GitHub Pages. Light/dark theme follows your system, with a manual toggle.
