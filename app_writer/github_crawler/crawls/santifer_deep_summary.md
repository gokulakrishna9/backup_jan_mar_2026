# GitHub Profile Deep Dive: santifer (Santiago Fernández de Valderrama)

> AI Product Manager · Solutions Architect · Forward Deployed Engineer
> Ex-founder with 16+ years building products. After scaling and selling his business (exit 2025), now focused on AI solutions.

Total public repositories: 10 (9 original + 1 fork)

---

## 1. [career-ops](https://github.com/santifer/career-ops)

**AI-powered job search system built on Claude Code.**

| Metric | Value |
|--------|-------|
| Language | JavaScript (Node.js, mjs modules) |
| Stars | 32,957 |
| Forks | 6,501 |
| License | MIT |
| Topics | ai-agent, anthropic, automation, career, claude, claude-code, cli, golang, interview-prep, job-search |

### What it does
A full-featured AI job search pipeline that automates offer evaluation, CV generation, portal scanning, and batch processing. Built as a Claude Code skill system with 14+ modes (evaluate, compare, scan, apply, interview-prep, batch, etc.).

### Architecture
- **Core engine:** Node.js scripts (`.mjs`) orchestrated by Claude Code via skill files in `.claude/skills/`
- **Dashboard:** Go (Golang) web dashboard (`dashboard/main.go`) for visual pipeline tracking
- **PDF generation:** Playwright-based HTML-to-PDF CV generator
- **Portal scanner:** Zero-LLM-cost scanner that hits Greenhouse/Ashby/Lever APIs directly
- **Batch processing:** Parallel evaluation workers with tracker merge system
- **Data contract:** Strict separation between user-layer files (CV, profile, reports) and system-layer files (modes, scripts)
- **Multi-language:** Modes available in English, German (DACH market), French, Japanese, Portuguese, Russian, Korean, Chinese
- **Update system:** Self-updating with rollback support (`update-system.mjs`)
- **CI/CD:** GitHub Actions with 63+ test checks, auto-labeler, Dependabot, branch protection

### Key files
- `modes/` — 14+ skill mode definitions (oferta, scan, batch, pdf, interview-prep, etc.)
- `config/profile.yml` — User personalization
- `dashboard/` — Go dashboard with internal packages
- `generate-pdf.mjs` — Playwright PDF generator
- `scan.mjs` — Portal scanner
- `batch/` — Batch processing system
- `templates/cv-template.html` — HTML CV template
- `CLAUDE.md` — Comprehensive agent instructions (the brain of the system)

---

## 2. [cv-santiago](https://github.com/santifer/cv-santiago)

**Interactive portfolio with AI chatbot, agentic RAG, automated evals, and LLMOps dashboard.**

| Metric | Value |
|--------|-------|
| Language | TypeScript / React 19 / HTML |
| Stars | 316 |
| Forks | 118 |
| Topics | ai, chatbot, claude, langfuse, llm, llmops, observability, portfolio, react, tailwindcss, typescript, vercel, vite |

### What it does
Santiago's personal portfolio website (santifer.io) with an integrated AI chatbot that can answer questions about his experience. Features text + voice chat modes, agentic RAG for portfolio content retrieval, 71 automated evaluations, a 6-layer prompt injection defense system, and full LLMOps observability via Langfuse.

### Architecture
- **Frontend:** React 19 + TypeScript + Tailwind CSS + Vite, deployed on Vercel
- **API layer:** Vercel Edge Functions (`api/chat.js`, `api/rag-search.js`, `api/voice-token.js`)
- **LLM:** Claude API (Anthropic SDK) with Langfuse tracing for every conversation
- **RAG:** Portfolio content ingestion with vector search (`scripts/ingest-rag.ts`, `scripts/embed-evals.ts`)
- **Voice mode:** ElevenLabs integration with audio analyser (`src/useVoiceMode.ts`, `src/VoiceOrb.tsx`)
- **Evals suite:** 31+ tests across 6 categories (factual accuracy, persona adherence, boundary testing, language handling, response quality, safety/jailbreak) with LLM judge using Haiku
- **Case study pages:** Dedicated pages for each project (BusinessOS, CareerOps, Jacobo, iRepair, Programmatic SEO, N8n for PMs)
- **SEO:** Sitemap generation, IndexNow pinging, Google Search Console integration, `llms.txt` for AI crawlers
- **Security:** Jailbreak detection with alerts, input length validation, prompt fingerprint detection

