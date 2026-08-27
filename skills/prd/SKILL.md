---
name: prd
description: Turn a raw product idea into a mature PRD (Product Requirement Document) in three stages — a short interview (5–8 smart questions with pickable options), an editable feature/phase plan, then the final PRD.md. Use whenever the user wants to create, draft, plan, or improve a PRD, product requirements doc, product spec, or feature brief — including casual phrasings like "buat PRD", "bikin PRD", "tolong buatkan PRD-nya", "write a spec for this", "plan this app before we build it" — even when the word "PRD" is not said but structured product planning before development is clearly wanted.
---

# PRD Writer

Turn a raw product idea into a PRD a dev team (human or AI) can build from, in three stages:

1. **Interview** — 5–8 smart questions via an interactive pop-up questionnaire (AskUserQuestion), each with clickable options so the user can answer in seconds.
2. **Plan** — an editable feature blueprint grouped into phases; the user reviews and edits it.
3. **PRD.md** — the final document, written only after the plan is approved.

Never skip a stage unless the user explicitly asks to ("langsung aja", "skip pertanyaannya"). If they do, jump ahead but mark every guess as "(asumsi)".

**Language rule:** run every stage — questions, plan, final PRD — in the user's language. If they write in Indonesian, everything is Indonesian.

**Golden rule:** never silently invent a product decision. An assumption is fine when it is visible: mark it "(asumsi)" or park it in *Open Questions*.

## Stage 1 — Interview

Mine the conversation first: idea, audience, stack, and constraints the user already gave are answered — never re-ask.

Classify the project to pick the question set (read `references/question-bank.md` before composing your batch):

- new app / product
- new feature on an existing product
- internal tool
- integration / API

Use the **AskUserQuestion tool** when available (ZCode) — questions appear as pop-ups with clickable options, so the user answers by tapping, never by typing question numbers. **If the tool is not available** (e.g., running inside Claude Code or another client without AskUserQuestion), fall back to a numbered text list in a single message and tell the user they can answer with numbers like "3: a,c,f". Tool constraints below shape the interview when AskUserQuestion is used:

- **Max 4 questions per pop-up** → split a 5–8 question interview into **2–3 waves** (e.g., wave 1 = questions 1–4, wave 2 = questions 5–8).
- **Max 4 options per question** → cap options at 4. If more candidates exist, keep the 4 strongest or split into a separate question. "Lainnya"/"Other" is added automatically by the tool — never add it manually.
- Options must be **inferred from the user's idea** and short (2–5 words) — like chips in a form. Generic lists that would fit any product are a smell; "Kirim undangan ke tamu" beats "Feature A".
- **Multi-select** for must-have features: set `multiSelect: true` and state the cap inside the question ("pilih maks 3") to force prioritization.
- **Open-text questions** (problem discovery) still work: give likely answers as options; the user can pick "Other" to type freely.
- **Skipping is fine**: nothing breaks if a question is skipped — whatever is unanswered becomes an Open Question later.

Wave shape (example, Indonesian — wave 1 of 2):

- Q1 (open, via "Other"): "Ceritakan orang yang paling butuh aplikasi ini — sekarang mereka ngatasi masalahnya gimana?"
- Q2 (single): "Saat pertama kali buka aplikasi, hal apa yang paling penting mereka selesaikan?" → "Buat undangan pertama" / "Lihat contoh undangan" / "Pilih desain"
- Q3 (multiSelect, maks 3): "Pilih 3 fitur yang wajib ada di rilis pertama:" → "Editor undangan" / "Atur tanggal acara" / "Kelola tamu" / "Kirim via WA"

After all waves, ask **at most 3 follow-ups**, and only for critical gaps: no target user, no scope boundary, or no success signal. Then stop asking — anything still unknown becomes an Open Question in the PRD.

Tech stack: ask via pop-up (or text list if the tool is unavailable) — "Udah punya pilihan tech stack, atau mau AI yang tentuin?" → "Biarkan AI pilih" / "Pilih sendiri". If "pilih sendiri", collect per layer (frontend, backend, database, deployment) as one wave of up to 4 questions, each with concrete options plus "Mau AI rekomendasikan". If "biarkan AI pilih", propose the stack yourself in Stage 2 with one-line reasons. Skip this entirely for non-software projects.

## Stage 2 — Editable plan

Before any PRD is written, present the blueprint for review:

1. **Summary** — 3 lines: problem → solution → for whom.
2. **Feature tree by phase** — a fenced code block that reads like a map. FASE 1 is the MVP; later phases hold everything the product can launch without.

```text
Undangan Digital
├─ FASE 1 — MVP
│  ├─ Editor Undangan
│  │   ├─ Isi nama pengantin
│  │   ├─ Atur tanggal acara
│  │   └─ Tambah foto
│  └─ URL Undangan
│      ├─ Buat link unik
│      └─ Salin & bagikan
├─ FASE 2
│  ├─ Kelola Tamu
│  │   ├─ Daftar tamu
│  │   ├─ Kirim undangan
│  │   └─ Pantau status kirim
│  └─ Kustomisasi Tema
└─ FASE 3
   ├─ RSVP & Analitik
   └─ Musik latar
```

3. **Tech stack per layer** (if software): frontend / backend / database / deployment, one-line reason each.
4. **Success metrics** — 2–4, measurable, with targets.
5. **Out of scope** — explicit list.

Close with an explicit review ask: "Review dulu — ada yang mau dihapus, ditambah, dipindah fase, atau diganti namanya?"

Apply every edit and re-render the tree. Only when the user approves ("oke", "gas", "lanjut") move on. **Writing PRD.md before approval is a bug.**

## Stage 3 — Write PRD.md

Read `references/prd-template.md` and fill **every** section from the interview + approved plan:

- Render headings in the user's language (the template shows an Indonesian example).
- No empty sections: unknown → best guess marked "(asumsi)", or moved to *Open Questions*.
- Every P0 feature gets testable acceptance criteria as checkboxes; P1/P2 features may have one-line criteria.
- Phases, priorities, and stack come verbatim from the approved plan — do not re-decide them here.

Write to `./PRD.md` in the working directory unless the user gave another path. Then confirm in ≤6 lines: file path, locked scope (phases + feature count), stack, top success metric, and how many open questions remain.
