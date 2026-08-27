# ryakarsa

Plugin ZCode berisi skill **PRD Writer** — mengubah ide produk mentah menjadi PRD siap bangun dalam tiga tahap:

1. **Interview** — 5–8 pertanyaan cerdas via pop-up interaktif (AskUserQuestion), jawab cukup dengan klik.
2. **Plan** — blueprint fitur per fase yang bisa diedit & direview sebelum menulis PRD.
3. **PRD.md** — dokumen final dengan acceptance criteria, metrik, risiko, dan pertanyaan terbuka.

## Cara pasang

1. **Settings → Plugin Management → Discover** → tombol **`+`** → pilih **GitHub repository**.
2. Tempel: `https://github.com/revianto/ryakarsa` → **Add**.
3. Klik plugin **ryakarsa** → **Install** → **Enable**.

## Cara pakai

Di percakapan ZCode, ketik:

```
/prd
```

lalu ikuti pertanyaan yang muncul. Atau sebut langsung: "buat PRD untuk aplikasi X".

## Struktur

```text
ryakarsa/
├── .zcode-plugin/
│   └── plugin.json          # manifest plugin
└── skills/
    └── prd/
        ├── SKILL.md
        └── references/
            ├── question-bank.md
            └── prd-template.md
```
