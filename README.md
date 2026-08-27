# ryakarsa

Plugin **PRD** untuk ZCode **dan Claude Code** — dua skill yang saling melengkapi:

- **`prd`** — mengubah ide produk mentah menjadi PRD siap bangun dalam tiga tahap:
  1. **Interview** — 5–8 pertanyaan cerdas. Di ZCode lewat pop-up interaktif (tinggal klik); di klien lain otomatis fallback ke daftar bernomor.
  2. **Plan** — blueprint fitur per fase yang bisa diedit & direview sebelum menulis PRD.
  3. **PRD.md** — dokumen final dengan acceptance criteria, metrik, risiko, dan pertanyaan terbuka.
- **`prd-refine`** — merapikan PRD yang **sudah ada** tanpa mengubah maksud penulisnya:
  1. **Audit** — temukan masalah konkret: struktur berantakan, kata tidak terukur ("cepat", "user-friendly"), fitur tanpa acceptance criteria, kontradiksi.
  2. **Temuan + pertanyaan minimal** — maksimal 5 pertanyaan hanya untuk hal yang ambigu; sisanya langsung dirapikan.
  3. **Tulis ulang** — PRD lama di-rename jadi **`PRD_old.md`** (backup), dan versi yang sudah dirapikan menempati **`PRD.md`**.

Repo ini membawa dua manifest sekaligus, jadi satu sumber untuk semua klien:

```text
ryakarsa/
├── .zcode-plugin/
│   └── plugin.json          # manifest untuk ZCode
├── .claude-plugin/
│   └── plugin.json          # manifest untuk Claude Code
└── skills/
    ├── prd/
    │   ├── SKILL.md
    │   └── references/
    │       ├── question-bank.md
    │       └── prd-template.md
    └── prd-refine/
        └── SKILL.md
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
cp -R skills/prd skills/prd-refine ~/.claude/skills/
```

## DeepSeek

DeepSeek tidak punya format marketplace plugin sendiri, tapi bisa dipakai lewat dua jalan:

- **Model DeepSeek di dalam Claude Code** — DeepSeek menyediakan endpoint kompatibel Anthropic. Setel `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic` (dan API key DeepSeek) di Claude Code, lalu pasang plugin seperti di atas. Plugin jalan apa pun modelnya, karena marketplace dikelola oleh klien, bukan model.
- **Model DeepSeek di dalam ZCode** — plugin ryakarsa terpasang seperti biasa; cukup pilih model DeepSeek di pengaturan ZCode.

## Cara pakai

**Buat PRD baru** — ketik `/prd` atau cukup bilang "buat PRD untuk aplikasi X". Jika klien tidak menyediakan pop-up pertanyaan, skill otomatis memakai daftar bernomor dan kamu jawab dengan angka (mis. `3: a,c,f`).

**Rapikan PRD yang sudah ada** — bilang "rapikan PRD ini: /path/ke/PRD.md". Skill akan menampilkan temuan audit dulu, menanyakan maksimal 5 hal yang ambigu, lalu menulis hasilnya ke `PRD.md` (versi lama tersimpan otomatis sebagai `PRD_old.md`).
