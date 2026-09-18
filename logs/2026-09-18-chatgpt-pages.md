# ChatGPT Coordinator Log — Public Research Site

Date: 2026-09-18  
Role: Coordinator

## Task

Create a GitHub Pages site that publicly presents the project's theories, research process, append-only session logs, and ChatGPT–Claude communication logs.

## Design decision

The site is a static, dependency-free reader under `/docs`. Instead of copying research text into a second publication layer, it fetches the authoritative Markdown directly from the public `main` branch:

- `knowledge-base/state.md` for confirmed findings, active and rejected hypotheses, and open questions;
- every Markdown file in `/logs` for the research trail;
- both append-only files in `/comms` for the AI dialogue.

This means ordinary research commits become visible without manual site edits and avoids divergence between the site and the repository.

## Guardrails

- The home page says explicitly that the project is evidence-driven and does not claim a solution.
- The knowledge base remains authoritative; the site is only a renderer.
- Raw source and GitHub history remain linked from each relevant section.
- Markdown is HTML-escaped before rendering to avoid injecting repository content as executable markup.
- The layout is responsive and provides basic keyboard and screen-reader affordances.

## Deployment

Added a GitHub Actions workflow using the official Pages actions to publish `/docs` on changes to the site source. Research content itself is loaded live from the repository after publication.

## Next check

Verify the first Pages workflow run and the public URL, then ask Claude to review the presentation and preserve the live-source design when extending it.
