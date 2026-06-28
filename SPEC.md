# Spec: AI Learning Journey Website

## Goal
A simple static website documenting a developer's journey learning
AI development — from first API call to a working autonomous agent. Built for
GitHub Pages (no build step, no server).

## Audience
- Future-me, as a reference
- Other engineers with a similar background considering the same path

## Tech requirements
- Plain HTML/CSS/JS only — no framework, no build tool, no npm dependency for the
  site itself (GitHub Pages must serve it with zero processing)
- Mobile responsive
- Fast-loading — no heavy assets, no external font/CDN dependency required to read content
- Code snippets should use a simple syntax-highlighted `<pre><code>` block (a small
  CSS-only highlight is fine — avoid pulling in a large JS highlighting library)

## Site structure
- `index.html` — landing page: short intro, a visual timeline/nav linking to all 6 stages
- `stages/stage1.html` through `stages/stage6.html` — one page per stage
- `css/style.css` — shared styling

## Content map (per stage page)
Each stage page should include:
1. **What was built** — the actual project (e.g. "multi-turn chatbot in Python")
2. **Key concept(s)** — the 2-3 ideas that mattered most
3. **One real "gotcha"** — something that didn't work the first time, and why
   (these are genuinely the most useful parts of the journey — don't sanitize them out)
4. A short code snippet illustrating the core mechanic, where relevant

Stage-by-stage content seeds (expand freely):
- **Stage 1** — Multi-turn chatbot, Python/TypeScript, system prompts, context window basics
- **Stage 2** — Structured JSON output, prompt engineering, Android code reviewer
- **Stage 3** — Tool use / function calling, the agent loop, long-running-agent context bloat
- **Stage 4** — RAG: embeddings, chunking, vector search, "chat with your docs"
- **Stage 5** — MCP: client/server/host roles, stdio vs HTTP transport, the real-world
  debugging saga (proxy issues, Docker networking, IPv6 vs IPv4 loopback)
- **Stage 6** — ReAct agents, harness engineering, generator/verifier separation,
  rate-limit-aware design, the terminology landscape (prompt → context → harness → loop engineering)

## Tone
- Conversational, first-person, written like a real engineer's notes — not corporate
  marketing copy
- Okay to be honest about what was confusing or what failed before it worked

## Design preferences
> _Add your own details here — color palette, dark mode, any visual style you have
> in mind, whether you want images/diagrams, etc._

## Acceptance criteria
- [ ] Site runs correctly when opened locally via `index.html` with no build step
- [ ] All 6 stage pages exist and link correctly from the landing page and to each other
- [ ] Page is readable and usable on a phone-width viewport
- [ ] No broken links, no console errors
- [ ] Deployed successfully via GitHub Pages at the repo's Pages URL

## Out of scope (for v1)
- No backend, no database, no live demos of the actual agents
- No CMS — content is hand-written HTML

---
## Your additional notes
> _Add anything else here before handing this to Claude Code — specific phrasing
> you want, sections to add/remove, examples you want highlighted, etc._
