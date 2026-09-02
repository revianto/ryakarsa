---
name: prd-refine
description: Audit and clean up an existing PRD (Product Requirement Document) — fix structure, vague requirements, contradictions, and missing acceptance criteria without changing the product's intent. Use when the user gives an existing PRD, spec, or requirements doc to tidy, restructure, review, or polish — phrasings like "rapikan PRD", "PRD-nya berantakan tolong dirapikan", "bersihkan/rapikan PRD ini", "review and fix this PRD", "restructure this spec", "make this PRD buildable" — or hands over an existing PRD.md and wants it better. For creating a new PRD from a raw idea, use the prd skill instead.
---

# PRD Refiner

Take an existing PRD and return a tidied, buildable version — **without changing what the product is**. The author's intent is law: you reorganize and sharpen; you never re-decide the product.

Language: match the user's language and the document's own language.

## Step 1 — Read and audit

Read the PRD the user points at (file path, pasted text, or link). If none was given, ask for it first — nothing else.

**Multiple documents:** if the user hands over more than one related document (e.g. a PRD plus a separate tech spec, or two draft PRDs to merge), read all of them before auditing. Treat any conflict between documents as a Consistency finding in Step 2 — same as an internal contradiction — and merge into a single refined PRD rather than producing one output per input file.

**Existing backup:** if a `<name>_old.md` (or the highest-numbered `<name>_oldN.md`) sits next to the input in the same folder, read it as the previous version. Note in the final change summary what changed since that version, not just since the audit — this makes iteration-over-iteration drift visible instead of only the latest pass.

Audit against this checklist and collect **concrete findings** with short quotes or references to the original text:

**Structure**
- Missing or buried sections: problem, goals/non-goals, target users, requirements, success metrics, open questions
- Same topic scattered in several places; requirements mixed into background story
- No phasing or priority — everything reads as equally urgent

**Clarity**
- Vague words with no number attached: "cepat", "user-friendly", "scalable", "lengkap"
- Must-have features without testable acceptance criteria
- Unprioritized feature lists, or everything marked high priority

**Consistency**
- Contradictions: two different scopes, conflicting metrics, a goal with no matching requirement (or vice versa)
- Tech stack named but ignored by the requirements
- Assumptions stated as facts

Do not fix anything yet.

## Step 2 — Report findings, ask only what's needed

Present the findings in three buckets:

1. **Aman dirapikan** — structure, grouping, ordering, formatting, moving content to the right section. You will just do these.
2. **Perlu keputusan user** — each contradiction or real gap becomes ONE short question with options inferred from the document itself, plus "Lainnya" (free text). Ask via the **AskUserQuestion tool** when it is available in the current client — pop-up with clickable options, same as the `prd` skill; otherwise fall back to a numbered text list. Skipping is fine. **Max 5 questions**; if there are more, ask the 5 that change the document most and push the rest to Open Questions.
3. **Akan ditandai "(asumsi)"** — things you will resolve yourself, but visibly.

Wait for the user's answers before rewriting.

## Step 3 — Rewrite

Apply the fixes:

- Normalize section order toward a standard PRD skeleton, keeping every section the original actually needs: problem → goals/non-goals → target users → requirements by priority/phase (with acceptance criteria) → non-functional → success metrics → release plan → risks → open questions. Don't pad missing sections with invented content.
- Vague → concrete wherever the document itself supports it; otherwise write the best reading and mark it "(perlu konfirmasi)".
- Never delete content silently: scope-like removals move to *Non-goals* with the original wording; anything else dropped appears in the change summary with a reason.
- Keep the original document's voice and terminology (feature names especially) — people and other docs reference them.

**Output file:** keep the updated PRD at the original path. Before writing, back up the current file — **rotate, never clobber**: if `<original>_old.md` doesn't exist yet, this is the first refine pass, so rename the current file to `<original>_old.md`. If `<original>_old.md` already exists, this isn't the first pass — moving straight to `_old.md` would destroy the very-first version it holds. Instead find the highest existing `<original>_oldN.md` and back up the current file one number past it (`_old.md` → next is `_old2.md`, then `_old3.md`, and so on), so every prior pass stays recoverable. Then write the refined version to the original path.

Close with a change summary of ≤8 lines: what moved where, what was sharpened, what is now marked asumsi/perlu konfirmasi, and how many open questions remain.

## Handoff

- If the input turns out not to be a PRD at all — just a raw idea or scattered notes — stop and say so: the `prd` skill (interview → plan → PRD.md) is the right tool for creating one from scratch.
- Once the refined PRD is written and any open questions are resolved, mention `prd-to-tasks` as the next step for turning it into an execution backlog + QA checklist — don't run it unasked.
