---
name: prd-to-tasks
description: Break an approved PRD (Product Requirement Document) into a concrete, ordered task backlog a dev team (human or AI) can start executing, plus a QA test-case checklist (happy path, edge cases, error handling) per feature so the PRD doesn't get called "done" without a way to verify it. One task list per phase, with acceptance criteria, estimates, and dependencies pulled from the PRD itself. Use when the user has a finished PRD and wants it turned into tasks, tickets, a backlog, a sprint plan, or a test-case/QA checklist before ship — phrasings like "buat task dari PRD ini", "breakdown fitur jadi task", "pecah PRD jadi backlog", "generate tickets from this PRD", "convert PRD to sprint plan", "buatkan test case dari PRD/fitur ini", "checklist QA sebelum rilis". For creating the PRD itself, use the prd skill; for cleaning up a messy PRD first, use prd-refine.
---

# PRD → Tasks

Turn an already-approved PRD into an execution-ready backlog **and** a QA checklist — **without re-deciding scope, priority, or phasing, and without inventing product behavior**. Everything here comes from the PRD; this skill only decomposes, sequences, and verifies it.

Language: match the user's language and the PRD's own language.

**Golden rule:** a task or test case with no acceptance criteria behind it doesn't get invented ones — it gets flagged and handed back (see Handoff). Never guess what "done" or "correct" means for a feature the PRD left vague.

## Step 1 — Locate and scope

Read the PRD at the path the user gives, or `./PRD.md` if none is given — ask first if neither exists.

**Existing TASKS.md:** if a backlog already exists at the target output path, read it before decomposing. It may have `[x]` checked items representing real completed work — this run must **merge**, never blindly overwrite.

Ask (via **AskUserQuestion** when available, else a numbered list) only what changes the shape of the output:
- Which phase(s) to break down now — just Fase 1 (MVP), or everything.
- Estimate unit — story points, hours/days, or T-shirt size (S/M/L).
- Solo builder or a team with roles (frontend/backend/design/QA) — this decides whether tasks get a role label.
- **Include test-case checklist?** — default yes; skip only if the user explicitly just wants tasks.

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

## Step 3 — Test-case checklist per feature

Skip this step if the user opted out in Step 1. For each feature that has at least one acceptance criterion:

1. **Happy path** — one test case per acceptance criterion, phrased as a verifiable check, not just the checkbox restated ("Isi form lengkap → data tersimpan, muncul di preview").
2. **Edge cases** — boundary and unusual-but-valid input implied by the feature's own fields/limits (empty input, max length, duplicate submission, concurrent edit) — only ones the PRD's fields actually make possible, not generic filler.
3. **Error handling** — what the PRD implies should fail gracefully (invalid input, network failure, permission denied, file-too-large where a limit is stated) — if the PRD names a specific limit or error message, use it verbatim; otherwise mark the case `(perlu konfirmasi perilaku)` instead of inventing the expected behavior.

A feature with no acceptance criteria gets no test cases either — it inherits the same `⚠ butuh acceptance criteria` flag from Step 2, not fabricated QA scenarios.

## Step 4 — Sequence

Within each phase, order tasks so dependencies come first. Call out cross-feature dependencies explicitly (e.g. "T1.2.1 butuh T1.1.3 selesai dulu karena share data model") — don't bury them inside individual tasks.

Phase boundaries from the PRD are fixed: never pull a later-phase task earlier or vice versa just because it'd resequence nicely.

## Step 5 — Write the backlog

**Merge, don't overwrite, when TASKS.md already exists:** match items by task ID and by the checkbox's own text, not by position. Carry forward `[x]` for any task/acceptance-criteria/test-case line whose ID and wording are unchanged. If a task's title or criteria changed from the PRD, treat it as reset (unchecked) — what's being verified is different now, so a stale checkmark would be a false signal. A previously-listed task that no longer matches anything in the current PRD scope doesn't get silently deleted — flag it `⚠ tidak ada lagi di PRD, cek manual sebelum dihapus` so completed work isn't lost by a resequencing mistake.

Write to `./TASKS.md` (or the path the user gave), grouped by phase, **all** of a feature's tasks first, then **one** test-case block for that feature right after — never one test-case block per task:

```markdown
## FASE 1 — MVP

### T1.1.1 — Implement form input undangan (FE)
- [ ] Field nama pengantin, tanggal, lokasi tervalidasi
- [ ] Data tersimpan otomatis; isi tidak hilang saat refresh
Estimate: 3 SP · Depends on: —

**Test Cases — Editor Undangan**
- [ ] Happy path: isi semua field valid → data tersimpan, tampil di preview
- [ ] Edge case: nama pengantin kosong → submit diblokir
- [ ] Edge case: foto tepat di batas 5 MB → diterima
- [ ] Error handling: foto > 5 MB → ditolak dengan pesan jelas (sesuai PRD)
```

A feature big enough to need multiple tasks still gets **one** test-case block, placed after the last of its tasks — the checklist covers the feature end-to-end, not each task in isolation:

```markdown
### T1.2.1 — Buat skema data tamu (BE)
- [ ] Tabel tamu: nama, status RSVP, nomor WA
Estimate: 2 SP · Depends on: —

### T1.2.2 — Endpoint tambah/edit tamu (BE)
- [ ] CRUD tamu tervalidasi
Estimate: 3 SP · Depends on: T1.2.1

### T1.2.3 — UI daftar & form tamu (FE)
- [ ] Tambah, edit, hapus tamu dari UI
- [ ] List ter-update tanpa reload
Estimate: 3 SP · Depends on: T1.2.2

**Test Cases — Kelola Tamu**
- [ ] Happy path: tambah tamu baru → muncul di list, tersimpan di DB
- [ ] Edge case: nomor WA duplikat → ditolak atau ditandai duplikat (sesuai PRD)
- [ ] Edge case: hapus tamu yang sudah di-invite → list & status ikut update
- [ ] Error handling: endpoint gagal saat submit → UI tampilkan error, data form tidak hilang
```

Close with a summary in ≤6 lines: file path, task count per phase, test-case count per phase (if generated), any `⚠ butuh acceptance criteria` / `(perlu konfirmasi perilaku)` / `⚠ tidak ada lagi di PRD` flags and how many, how many `[x]` were carried forward from an existing TASKS.md, and the critical-path dependency chain if one stands out.

## Handoff

- If the PRD itself has vague/missing acceptance criteria on features the user wants broken down now, say so and suggest running `prd-refine` first — don't patch it silently here.
- If no PRD exists yet, point to the `prd` skill instead of starting from a raw idea.
- Once the backlog is written, building the UI is the natural next step — mention `uiux-guide` for applying UI/UX rules while building/reviewing, or for producing a standalone interaction & behavior standards doc from the same PRD — don't run it unasked.