### Key files
- `api/chat.js` — Main chat endpoint with RAG, Langfuse tracing, prompt injection defense
- `evals/` — Full evaluation suite with deterministic + LLM judge assertions
- `src/FloatingChat.tsx` — Chat UI component
- `src/VoiceOrb.tsx` — Voice mode UI
- `scripts/` — 15+ utility scripts (adversarial testing, RAG ingestion, prompt sync, etc.)
- `chatbot-prompt.txt` — System prompt for the AI avatar

---

## 3. [jacobo-workflows](https://github.com/santifer/jacobo-workflows)

**7 production n8n workflows from a multi-agent AI system (WhatsApp + Voice).**

| Metric | Value |
|--------|-------|
| Language | N/A (JSON workflow files) |
| Stars | 117 |
| Forks | 35 |
| Topics | ai-agents, elevenlabs, hitl, multi-agent, n8n, tool-calling, voice-ai, whatsapp |

### What it does
Open-source release of 7 real production n8n workflows from "Jacobo," an omnichannel AI agent that handled ~90% of customer interactions for a phone repair business (Santifer iRepair). The system ran in production for 2 years handling WhatsApp and phone calls.

### Architecture
- **Orchestration:** n8n workflow automation platform
- **Channels:** WhatsApp (via WATI) + Voice (ElevenLabs) + Aircall PBX
- **Agent pattern:** Multi-agent with sub-agent orchestration via tool calling
- **HITL:** Human-in-the-loop handoff with full conversation context

### Workflow files
- `jacobo-chatbot-v2.json` — Main chatbot orchestrator
- `subagente-citas.json` — Appointments sub-agent
- `hacer-pedido.json` — Order placement sub-agent
- `presupuesto-modelo.json` — Quote/pricing model sub-agent
- `calculadora-santifer.json` — Price calculator
- `contactar-agente-humano.json` — Human agent handoff
- `enviar-mensaje-wati.json` — WhatsApp message sender (WATI integration)

---

## 4. [santifer-irepair](https://github.com/santifer/santifer-irepair)

**Programmatic SEO website that generated 15,500+ unique pages from an Airtable ERP.**

| Metric | Value |
|--------|-------|
| Language | Astro + TypeScript |
| Stars | 12 |
| Forks | 7 |
| Topics | airtable, astro, nodejs, programmatic-seo, seo, tailwindcss, typescript, vercel |

### What it does
The website for Santiago's phone repair business (Santifer iRepair in Seville, Spain). Uses programmatic SEO to auto-generate thousands of pages from Airtable data — one page per device model × repair type combination. Reached 2.26M impressions and 2,000 monthly clicks in Google Spain.

### Architecture
- **Framework:** Astro 4.x with SSG (Static Site Generation)
- **Styling:** Tailwind CSS
- **Data source:** Airtable API (device models, repair types, pricing from the business ERP)
- **Image pipeline:** Node.js scripts using Sharp for image processing + EXIF metadata injection for SEO
- **Deployment:** Vercel with analytics and speed insights
- **SEO:** Custom sitemap generation (regular + image sitemaps), structured data, programmatic page generation

### Key files
- `src/pages/` — Astro page templates for programmatic generation
- `scripts/` — Node.js image generation pipeline (brand images, model images, repair type images, review images, success stories)
- `public/modelos5.json` — Device model data
- `scripts/sitemaps.mjs` — Custom sitemap generator
- `astro.config.mjs` — Astro configuration with Vercel adapter

---

## 5. [claudeable](https://github.com/santifer/claudeable)

**Claude Code metaproject for creating professional web pages.**

| Metric | Value |
|--------|-------|
| Language | TypeScript |
| Stars | 12 |
| Forks | 7 |
| Topics | claude-code, mcp, react, shadcn-ui, tailwindcss, vite, web-development |

