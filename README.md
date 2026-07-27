# my-little-skills

A curated Codex and Claude Code plugin marketplace that bundles [Anthropic's official skills](https://github.com/anthropics/skills) with custom-built skills for developer workflows, document processing, design, and project-specific automation.

## Quick Start

### Claude Code

Register this marketplace:
```
/plugin marketplace add dabsdamoon/my-little-skills
```

Browse and install plugins:
```
/plugin
```
Then go to the **Discover** tab, or install directly:
```
/plugin install <plugin-name>@my-little-skills
```

### Codex

Connect the GitHub marketplace and install a plugin once for the current user:

```bash
codex plugin marketplace add dabsdamoon/my-little-skills --ref main
codex plugin add developer-workflow-skills@my-little-skills
```

The installed plugin is available in every repository opened by that user. Codex stores plugin configuration and cache data under `CODEX_HOME`, which defaults to `~/.codex`; installation is not shared automatically with other operating-system accounts.

#### `humanize-korean` installation

`humanize-korean` belongs to the `writing-skills` plugin and must be installed
explicitly before Codex or Claude Code can load it. Installing
`developer-workflow-skills` alone is not sufficient, even though
`generate-git-work-report` uses `humanize-korean` for Korean report narrative.

For Codex:

```bash
codex plugin add writing-skills@my-little-skills
```

For Claude Code:

```text
/plugin install writing-skills@my-little-skills
```

Adding or upgrading the marketplace only refreshes the available plugin
catalog and updates plugins that are already installed; it does not
automatically install newly published plugins. Start a new session if
`writing-skills:humanize-korean` does not appear immediately after
installation.

Run the shared update primitive at any time:

```bash
codex plugin marketplace upgrade my-little-skills
```

This refreshes the Git-backed marketplace and its installed plugins. The platform adapters below schedule this same command; they do not edit application repositories.

## Automatic Codex Updates

Clone this repository on each machine where updates should be scheduled, connect the marketplace as shown above, and run the adapter for that operating system. Each adapter captures the current `codex` executable and `CODEX_HOME`, runs once at login or user-manager startup, and checks daily afterward.

### Windows

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex-marketplace-updater.ps1 -RunNow
```

This installs the per-user Task Scheduler task `Codex-MyLittleSkills-Upgrade`. To target a non-default profile, pass `-CodexHome C:\path\to\codex-home`. To remove it:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall-codex-marketplace-updater.ps1
```

### macOS

```bash
sh scripts/install-codex-marketplace-updater.sh --run-now
```

This installs `~/Library/LaunchAgents/com.dabsdamoon.codex-my-little-skills-upgrade.plist`. A LaunchAgent runs for the signed-in user. For an unattended macOS service account, provision an equivalent LaunchDaemon through the machine's administration tooling.

### Linux

```bash
sh scripts/install-codex-marketplace-updater.sh --run-now
```

This installs and enables the systemd user timer `codex-my-little-skills-upgrade.timer`. On a headless server, run the installer as the account that owns the Codex installation and keep that user's systemd manager active:

```bash
sudo loginctl enable-linger <service-account>
```

For macOS or Linux with a non-default profile, pass `--codex-home /path/to/codex-home`. Remove either POSIX adapter with:

```bash
sh scripts/uninstall-codex-marketplace-updater.sh
```

The updater logs to `$CODEX_HOME/log/marketplace-updates.log` and keeps one rotated backup. Push plugin changes to the tracked branch and keep the version and core metadata aligned across both plugin manifests. New Codex sessions load the refreshed plugin; restart Codex if an update is not detected in an existing session.

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| **document-skills** | xlsx, docx, pptx, pdf | Create, read, edit spreadsheets, Word docs, presentations, and PDFs |
| **design-skills** | frontend-design, algorithmic-art, canvas-design, brand-guidelines, theme-factory, slack-gif-creator, web-artifacts-builder | Frontend UI, generative art, visual design, and brand styling |
| **developer-workflow-skills** | pr-creator, pr-checklist-verifier, setup-release-pipeline, deploy-check, webapp-testing, refactoring-resistant-tests, generate-git-work-report, docker-ram-checker, mcp-builder, prompt-optimizer, subagent-creator, debugging-retrospective, gcloud-direnv-setup | PR docs, release pipelines, deploy checks, Git-based execution histories, browser testing, refactoring-resistant testing, Docker memory checks, debugging postmortems, and more |
| **fde-estimation-skills** | capture-customer-outcomes, document-field-discovery, collect-as-built-evidence, define-estimation-policy, reconcile-scope-delta, generate-estimate-package | Interactive, evidence-backed FDE discovery, reviewed staffing, seniority, rate, scope, and effort reconciliation, budgetary estimates, and basis-of-estimate reports |
| **writing-skills** | doc-coauthoring, internal-comms, skill-creator, system-prompt-creator, humanize-korean | Documentation workflows, internal comms, skill/prompt authoring, Korean AI-text humanizing |
| **resume-skills** | resume-formatter, resume-translator, resume-project-summary | Resume formatting, EN/JP/KR/CN translation, portfolio summaries from codebases |
| **config-skills** | claude-config-migrator, update-notes, update-houmy-notes | Migrate Claude Code config between repos, write update notes |
| **llm-wiki-skills** | make-llm-wiki-raw, wikify-raw | Capture raw LLM-Wiki sources and turn them into linked Obsidian wiki pages |
| **houmy-skills** | houmlike-design, houm-refactoring | Houmy maternity care service: branded UI design and systematic codebase refactoring |
| **claude-api** | claude-api | Claude API & SDK reference across Python, TypeScript, Go, Java, PHP, Ruby, C#, curl |
| **translation-skills** | translate-book | Translate entire books (PDF/DOCX/EPUB) into any language using parallel sub-agents |

## What's Included from Upstream

This marketplace tracks [anthropics/skills](https://github.com/anthropics/skills) as an upstream remote. The following skills come directly from Anthropic's official repository:

algorithmic-art, brand-guidelines, canvas-design, claude-api, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx

To sync with upstream:
```bash
git fetch upstream
git rebase upstream/main
```

## Custom Skills

These skills are original to this marketplace — not available in Anthropic's official repo.

### Developer Workflow

| Skill | What It Does |
|-------|-------------|
| **pr-creator** | Generates PR documentation with blast radius analysis (how many files depend on your changes) and OWASP security scanning of the diff |
| **setup-release-pipeline** | Sets up an opinionated production-pointer release workflow for branch-tracking hosts: `main` stays latest-code/release-candidate, `production` is the live branch, and `run_deploy.sh` ships explicitly without deploy secrets |
| **deploy-check** | Checks deployment readiness and records a concise deploy report |
| **docker-ram-checker** | Tests Docker container memory usage before deploying to Cloud Run, ECS, or Kubernetes |
| **prompt-optimizer** | Reduces token usage and improves cache efficiency for production LLM prompts |
| **subagent-creator** | Generates repository-specific Claude Code subagents tailored to your tech stack |
| **debugging-retrospective** | Summarizes debugging sessions into educational postmortems with lessons learned |
| **generate-git-work-report** | Produces timestamped external and internal Git work reports from a verifiable evidence snapshot, with conservative Korean narrative editing and reference-matched DOCX/PDF QA |
| **gcloud-direnv-setup** | Configures per-directory GCP credentials with direnv for multi-account setups |
| **refactoring-resistant-tests** | Builds behavior-focused tests that survive internal refactors and use stable observable boundaries |

### FDE Estimation

| Skill | What It Does |
|-------|-------------|
| **capture-customer-outcomes** | Preserves the customer's original outcomes, explicit scope, assumptions, constraints, and approval baseline |
| **document-field-discovery** | Separates field observations, FDE inferences, solution decisions, and customer validation |
| **collect-as-built-evidence** | Builds a read-only implementation evidence record from Git and delivery artifacts without treating commits as hours |
| **define-estimation-policy** | Defines dated rates, cost composition, tax, uncertainty, and validity rules |
| **reconcile-scope-delta** | Maps baseline, discovery, and implementation evidence into independent commercial scenarios |
| **generate-estimate-package** | Produces and verifies a budgetary estimate, basis of estimate, and optional change or remaining-work documents from one calculation |

### Writing

| Skill | What It Does |
|-------|-------------|
| **humanize-korean** | Rewrites Korean AI-generated text to sound natural while preserving facts, claims, names, numbers, and quoted text |
| **doc-coauthoring** | Helps co-author structured documentation with the user |
| **internal-comms** | Drafts and refines internal communications |
| **system-prompt-creator** | Guides production-grade system prompt creation |
| **skill-creator** | Helps create and update reusable agent skills |

### Translation

| Skill | What It Does |
|-------|-------------|
| **translate-book** | Translates entire books (PDF/DOCX/EPUB) into any language using 8 parallel sub-agents with SHA-256 manifest validation. Outputs HTML, DOCX, EPUB, PDF. Requires Calibre + Pandoc. ([source: deusyu/translate-book](https://github.com/deusyu/translate-book)) |

### Resume & Career (Work in Progress)

> These skills are still being curated and may not work reliably yet.

| Skill | What It Does |
|-------|-------------|
| **resume-formatter** | Reformats resumes to match specific company templates while preserving content |
| **resume-translator** | Translates resumes between English and Japanese, Korean, or Chinese (.docx) |
| **resume-project-summary** | Generates portfolio-ready project summaries from codebases for resumes |

### Configuration & Ops

| Skill | What It Does |
|-------|-------------|
| **claude-config-migrator** | Transfers Claude Code config (rules, skills, hooks, MCP) between repositories |
| **system-prompt-creator** | Guides creation of production system prompts following OpenAI, Anthropic, Google, and OWASP best practices |
| **update-notes** | Writes concise release/update notes for projects |

### LLM Wiki

| Skill | What It Does |
|-------|-------------|
| **make-llm-wiki-raw** | Creates raw source notes in `/Users/dabsdamoon/LLM-Wiki/LLM-Wiki/raw/inbox` from URLs, files, pasted text, or project artifacts |
| **wikify-raw** | Ingests raw LLM-Wiki sources into `wiki/sources`, `wiki/entities`, `wiki/concepts`, `wiki/syntheses`, `wiki/index.md`, and `wiki/log.md` |

### Houmy (Project-Specific)

| Skill | What It Does |
|-------|-------------|
| **houmlike-design** | Branded UI design for Houmy, a maternity care service — applies Houm's design philosophy to web interfaces |
| **houm-refactoring** | Systematic refactoring for Houmy's Python/FastAPI + React/Vite codebase — replaces implicit/magic patterns with explicit, grep-able code |
| **update-houmy-notes** | Writes update notes specific to the Houmy repository |

## Repository Structure

```
.claude-plugin/
  marketplace.json          # Marketplace registry
plugins/
  document-skills/          # Plugin manifests and skills/
  design-skills/
  developer-workflow-skills/
  fde-estimation-skills/
  writing-skills/
  resume-skills/
  config-skills/
  llm-wiki-skills/
  houmy-skills/
skills/                     # Source skills (copied into plugins)
spec/                       # Agent Skills specification
template/                   # Skill template for creating new skills
scripts/                    # Cross-platform Codex marketplace updater adapters
```

## Creating a New Skill

Each skill is a folder with a `SKILL.md`:

```markdown
---
name: my-skill
description: "When and how to trigger this skill"
---

# Instructions for Claude here...
```

To bundle skills into a dual-compatible plugin, create `plugins/<name>/.codex-plugin/plugin.json` and `plugins/<name>/.claude-plugin/plugin.json`, then add the plugin to `.claude-plugin/marketplace.json`. Keep their versions and core metadata aligned; the Codex manifest can additionally contain its required `interface` metadata.

## Links

- [Agent Skills standard](https://agentskills.io)
- [Skills documentation](https://code.claude.com/docs/en/skills)
- [Plugins documentation](https://code.claude.com/docs/en/plugins)
- [Codex plugin documentation](https://learn.chatgpt.com/docs/build-plugins)
- [Upstream: anthropics/skills](https://github.com/anthropics/skills)
