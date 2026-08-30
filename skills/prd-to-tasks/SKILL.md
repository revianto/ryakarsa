---
name: prd-to-tasks
description: Break an approved PRD (Product Requirement Document) into a concrete, ordered task backlog a dev team (human or AI) can start executing — one task list per phase, with acceptance criteria, estimates, and dependencies pulled from the PRD itself. Use when the user has a finished PRD and wants it turned into tasks, tickets, a backlog, or a sprint plan — phrasings like "buat task dari PRD ini", "breakdown fitur jadi task", "pecah PRD jadi backlog", "generate tickets from this PRD", "convert PRD to sprint plan". For creating the PRD itself, use the prd skill; for cleaning up a messy PRD first, use prd-refine.
---

# PRD → Tasks

Turn an already-approved PRD into an execution-ready backlog — **without re-deciding scope, priority, or phasing**. Everything here comes from the PRD; this skill only decomposes and sequences it.

Language: match the user's language and the PRD's own language.

**Golden rule:** a task with no acceptance criteria in the PRD doesn't get invented ones — it gets flagged and handed back (see Handoff). Never guess what "done" means for a feature the PRD left vague.

## Step 1 — Locate and scope

Read the PRD at the path the user gives, or `./PRD.md` if none is given — ask first if neither exists.

Ask (via **AskUserQuestion** when available, else a numbered list) only what changes the shape of the backlog:
- Which phase(s) to break down now — just Fase 1 (MVP), or everything.
- Estimate unit — story points, hours/days, or T-shirt size (S/M/L).
- Solo builder or a team with roles (frontend/backend/design/QA) — this decides whether tasks get a role label.

Skip anything already obvious from the PRD (e.g. if it names a solo AI-assisted build, don't ask about team roles).

## Step 2 — Decompose per feature

For each feature in scope, in PRD order:

1. Read its description, sub-features, and acceptance criteria verbatim.
2. Split into 1–5 tasks along natural seams (data model, backend/API, UI, integration, tests) — only where the feature is actually big enough to need it. A one-line P2 feature stays one task; don't manufacture busywork.
3. Each task inherits the slice of acceptance criteria it's responsible for — copy the PRD's checkbox wording, don't rephrase into something looser.
4. If a feature has no acceptance criteria at all, still create a task but mark it `⚠ butuh acceptance criteria` instead of inventing one — this belongs back in `prd-refine` or a decision from the user, not a guess here.

Task fields:
- **ID** — `T<fase>.<fitur>.<n>`, e.g. `T1.1.2`.
- **Title** — verb-first, one line ("Implement editor undangan form").
- **Acceptance criteria** — checkboxes, from the PRD.
- **Estimate** — in the unit chosen in Step 1.
- **Dependencies** — other task IDs that must land first (same feature or cross-feature).
- **Label** — role tag (frontend/backend/design/QA/infra), only if a team was chosen in Step 1.

## Step 3 — Sequence

Within each phase, order tasks so dependencies come first. Call out cross-feature dependencies explicitly (e.g. "T1.2.1 butuh T1.1.3 selesai dulu karena share data model") — don't bury them inside individual tasks.

Phase boundaries from the PRD are fixed: never pull a later-phase task earlier or vice versa just because it'd resequence nicely.

## Step 4 — Write the backlog

Write to `./TASKS.md` (or the path the user gave), grouped by phase, each phase as a section with its tasks as a checklist:

```markdown
## FASE 1 — MVP

### T1.1.1 — Implement form input undangan (FE)
- [ ] Field nama pengantin, tanggal, lokasi tervalidasi
- [ ] Data tersimpan otomatis; isi tidak hilang saat refresh
Estimate: 3 SP · Depends on: —
```

Close with a summary in ≤6 lines: file path, task count per phase, any `⚠ butuh acceptance criteria` flags and how many, and the critical-path dependency chain if one stands out.

## Handoff

- If the PRD itself has vague/missing acceptance criteria on features the user wants broken down now, say so and suggest running `prd-refine` first — don't patch it silently here.
- If no PRD exists yet, point to the `prd` skill instead of starting from a raw idea.