### What it does
A project scaffolding tool and Claude Code skill set for rapidly creating professional, production-ready web applications. Provides a Vite + React + shadcn/ui + Tailwind template with pre-configured MCP servers (Figma, Playwright, Supabase, image generation via Nanobanana).

### Architecture
- **Template:** Vite + React + TypeScript + shadcn/ui + Tailwind CSS
- **MCP integrations:** Figma (design import), Playwright (testing/screenshots), Supabase (backend), Nanobanana/Google (image generation)
- **Scaffolding:** Shell script (`new-project.sh`) to create new projects from template
- **Claude Code skills:** Pre-configured in `.claude/skills/` for web development best practices

### Key files
- `new-project.sh` — Project scaffolding script
- `templates/vite-react-shadcn/` — Full project template
- `.mcp.json` — MCP server configuration (Figma, Playwright, Supabase, Nanobanana)
- `.claude/skills/` — Claude Code skill definitions

---

## 6. [claude-eye](https://github.com/santifer/claude-eye)

**CLI tool that analyzes web animation videos frame-by-frame using Claude Vision.**

| Metric | Value |
|--------|-------|
| Language | TypeScript |
| Stars | 5 |
| Forks | 3 |
| Topics | animation, claude, cli, css, debugging, vision-ai |

### What it does
A developer tool for debugging CSS animations and transitions. Records a video of the animation, then uses Claude Vision API to analyze each frame, build a timeline of element states, and detect timing desyncs or issues.

### Architecture
- **CLI:** Commander.js with chalk/ora for terminal UI
- **Frame extraction:** ffmpeg-based frame extraction at configurable FPS
- **Analysis:** Claude Vision API analyzes each frame for element positions, states, and transitions
- **Timeline:** Builds a timeline tracking unique elements across frames, detecting desyncs
- **Output:** Markdown report + JSON data + extracted frames

### Key files
- `src/index.ts` — CLI entry point with `analyze` command
- `src/extract.ts` — ffmpeg frame extraction
- `src/analyze.ts` — Claude Vision API frame analysis
- `src/timeline.ts` — Timeline builder and desync detection
- `src/report.ts` — Report generation (Markdown + JSON)

---

## 7. [watermark-remover](https://github.com/santifer/watermark-remover)

**CLI tool to remove watermarks from images using YOLO detection + LaMa inpainting.**

| Metric | Value |
|--------|-------|
| Language | Python |
| Stars | 7 |
| Forks | 5 |
| License | MIT |
| Topics | ai, cli, image-processing, inpainting, lama, python, watermark-removal, yolo |

### What it does
An AI-powered CLI tool that automatically detects watermarks in images using YOLO object detection, then removes them using LaMa (Large Mask) inpainting. Falls back to corner-based masking if YOLO doesn't detect anything.

### Architecture
- **CLI:** Click-based Python CLI with verbose mode
- **Detection:** YOLO model for watermark bounding box detection with configurable confidence threshold
- **Inpainting:** Two methods — LaMa (higher quality) or OpenCV (faster)
- **Fallback:** Corner-based mask generation (configurable corner, width/height ratios)
- **Pipeline:** Load image → Detect watermark (YOLO) → Generate mask → Inpaint → Save

### Key files
- `watermark_remover/cli.py` — CLI interface with Click
- `watermark_remover/detector.py` — YOLO watermark detection + corner mask fallback
- `watermark_remover/inpainter.py` — LaMa and OpenCV inpainting engines
- `requirements.txt` — Dependencies
- `setup.py` — Package setup

---

## 8. [github-viral-ranking](https://github.com/santifer/github-viral-ranking) *(fork)*

**Analyze, compare, and predict GitHub repo growth. Find where your repo ranks among the most viral in history.**

| Metric | Value |
|--------|-------|
| Language | Python |
| Stars | 6 |
| Forks | 1 |
| License | MIT |
| Fork | Yes (from ChenLiu-1996/GitStarPercentile) |

