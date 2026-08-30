# ryakarsa

Plugin skill untuk ZCode **dan** Claude Code — empat skill yang saling melengkapi:

| Skill | Fungsi |
|---|---|
| [`prd`](#1-prd--buat-prd-dari-ide-mentah) | ide mentah → PRD siap bangun |
| [`prd-refine`](#2-prd-refine--rapikan-prd-yang-sudah-ada) | PRD lama yang berantakan → rapi & buildable |
| [`prd-to-tasks`](#3-prd-to-tasks--pecah-prd-jadi-backlog-task) | PRD yang sudah disetujui → backlog task siap dikerjakan |
| [`uiux-guide`](#4-uiux-guide--desain--review-antarmuka) | terapkan teori UI/UX saat mendesain atau mereview antarmuka |

Repo ini membawa dua manifest sekaligus, jadi satu sumber untuk semua klien:

```text
ryakarsa/
├── .zcode-plugin/
│   └── plugin.json          # manifest untuk ZCode
├── .claude-plugin/
│   └── plugin.json          # manifest untuk Claude Code
├── scripts/
│   └── sync-and-push.sh     # sinkron ~/.agents/skills → repo, commit & push
└── skills/
    ├── prd/
    │   ├── SKILL.md
    │   └── references/
    │       ├── question-bank.md
    │       └── prd-template.md
    ├── prd-refine/
    │   └── SKILL.md
    ├── prd-to-tasks/
    │   └── SKILL.md
    └── uiux-guide/
        ├── SKILL.md
        └── references/
            └── panduan-lengkap.md
```

## Pasang di ZCode

1. **Settings → Plugin Management → Discover** → tombol **`+`** → **GitHub repository**.
2. Tempel: `https://github.com/revianto/ryakarsa` → **Add**.
3. Klik plugin **ryakarsa** → **Install** → **Enable**.

## Pasang di Claude Code

Di dalam Claude Code:

```
/plugin marketplace add https://github.com/revianto/ryakarsa
/plugin install ryakarsa@revianto/ryakarsa
```

Atau tanpa plugin: salin folder skill ke `~/.claude/skills/`:

```bash
cp -R skills/prd skills/prd-refine skills/prd-to-tasks skills/uiux-guide ~/.claude/skills/
```

## DeepSeek

DeepSeek tidak punya format marketplace plugin sendiri, tapi bisa dipakai lewat dua jalan:

- **Model DeepSeek di dalam Claude Code** — DeepSeek menyediakan endpoint kompatibel Anthropic. Setel `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic` (dan API key DeepSeek) di Claude Code, lalu pasang plugin seperti di atas. Plugin jalan apa pun modelnya, karena marketplace dikelola oleh klien, bukan model.
- **Model DeepSeek di dalam ZCode** — plugin ryakarsa terpasang seperti biasa; cukup pilih model DeepSeek di pengaturan ZCode.

---

## Cara pakai

### 1. `prd` — buat PRD dari ide mentah

**Kapan dipakai:** mau merencanakan produk/fitur baru sebelum dibangun.

**Cara pakai:** ketik `/prd` atau cukup bilang *"buat PRD untuk aplikasi X"*, *"bikin PRD-nya"* — bahkan tanpa kata "PRD" asalkan terlihat ingin perencanaan terstruktur.

**Alur (3 tahap, tidak bisa dilompati kecuali diminta):**
1. **Interview** — 5–8 pertanyaan cerdas lewat pop-up interaktif (tinggal klik); di klien tanpa pop-up otomatis jadi daftar bernomor, jawab dengan angka (mis. `3: a,c,f`).
2. **Plan** — blueprint fitur per fase yang bisa diedit & direview sebelum PRD ditulis.
3. **PRD.md** — dokumen final: acceptance criteria, metrik, risiko, pertanyaan terbuka.

Tebakan yang harus diambil model selalu ditandai "(asumsi)" atau masuk *Open Questions* — tidak ada keputusan produk yang direkayasa diam-diam.

Kalau sudah ada data existing (analytics, hasil wawancara user, riset kompetitor), lampirkan saja — skill langsung memakainya sebagai jawaban dan mengutipnya di plan/PRD, bukan menanyakan ulang hal yang sudah terjawab dari data tersebut.

### 2. `prd-refine` — rapikan PRD yang sudah ada

**Kapan dipakai:** punya PRD/spesifikasi lama yang berantakan, kabur, atau kontradiktif.

**Cara pakai:** bilang *"rapikan PRD ini: /path/ke/PRD.md"*, *"review and fix this PRD"*, *"make this PRD buildable"*.

**Alur:**
1. **Audit** — temuan konkret: struktur berantakan, kata tidak terukur ("cepat", "user-friendly"), fitur tanpa acceptance criteria, kontradiksi.
2. **Pertanyaan minimal** — maksimal 5 pertanyaan hanya untuk hal yang ambigu; sisanya langsung dirapikan.
3. **Tulis ulang** — versi lama otomatis di-backup sebagai `PRD_old.md`, versi rapi menempati `PRD.md` asli.

Maksud penulis tidak pernah diubah: skill hanya menata dan mempertajam.

Mendukung lebih dari satu dokumen sekaligus (mis. PRD + tech spec terpisah, atau dua draft yang perlu digabung) — konflik antar dokumen jadi temuan Consistency, bukan diselesaikan diam-diam. Kalau ada backup versi sebelumnya (`PRD_old.md`) di folder yang sama, ringkasan perubahan juga membandingkan terhadap versi itu, bukan cuma terhadap draft saat ini.

### 3. `prd-to-tasks` — pecah PRD jadi backlog task

**Kapan dipakai:** PRD sudah final/disetujui, saatnya diterjemahkan jadi task konkret yang bisa langsung dikerjakan (manusia atau AI).

**Cara pakai:** bilang *"buat task dari PRD ini"*, *"breakdown fitur jadi task"*, *"pecah PRD jadi backlog"*, *"generate tickets from this PRD"*.

**Alur:**
1. **Scope** — pilih fase yang mau dipecah (Fase 1 saja atau semua), unit estimasi (SP/jam/T-shirt size), solo atau tim (menentukan label role per task).
2. **Decompose** — tiap fitur dipecah jadi 1–5 task menurut seam alami (data model, backend, UI, integrasi, testing); acceptance criteria disalin persis dari PRD, bukan ditulis ulang.
3. **Sequence** — task diurutkan sesuai dependency; dependency lintas fitur disebut eksplisit.
4. **TASKS.md** — backlog per fase, tiap task punya ID, judul, acceptance criteria (checkbox), estimasi, dependency.

Fitur yang di PRD-nya tidak punya acceptance criteria **tidak** diberi kriteria karangan — task-nya tetap dibuat tapi ditandai `⚠ butuh acceptance criteria`, lalu diarahkan balik ke `prd-refine`.

### 4. `uiux-guide` — desain & review antarmuka

**Kapan dipakai:** membuat halaman/screen/komponen apa pun, atau mengkritik & memperbaiki UI yang sudah ada (Flutter, Next.js, React, native).

**Cara pakai:** bilang *"buatkan halaman X"*, *"desain screen Y"*, atau *"review UI ini, kenapa rasanya berantakan?"* — teori diterapkan otomatis, tanpa perlu menyebut "UI/UX".

**Dua mode:**
1. **Mode desain** — aturan diterapkan saat membangun: design tokens, grid 8-point, proporsi warna 60-30-10, kontras WCAG AA (4.5:1), tap target ≥44px, thumb zone, pola baca Z/F, motion 200–300ms.
2. **Mode review** — audit terhadap angka-angka kunci + checklist ship: temuan per aturan dengan perbaikan konkret ("padding 10px → 16px agar masuk grid 8-point") dan severity (aksesibilitas = blocking, proporsi/motion = polish).

Kalau ada success metric dari PRD yang jadi acuan (mis. conversion checkout), skill ini juga memastikan aksi penentunya (klik CTA, submit form, tiap step funnel) punya titik instrumentasi yang jelas — bukan mendefinisikan metriknya (itu tugas `prd`), hanya memastikan UI-nya bisa diukur.

Referensi teori lengkap (Gestalt, Nielsen, hukum kognitif, thumb zone): `skills/uiux-guide/references/panduan-lengkap.md`.

## Maintenance

Skill dikembangkan di `~/.agents/skills/` (sumber kebenaran), lalu disinkronkan ke repo ini:

```bash
./scripts/sync-and-push.sh
```

Script melakukan rsync ketiga skill ke `skills/`, memvalidasi frontmatter, lalu commit & push jika ada perubahan.
