# ryakarsa

Plugin skill untuk ZCode, Claude Code, **dan** Codex CLI — delapan skill dalam dua alur yang saling menyambung:

**Alur PRD**

| Skill | Fungsi |
|---|---|
| [`prd`](#1-prd--buat-prd-dari-ide-mentah) | ide mentah → PRD siap bangun |
| [`prd-refine`](#2-prd-refine--rapikan-prd-yang-sudah-ada) | PRD lama yang berantakan → rapi & buildable |
| [`prd-to-tasks`](#3-prd-to-tasks--pecah-prd-jadi-backlog-task--checklist-test-case) | PRD yang sudah disetujui → backlog task + checklist test case siap dikerjakan |

**Alur design**

| Skill | Fungsi |
|---|---|
| [`uiux-guide`](#4-uiux-guide--desain-review--standar-antarmuka) | terapkan teori UI/UX saat mendesain, mereview, atau menyusun standar interaksi |
| [`design-brief`](#5-design-brief--prd-jadi-identitas-visual) | PRD → identitas visual (warna, tipografi, layout) lewat wawancara kebutuhan UI |
| [`design-tokens`](#6-design-tokens--library-design-system) | library design system pribadi, dipakai ulang lintas project |
| [`component-library`](#7-component-library--library-komponen-ui) | library komponen UI (HTML/CSS/JS generik, portable ke stack apa pun) |
| [`animation-library`](#8-animation-library--library-animasi) | library animasi CSS/JS pribadi |

Butuh marketing & branding (brand kit, konten per platform, desain post sosmed)? Itu ada di pack saudaranya: [`ryakarsa-market`](https://github.com/revianto/ryakarsa-market).

Repo ini membawa manifest untuk tiap klien, plus satu cermin untuk Codex, jadi satu sumber untuk semua:

```text
ryakarsa/
├── .zcode-plugin/
│   └── plugin.json          # manifest untuk ZCode
├── .claude-plugin/
│   └── plugin.json          # manifest untuk Claude Code
├── .codex/
│   └── skills/               # cermin persis dari skills/ — auto-discovery Codex CLI, tanpa manifest
│       └── ...               # (kedelapan skill)
├── scripts/
│   └── sync-and-push.sh     # sinkron ~/.agents/skills → skills/ → .codex/skills/, commit & push
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
    ├── uiux-guide/
    │   ├── SKILL.md
    │   └── references/
    │       └── panduan-lengkap.md
    ├── design-brief/SKILL.md
    ├── design-tokens/                # + scripts/manage_library.py
    ├── component-library/            # + scripts/manage_library.py
    └── animation-library/            # + scripts/ & references/
```

Folder `library/` di tiap skill library (isi design system, komponen, dan animasi yang kamu simpan) adalah data pribadi dan **tidak ikut repo** — yang dibagikan cuma definisi skill-nya.

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
cp -R skills/* ~/.claude/skills/
```

## Pasang di Codex CLI

Codex CLI membaca skill dalam format `SKILL.md` yang sama (standar terbuka [agentskills.io](https://agentskills.io), tanpa manifest terpisah) — cukup taruh di lokasi yang di-scan otomatis saat startup:

- **Per-project** (skill aktif hanya di repo ini): clone repo ini, lalu jalankan Codex dari dalamnya — direktori `.codex/skills/` di repo sudah berisi salinan semua skill, langsung terbaca.
- **Semua project** (skill aktif di mana pun Codex dijalankan):
  ```bash
  cp -R skills/* ~/.codex/skills/
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

Untuk produk yang dilihat publik/berbayar, interview juga menanyakan **positioning & brand tone** (mass-market/mid/premium, kesan brand, pembanding) — masuk ke section khusus di PRD, dan dipakai `design-brief` untuk menentukan tingkat ornamen UI.

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

### 3. `prd-to-tasks` — pecah PRD jadi backlog task + checklist test case

**Kapan dipakai:** PRD sudah final/disetujui, saatnya diterjemahkan jadi task konkret yang bisa langsung dikerjakan (manusia atau AI) — sekaligus checklist QA supaya "PRD selesai" tidak berarti "siap ship tanpa dites".

**Cara pakai:** bilang *"buat task dari PRD ini"*, *"breakdown fitur jadi task"*, *"pecah PRD jadi backlog"*, *"generate tickets from this PRD"*, atau *"buatkan test case/checklist QA dari PRD ini"*.

**Alur:**
1. **Scope** — pilih fase yang mau dipecah (Fase 1 saja atau semua), unit estimasi (SP/jam/T-shirt size), solo atau tim (menentukan label role per task), dan apakah checklist test case ikut dibuat (default ya).
2. **Decompose** — tiap fitur dipecah jadi 1–5 task menurut seam alami (data model, backend, UI, integrasi, testing); acceptance criteria disalin persis dari PRD, bukan ditulis ulang.
3. **Test case** — tiap fitur dengan acceptance criteria dapat checklist happy path, edge case, dan error handling; kasus yang perilakunya tidak dijelaskan PRD ditandai "(perlu konfirmasi perilaku)", bukan dikarang.
4. **Sequence** — task diurutkan sesuai dependency; dependency lintas fitur disebut eksplisit.
5. **TASKS.md** — backlog per fase, tiap task punya ID, judul, acceptance criteria (checkbox), estimasi, dependency, diikuti checklist test case fitur tersebut.

Fitur yang di PRD-nya tidak punya acceptance criteria **tidak** diberi kriteria atau test case karangan — task-nya tetap dibuat tapi ditandai `⚠ butuh acceptance criteria`, lalu diarahkan balik ke `prd-refine`.

**Urutan pengerjaan:** default mengikuti dependency (data → backend → UI). Bisa diminta **frontend dulu** (UI dibangun dengan data dummy, lalu backend, lalu task penyambung ke API asli).

**Guard sinkronisasi:** setelah `TASKS.md` ditulis, skill menambahkan aturan sinkron PRD ↔ TASKS ke `CLAUDE.md` project (kalau file itu ada dan belum punya aturan serupa) — supaya perubahan fitur di tengah development selalu lewat PRD dulu, bukan edit TASKS.md manual.

**Dijalankan ulang di atas TASKS.md yang sudah ada** (mis. setelah PRD di-update): skill ini **merge**, bukan timpa — item `[x]` yang sudah dicentang dipertahankan selama ID & isinya belum berubah, task yang isinya berubah dianggap reset, dan task lama yang sudah tidak ada di PRD ditandai `⚠ tidak ada lagi di PRD` alih-alih dihapus diam-diam.

### 4. `uiux-guide` — desain, review & standar antarmuka

**Kapan dipakai:** membuat halaman/screen/komponen apa pun, mengkritik & memperbaiki UI yang sudah ada (Flutter, Next.js, React, native), atau menyusun dokumen standar interaksi untuk tim design.

**Cara pakai:** bilang *"buatkan halaman X"*, *"desain screen Y"*, *"review UI ini, kenapa rasanya berantakan?"*, atau *"dari PRD.md buat interaction & behavior standar untuk panduan tim design"* — teori diterapkan otomatis, tanpa perlu menyebut "UI/UX".

**Tiga mode:**
1. **Mode desain** — aturan diterapkan saat membangun: design tokens, grid 8-point, proporsi warna 60-30-10, kontras WCAG AA (4.5:1), tap target ≥44px, thumb zone, pola baca Z/F, motion 200–300ms.
2. **Mode review** — audit terhadap angka-angka kunci + checklist ship: temuan per aturan dengan perbaikan konkret ("padding 10px → 16px agar masuk grid 8-point") dan severity (aksesibilitas = blocking, proporsi/motion = polish).
3. **Mode standards** — hasilkan dokumen `UI-STANDARDS.md`: aturan interaksi & perilaku (states, form UX, motion, aksesibilitas, responsive, microcopy) yang di-scope dari PRD, **tanpa** palet warna, font family, atau layout per halaman — itu ranah design brief, bukan behavior standard.

Kalau ada success metric dari PRD yang jadi acuan (mis. conversion checkout), skill ini juga memastikan aksi penentunya (klik CTA, submit form, tiap step funnel) punya titik instrumentasi yang jelas — bukan mendefinisikan metriknya (itu tugas `prd`), hanya memastikan UI-nya bisa diukur.

Di produk yang **sudah jalan**, mode desain lebih dulu memindai pola interaksi yang sudah dipakai (skeleton vs spinner, toast vs banner, modal vs drawer) dan mengikutinya — bukan memperkenalkan pola baru yang tidak konsisten. Nilai token dicari berurutan: token di codebase → design system tersimpan di `design-tokens` → baru diasumsikan. Ada juga aturan **memilih komponen input** (kapan radio, dropdown, combobox, checkbox, toggle, segmented control).

Referensi teori lengkap (Gestalt, Nielsen, hukum kognitif, thumb zone, pemilihan komponen input): `skills/uiux-guide/references/panduan-lengkap.md`.

### 5. `design-brief` — PRD jadi identitas visual

**Kapan dipakai:** PRD sudah ada, perlu menentukan arah visual (warna, tipografi, layout) yang berakar dari tujuan bisnis — bukan template generik.

**Cara pakai:** bilang *"buat design brief dari PRD ini"*, *"tentukan filosofi warna/font dari PRD"*, *"cari referensi UI yang cocok"*.

**Alur:**
1. **Cek yang sudah ada** — token di kode (mode *extract*: dokumentasikan, bukan ganti) dan aset brand resmi (logo, guideline) sebagai batasan keras.
2. **Wawancara kebutuhan UI** — prioritas produk (estetika/layanan/utility), blok konten (CTA, carousel, dll), **tingkat ornamen** (polos → kaya/eksklusif), level animasi, referensi visual, dan target dark mode.
3. **Filosofi → per area UI → riset referensi → slop check** — termasuk *surface treatment* komponen (solid/outline/shine). Referensi UI dari kamu **dinilai** (cocok penuh / sebagian / tidak cocok, dengan alasan), bukan diterima mentah-mentah.
4. **Otomatis setelahnya** — starter kit (3 komponen + 2 animasi) dan pendaftaran design system ke `design-tokens`.

### 6. `design-tokens` — library design system

**Kapan dipakai:** menyimpan design system (warna, tipografi, spacing, radius, shadow, motion) supaya bisa dipakai ulang di project berikutnya tanpa menebak ulang.

**Cara pakai:** *"simpan design system dari project ini"*, *"design system apa aja yang tersimpan"*, lalu di project lain *"buatkan halaman X pakai design system 'nama'"*.

Satu entri = satu design system utuh (semua kategori token dalam satu `tokens.json`). Bisa diekstrak dari kode/design doc yang sudah ada, dari screenshot, atau dari deskripsi. Kalau kamu punya artifact viewer-nya, tiap perubahan library ikut dipublish ulang.

### 7. `component-library` — library komponen UI

**Kapan dipakai:** menyimpan komponen (button, card, navbar, form, dll) sebagai HTML/CSS/JS generik yang bisa diterjemahkan ke React, Flutter, Vue, dst.

**Cara pakai:** *"bikinkan pricing card minimalis dan simpan"*, *"simpan komponen ini"*, *"pasang card pricing yang tersimpan ke project ini"*. Warna & font diambil dari design system tersimpan kalau ada, bukan dikarang.

### 8. `animation-library` — library animasi

**Kapan dipakai:** menyimpan dan menerapkan animasi (entrance, hover, loading, scroll-reveal) ke elemen/project.

**Cara pakai:** *"tambahin animasi fade in pelan ke card ini"*, *"lihat animasi apa aja yang ada"*. Durasi & easing mengikuti design system dan level animasi dari design brief kalau ada.

## Maintenance

Skill dikembangkan di `~/.agents/skills/` (sumber kebenaran), lalu disinkronkan ke repo ini:

```bash
./scripts/sync-and-push.sh
```

Script melakukan rsync semua skill di array `SKILLS` ke `skills/` (tanpa folder `library/`), memvalidasi frontmatter, mencerminkan `skills/` ke `.codex/skills/`, lalu commit & push jika ada perubahan. Menambah skill baru: daftarkan di array `SKILLS` dan bump versi di kedua manifest (`.claude-plugin/` & `.zcode-plugin/`).