### What it does
A collection of Python scripts to analyze GitHub star growth patterns. The core tool calculates your repo's star percentile among all GitHub repos. Santiago's additions include a viral ranking system that compares first-24-hour star counts against historically viral repos, plus visualization tools.

### Architecture
- **Percentile calculator:** Downloads GitHub star distribution CSV, calculates where your repo ranks
- **Viral ranking:** Fetches stargazer timestamps via GitHub API, counts first-24h and first-48h stars, ranks against known viral repos (AutoGPT, DeepSeek, ollama, etc.)
- **Visualizations:** Matplotlib-based charts — histograms, race charts, growth analysis
- **Data:** Cached star data in `data/viral_repos.json`, CSV stats in `stats/`

### Key files
- `git_star_percentile/__main__.py` — Star percentile calculator
- `viral_ranking.py` — First-day viral ranking against top repos
- `viral_tracker.py` — Track and update viral repo database
- `star_history.py` — Star growth history fetcher
- `plot_histogram.py`, `race_chart.py`, `viral_chart.py` — Visualization scripts

---

## 9. [claude-pulse](https://github.com/santifer/claude-pulse)

**SwiftBar plugin for macOS — real-time Claude API usage monitoring.**

| Metric | Value |
|--------|-------|
| Language | Shell (Bash) |
| Stars | 4 |
| Forks | 5 |
| Topics | api-usage, claude, macos, monitoring, rate-limiting, swiftbar |

### What it does
A macOS menu bar plugin (via SwiftBar) that monitors Claude Code API usage in real-time. Tracks both the 5-hour and 7-day rate limit windows, predicts when you'll hit caps, shows session history, and sends native macOS alerts at configurable thresholds.

### Architecture
- **Platform:** SwiftBar plugin (runs every 1 minute)
- **Auth:** Reads Claude Code OAuth token from macOS Keychain
- **API:** Fetches usage data from `api.anthropic.com/api/oauth/usage`
- **Features:**
  - 5-hour + 7-day window tracking with color-coded status circles
  - Token velocity calculation (tokens/hour)
  - Rate limit prediction (minutes until cap at current pace)
  - Recent sessions list with resume capability
  - Streak tracking (consecutive days of usage)
  - Smart tips based on usage patterns
  - Native macOS notifications at warning/critical thresholds
  - Configurable via JSON config file

### Key files
- `claude-pulse.1m.sh` — The entire plugin (single ~500-line bash script)

---

## 10. [santifer](https://github.com/santifer/santifer)

**GitHub Profile README.**

| Metric | Value |
|--------|-------|
| Language | N/A (Markdown) |
| Stars | 7 |
| Forks | 2 |

### What it does
Santiago's GitHub profile README showcasing his background, published case studies, tech stack, and certifications (Anthropic, Airtable, Make Academy).

---

## Summary: Tech Stack & Themes

| Technology | Used in |
|------------|---------|
| Claude API / Anthropic | career-ops, cv-santiago, claude-eye, claude-pulse, claudeable |
| TypeScript | cv-santiago, claude-eye, claudeable, santifer-irepair |
| React | cv-santiago, claudeable |
| Node.js | career-ops, santifer-irepair |
| Python | watermark-remover, github-viral-ranking |
| Go | career-ops (dashboard) |
| Bash/Shell | claude-pulse |
| n8n | jacobo-workflows |
| Astro | santifer-irepair |
| Tailwind CSS | cv-santiago, claudeable, santifer-irepair |
| Vercel | cv-santiago, santifer-irepair |
| Langfuse | cv-santiago |
| ElevenLabs | cv-santiago (voice), jacobo-workflows |
| YOLO / LaMa | watermark-remover |
| Playwright | career-ops (PDF gen) |
| Airtable | santifer-irepair |

### Recurring themes
- Heavy Claude/Anthropic ecosystem usage (5 of 10 repos)
- AI agent patterns: multi-agent orchestration, tool calling, HITL handoff
- LLMOps: evaluations, observability, prompt versioning, jailbreak defense
- Programmatic SEO and content generation at scale
- Developer tooling (CLI tools, menu bar plugins, animation debuggers)
- Bilingual (Spanish/English) with multi-language support
