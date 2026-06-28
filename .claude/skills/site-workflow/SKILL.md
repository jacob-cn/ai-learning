---
name: site-workflow
description: Use this whenever adding a new stage page, updating a demo's README, citing real code on a page, deciding whether something belongs on a page or in a README, styling pages for readability (tables/charts/images), checking or introducing terminology, or folding a future deep-dive conversation into the site. Covers the full content workflow for the AI Learning Journey site.
---

# Adding a new stage

1. Add a row to the Stage registry in CLAUDE.md FIRST — pick the next number,
   name the topic
2. Create `stages/stageN-<topic>.html` following the **Stage page anatomy**
   below
3. Add a stage card to the `index.html` timeline (title + one-line summary
   only — NO demo language listed), and keep the `stage-next` card last
4. Repoint pagers: old last stage's "next" → the new stage; new stage's
   "next" → `stage-next.html`
5. If there's real tested code, copy a redacted version into
   `demos/NN-<topic>-<language>/` — see CLAUDE.md's Security rules
6. Never edit SPEC.md (sole exception: scrubbing personal/identifying info)
7. Keep tone consistent: conversational, first-person, honest about what
   didn't work the first time
8. Add an entry to CHANGELOG.md

# Stage page anatomy

Same heading order on every page:

1. **What I built** — the actual project, followed immediately by a
   `.demo-link` button to the GitHub demo folder. Base URL:
   `https://github.com/jacob-cn/ai-learning/tree/main/demos/<folder>`
2. **Key concepts** — the durable ideas, with a hand-authored SVG diagram for
   anything sequential, proportional, or spatial (see Visual presentation)
3. **Gotchas & lessons** — keep it SHORT (a `.callout`, a sentence or two).
   Only AI-/engineering-relevant lessons belong here; operational specifics
   (a venv quirk, a proxy fix, a Docker binding) go to the demo README, not
   the page. Drop a point entirely if it's neither.
4. **The core mechanic, in code** — a 10-20 line snippet, then ALWAYS a
   `.codewalk` numbered list explaining it in plain language so a reader who
   doesn't know Python/TS can still follow. Don't reference the README's
   "What to check" here — the page explains the mechanism, not how to run it.

# Demo README convention

Every `demos/` folder needs a README with exactly three sections:
**Setup** (install + API key, point to `.env.example`, never a real key),
**Run** (exact command + one example input), **What to check in the result**
(concrete signals a correct run actually shows — not just "it should work" —
plus any known gotcha from this project's own history).

# Citing real code on a page

Prefer a short snippet (10-20 lines) over the full file, followed by a link
to the real file in `demos/`. Don't reconstruct whole files inline.

# What belongs on a page vs in a README

- **Page** = durable AI/engineering concepts: how something works, why it
  matters, generally true beyond this one project
- **README** ("What to check") = operational/practical specifics to THIS demo
  (a proxy fix, a venv quirk, a specific error and its fix)
- If it's neither AI-relevant nor useful to a reader, it's fine to drop it

# Visual presentation

- Clear headings, short paragraphs, generous whitespace over dense prose
- A table whenever comparing more than 2 things side by side
- A diagram for anything sequential, proportional, or spatial. Hand-author it
  as inline SVG wrapped in `<figure><div class="diagram">…</div></figure>` —
  NO JS chart libraries (must work on GitHub Pages with zero build).
- Diagrams MUST use the shared SVG token classes in `css/style.css`
  (`.svg-box`, `.svg-box-a`, `.svg-box-t`, `.svg-lbl`, `.svg-sub`, `.svg-ph`,
  `.svg-ar`, `.svg-dot`, …) rather than hard-coded colours, so they adapt to
  dark mode. Every SVG needs `role="img"` + a real `aria-label`.
- Theme is warm/Claude-like (clay accent `--accent`, teal secondary for
  diagrams); all colours come from CSS variables — never hard-code hex on a page.
- Images only where they genuinely aid understanding, always with real `alt` text
- Same heading hierarchy across every stage page (see Stage page anatomy)
- When in doubt, readability over cleverness

# Canonical terminology

The full canonical term table lives in **`terminology.md`** (next to this file) —
open it whenever you're checking, using, or introducing a term. Core rules:

- Use the exact canonical terms everywhere; mention a synonym once on first use,
  then stick to the canonical one.
- `terminology.md` is the source; `glossary.html` is its reader-facing mirror.
  When a new term is introduced anywhere, add it to BOTH, in the same edit, in
  first-appears order.

# Future deep-dives

1. End of a useful conversation: ask for a short addendum — which stage,
   a handful of bullet points, not a transcript
2. Save it as e.g. `ADDENDUM-stage5-topic.md`
3. Hand to Claude Code: "Read this addendum and CLAUDE.md. Add it to the
   matching stage page using the canonical terms in `terminology.md`. If a new
   term appeared, add it to BOTH `terminology.md` and glossary.html. Add a
   CHANGELOG.md entry. Tell me when done so I can delete the addendum."
4. Delete the addendum once merged
