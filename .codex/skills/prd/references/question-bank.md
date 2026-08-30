# Question bank

Pick 5–8 questions per project from the core set; add type-specific ones only when they fill a real gap. Every option must be inferred from the user's idea — never a generic list.

## Core questions

1. **Target user & current workaround** (open text) — validates the problem.
   "Ceritakan orang yang paling butuh ini. Sekarang mereka ngatasin masalahnya gimana?"
2. **First-run core job** (single choice) — anchors MVP scope.
   "Saat pertama kali buka, hal apa yang paling penting mereka selesaikan?"
3. **Must-have features** (multi-select, max 3) — options are candidate features you inferred from the idea.
   "Pilih 3 fitur yang wajib ada di rilis pertama."
4. **Differentiator** (single or multi) —
   "Apa keunggulan utama dibanding cara mereka sekarang?" e.g. lebih cepat / lebih murah / lebih gampang / lebih aman.
5. **Retention hook** (multi) —
   "Apa yang bikin mereka balik lagi, bukan cuma sekali?" options like konten baru, edit/update, notifikasi, progres tersimpan — inferred, not copied.
6. **Success signal** (single choice or open) —
   "3 bulan setelah rilis, gimana kamu tahu ini berhasil?" options: jumlah X dibuat, dibagikan ke N orang, rating, revenue.
7. **Constraints** (multi or open) — platform (web / Android / iOS / WhatsApp), deadline, siapa yang bangun (solo / tim / AI), budget hosting, integrasi wajib (payment, WhatsApp, Maps).
8. **Tech stack** — "Udah punya pilihan tech stack, atau mau AI yang tentuin?"
   a. Biarkan AI pilih (AI rekomendasikan yang paling cocok)
   b. Pilih sendiri → then per layer: Frontend (UI & tampilan user), Backend (logika & API server), Database (penyimpanan data), Deployment (hosting & infra).

## Type-specific extras

**Feature on existing product**
- Behavior today & who asked for this feature (user request? support tickets? metrics?)
- Success metric for this specific feature
- Rollout: semua user sekaligus / bertahap / di-balik feature flag
- Compatibility constraints with existing data or flows

**Internal tool**
- Current manual process: steps + time cost per week
- Who uses it (role, count) & who must NOT have access
- Where the data lives today
- Priority tradeoff: speed of build vs polish

**Integration / API**
- Systems on both sides + auth methods
- Data shape & volume, sync frequency
- Failure handling: retry, queue, alerting
- Rate limits & cost per call

## Anti-patterns

- Re-asking anything the user already said in the conversation.
- More than 8 questions + 3 follow-ups total — fatigue wrecks answer quality.
- Generic option lists that would fit any product.
- Open text where a choice would do; choices where open text is needed (problem discovery needs free text).
- Tech-stack questions for non-software projects.
