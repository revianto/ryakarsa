# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`ryakarsa` is not an application — it's a Claude Code / ZCode **plugin** distributing a set of skills (Markdown instruction files with YAML frontmatter, plus reference docs). There is no build, lint, or test suite; "development" here means editing `SKILL.md` files and their `references/` docs, then syncing and publishing.

## Source of truth vs. this repo

**The actual source of truth is `~/.agents/skills/`, not `skills/` in this repo.** This repo's `skills/` directory is a synced copy. Edits made only inside the repo checkout will be silently overwritten (via `rsync --delete`) the next time `scripts/sync-and-push.sh` runs from a machine with `~/.agents/skills/` populated.

Correct workflow when changing a skill:
1. Edit the skill under `~/.agents/skills/<skill-name>/`.
2. Run `./scripts/sync-and-push.sh` — it rsyncs each skill in its `SKILLS` array from `~/.agents/skills/<skill>/` into `skills/<skill>/`, validates frontmatter, then commits and pushes if anything changed.
3. If `~/.agents/skills/` isn't available in the current environment, edit `skills/` directly in the repo and remember to backport the same change to `~/.agents/skills/` before the next sync (otherwise it gets clobbered).

When adding a brand-new skill, add its name to the `SKILLS=(...)` array in `scripts/sync-and-push.sh` too, or the sync script will silently skip it.

## Commands

```bash
./scripts/sync-and-push.sh   # sync ~/.agents/skills -> skills/, validate frontmatter, commit & push if changed
```

The script's frontmatter validation (also worth running manually after hand-editing `skills/`) requires, for every `skills/*/SKILL.md`:
- `name: <dirname>` matching the containing folder name exactly
- a non-empty `description:` field

## Architecture

**Dual plugin manifest.** The repo ships two manifests pointing at the same `skills/` directory so one repo serves both clients:
- `.claude-plugin/plugin.json` — Claude Code
- `.zcode-plugin/plugin.json` — ZCode

Both must be bumped and kept in sync (version + description) together — there's no single source for the version number.

**Skill anatomy.** Each skill is a folder under `skills/` with a required `SKILL.md` (frontmatter: `name`, `description`) and optional `references/*.md` for material too long to keep inline (loaded by the model only when the skill's SKILL.md tells it to). The `description` field is what triggering is matched against, so it enumerates concrete trigger phrases (including Indonesian ones) rather than a generic summary.

**How the four skills relate:**
- `prd` — raw idea → PRD.md, via interview → editable phase/feature plan → final document. Uses `references/question-bank.md` (which questions to ask per project type) and `references/prd-template.md` (section-by-section PRD skeleton).
- `prd-refine` — takes an existing (possibly messy) PRD and tidies it without changing product intent; backs up the original to `<name>_old.md` before overwriting.
- `prd-to-tasks` — takes an *approved* PRD and decomposes it into a dependency-ordered `TASKS.md` backlog, plus a per-feature QA test-case checklist (happy path / edge cases / error handling) appended after each feature's tasks. Refuses to invent acceptance criteria (or test cases) a feature doesn't have, handing that back to `prd-refine` instead.
- `uiux-guide` — applies UI/UX theory (60-30-10 color, 8-point grid, WCAG contrast, Gestalt/cognitive laws, thumb zone, etc.) in "design" or "review" mode; the condensed rules live in `SKILL.md`, the full theory/citations in `references/panduan-lengkap.md`.

These four are meant to be chained in sequence (idea → `prd` → `prd-refine` if messy → `prd-to-tasks` → build with `uiux-guide` applied), and each skill's frontmatter description explicitly hands off to the right neighbor rather than overlapping scope.

**Cross-client tool differences matter.** Interactive question-asking (`AskUserQuestion`) is available in both Claude Code and ZCode, not exclusive to either — skills must not gate its use on a specific client name, only on whether the tool is actually present in the current session, falling back to a numbered text list otherwise.

**Language rule.** Every skill runs in the user's language (the templates/examples are Indonesian but are explicitly meant to be rendered in whatever language the user is using).

**Golden rule shared across the PRD skills.** Never silently invent a product decision — mark it "(asumsi)"/"(perlu konfirmasi)" or push it to *Open Questions*. This is treated as a hard constraint, not a suggestion, in `prd`, `prd-refine`, and `prd-to-tasks`.
