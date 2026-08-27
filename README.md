# ryakarsa

Plugin **PRD Writer** untuk ZCode **dan Claude Code** — mengubah ide produk mentah menjadi PRD siap bangun dalam tiga tahap:

1. **Interview** — 5–8 pertanyaan cerdas. Di ZCode lewat pop-up interaktif (tinggal klik); di klien lain otomatis fallback ke daftar bernomor.
2. **Plan** — blueprint fitur per fase yang bisa diedit & direview sebelum menulis PRD.
3. **PRD.md** — dokumen final dengan acceptance criteria, metrik, risiko, dan pertanyaan terbuka.

Repo ini membawa dua manifest sekaligus, jadi satu sumber untuk semua klien:

```text
ryakarsa/
├── .zcode-plugin/
│   └── plugin.json          # manifest untuk ZCode
├── .claude-plugin/
│   └── plugin.json          # manifest untuk Claude Code
└── skills/
    └── prd/
        ├── SKILL.md
        └── references/
            ├── question-bank.md
            └── prd-template.md
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
cp -R skills/prd ~/.claude/skills/prd
```

## DeepSeek

DeepSeek tidak punya format marketplace plugin sendiri, tapi bisa dipakai lewat dua jalan:

- **Model DeepSeek di dalam Claude Code** — DeepSeek menyediakan endpoint kompatibel Anthropic. Setel `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic` (dan API key DeepSeek) di Claude Code, lalu pasang plugin seperti di atas. Plugin jalan apa pun modelnya, karena marketplace dikelola oleh klien, bukan model.
- **Model DeepSeek di dalam ZCode** — plugin ryakarsa terpasang seperti biasa; cukup pilih model DeepSeek di pengaturan ZCode.

## Cara pakai

Di percakapan, ketik `/prd` atau cukup bilang "buat PRD untuk aplikasi X". Jika klien tidak menyediakan pop-up pertanyaan, skill otomatis memakai daftar bernomor dan kamu jawab dengan angka (mis. `3: a,c,f`).
