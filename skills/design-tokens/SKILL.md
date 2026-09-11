---
name: design-tokens
description: 'Kelola library design system pribadi milik user (banyak design system, terus bertambah/berkurang), tiap design system berisi detail design token lengkap di dalamnya (color, typography, spacing, radius, shadow, breakpoint, motion, z-index) dalam format JSON generik yang portable ke stack apa pun. Bisa CRUD penuh — tambah, lihat/cari, update, hapus design system. Design system baru bisa dibuat dari desain yang sudah ada (screenshot/mockup/Figma export yang di-attach user), deskripsi teks/prompt ("bikinkan design system hangat untuk brand F&B"), atau nilai yang sudah ditentukan user (di-paste langsung). WAJIB gunakan skill ini setiap kali user menyebut "design system", "design token", "token warna/spacing/typography", "simpan design system ini", "tambahin ke library design system", "design system apa aja yang tersimpan", "update/ganti design system X", "hapus design system X", atau minta dibuatkan/diekstrak design system dari desain yang sudah ada, atau minta membuat sesuatu ("desain X", "buatkan halaman Y") dengan merujuk salah satu design system tersimpan (mis. `menggunakan design system "abc"`) — bahkan kalau user tidak menyebut kata "skill" atau "library" secara eksplisit. Skill ini portable: folder yang sama bisa dipasang di Claude.ai maupun Claude Code.'
---

# Design Tokens

Skill ini memberi Claude sebuah "lemari" berisi design system milik user sendiri, yang terus tumbuh (dan kadang menyusut) seiring waktu. Ini adalah pasangan dari `component-library` dan `animation-library`: kalau dua skill itu menyimpan *implementasi* (markup, CSS, animasi), skill ini menyimpan *keputusan desain mentah* di baliknya — warna, skala tipografi, grid spacing, radius, shadow, breakpoint, dan durasi/easing motion — supaya bisa dipakai ulang secara konsisten di project apa pun ke depannya, tanpa menebak ulang nilai-nilai itu dari nol setiap kali mulai project baru.

**Unit utamanya adalah satu design system utuh**, bukan token satuan lepas. Satu entri = satu design system (mis. "rebrew", "onyx-studio", "revianto-cv"), dan di dalamnya tersimpan semua kategori token miliknya sekaligus dalam satu file JSON nested. Ini yang membuatnya portable: dari satu file JSON yang sama, Claude bisa menerjemahkannya jadi CSS custom properties, Tailwind theme config, Dart `ThemeData` constants, atau format lain sesuai stack project target — tanpa perlu menyimpan ulang versi per-stack di library.

## Portable ke Claude Code

Folder skill ini (`design-tokens/` beserta isinya: `SKILL.md`, `scripts/`, `library/`) tidak bergantung pada fitur khusus Claude.ai. Kalau user mau pakai skill yang sama di Claude Code, cukup salin foldernya ke `~/.claude/skills/design-tokens/` (personal, lintas project) atau `.claude/skills/design-tokens/` di root sebuah project (khusus project itu). Isi `library/` ikut terbawa, jadi koleksi design system-nya tetap sama di kedua tempat — tidak perlu setup ulang. Kalau user memintanya, bantu siapkan salinan itu (copy folder, jangan symlink, supaya tidak tergantung struktur direktori Claude.ai).

## Struktur library

```
library/
├── index.json                  # daftar metadata semua design system
├── rebrew/
│   └── tokens.json             # semua kategori token milik "rebrew", nested dalam satu file
├── onyx-studio/
│   └── tokens.json
└── ...
```

`index.json` adalah satu-satunya sumber kebenaran soal design system apa saja yang ada. Setiap entri:

```json
{
  "id": "rebrew",
  "name": "rebrew",
  "tags": ["brand", "warm", "f&b", "light-dark"],
  "source": "design",
  "description": "Design system brand Rebrew — hangat, coklat/krem, ada varian dark mode.",
  "file": "rebrew/tokens.json"
}
```

- `source` menandai asal pembuatan: `design` (diekstrak dari desain/screenshot yang sudah ada), `prompt` (dibuat dari deskripsi teks), atau `code` (diambil dari kode/config yang sudah ada).
- `file` adalah path relatif ke folder `library/`, selalu `<id>/tokens.json`.

**Jangan edit `index.json` dengan tangan.** Selalu lewat `scripts/manage_library.py` (lihat di bawah) supaya formatnya tetap valid dan konsisten — script ini satu-satunya yang boleh menulis ke file itu. File `tokens.json` per design system boleh dan memang harus diedit langsung pakai Read/Write/Edit seperti biasa — isi token itu terlalu detail dan sering berubah untuk lewat argumen CLI.

## Format `tokens.json` (nested per kategori)

Tidak ada skema kaku yang dipaksakan (desain nyata bervariasi), tapi bentuk berikut menjaga konsistensi antar design system. Saat `manage_library.py add` membuat design system baru, kerangka kosong ini otomatis ditulis — tinggal diisi:

```json
{
  "color": {
    "primitive": { "brown-900": "#3B2412", "cream-50": "#FBF6EF" },
    "semantic": {
      "background": { "light": "#FBF6EF", "dark": "#1A120B" },
      "foreground": { "light": "#3B2412", "dark": "#F5ECE0" },
      "accent": { "light": "#B5651D", "dark": "#D98A3D" }
    }
  },
  "typography": {
    "fontFamily": { "heading": "Fraunces, serif", "body": "Inter, sans-serif" },
    "scale": { "xs": "0.75rem", "sm": "0.875rem", "base": "1rem", "lg": "1.125rem", "xl": "1.25rem", "2xl": "1.5rem", "3xl": "2rem" },
    "weight": { "regular": 400, "medium": 500, "bold": 700 },
    "lineHeight": { "tight": 1.2, "normal": 1.5, "relaxed": 1.75 }
  },
  "spacing": { "0": "0px", "1": "4px", "2": "8px", "3": "16px", "4": "24px", "5": "32px", "6": "48px", "7": "64px" },
  "radius": { "sm": "4px", "md": "10px", "lg": "18px", "full": "999px" },
  "shadow": { "sm": "0 1px 2px rgb(0 0 0 / 0.08)", "md": "0 6px 16px rgb(0 0 0 / 0.14)" },
  "breakpoint": { "sm": "480px", "md": "768px", "lg": "1024px", "xl": "1280px" },
  "motion": {
    "duration": { "fast": "120ms", "normal": "250ms", "slow": "400ms" },
    "easing": { "standard": "cubic-bezier(0.4,0,0.2,1)", "spring": "cubic-bezier(0.34,1.56,0.64,1)" }
  },
  "z-index": { "dropdown": 100, "modal": 300, "toast": 400 }
}
```

Kategori yang tidak relevan untuk suatu design system boleh dibiarkan kosong (`{}`) — jangan dihapus dari struktur, supaya bentuknya tetap konsisten antar design system saat dibandingkan atau ditampilkan di System Shelf.

### Konvensi metadata: `usage`, `notes`, `<kategori>Usage`

Kadang nilai token saja tidak cukup — perlu dicatat juga *kenapa*/*di mana* dipakai, atau kategori itu memang belum punya nilai konkret (baru sekadar dicatat konteksnya). Pakai sibling-key berikut, **jangan dianggap token asli** (System Shelf otomatis memfilternya dari tampilan swatch/nilai, cuma ditampilkan sebagai teks konteks):

- **`usage`** — sibling key di dalam object kategori (mis. `color.usage`), berisi object dengan key yang sama seperti token di sebelahnya, isinya deskripsi teks kapan/kenapa token itu dipakai. Contoh: `color.semantic.accent` punya nilai hex, `color.usage.accent` punya teks "dipakai untuk CTA utama, foil non-text saja".
- **`<kategori>Usage`** — sibling key di level top (mis. `spacingUsage`, `radiusUsage`, `breakpointUsage`), dipakai kalau kategori itu sendiri (`spacing`, `radius`, `breakpoint`) tidak punya struktur nested untuk ditaruhi `usage` di dalamnya. Isinya sama: object key→teks penjelasan, atau `{"notes": "..."}` kalau kategori itu memang masih kosong (`{}`) dan cuma perlu dicatat kenapa (mis. "belum ada spacing scale custom, masih pakai default Tailwind").
- **`notes`** — string bebas di level kategori (mis. `motion.notes`, `shadow.notes`) untuk konteks yang tidak cocok dipecah per-key, atau saat seluruh kategori itu memang kosong tapi ada hal penting untuk dicatat.

Contoh nyata pola ini ada di `library/undangoo-landing/tokens.json` dan `library/rebrew/tokens.json` (kalau sudah dibuat) — lihat langsung untuk referensi format.

## Menggunakan `scripts/manage_library.py`

Semua operasi terhadap metadata (tambah entri, cari, hapus, ubah field) lewat script ini, bukan ditulis manual sebagai JSON — supaya tidak ada typo struktur atau id yang bentrok:

```bash
# Tambah design system baru (otomatis membuat library/<id>/tokens.json kosong)
python scripts/manage_library.py add --name rebrew \
  --tags brand,warm,f&b --description "Design system brand Rebrew, hangat, ada dark mode" \
  --source design

# Lihat semua, atau filter
python scripts/manage_library.py list
python scripts/manage_library.py list --tag warm
python scripts/manage_library.py list --query rebrew

# Lihat detail satu design system (metadata + seluruh isi token)
python scripts/manage_library.py get --name rebrew

# Update metadata (deskripsi/tag/rename — bukan isi token)
python scripts/manage_library.py update --name rebrew --description "..."

# Hapus design system (otomatis hapus folder + tokens.json-nya juga)
python scripts/manage_library.py remove --name rebrew
```

Jalankan dari dalam folder skill ini (`design-tokens/`) supaya path relatif ke `library/` benar.

## Alur kerja

### 1. Menambah design system dari desain yang sudah ada (screenshot/mockup/Figma export)

Ini alur utama yang disebut user: dia sudah punya beberapa desain dan mau nilai-nilainya diekstrak jadi design system reusable. Tugas Claude:

1. Daftarkan dulu kerangkanya: `manage_library.py add --name <nama> --source design` (ini membuat `library/<id>/tokens.json` kosong).
2. Amati gambar/file desainnya dengan teliti: warna (termasuk variasi shade/tint dan light-dark kalau ada dua mode), font yang dipakai (heading vs body), skala ukuran teks yang terlihat berulang, jarak/spacing antar elemen, radius sudut, shadow, breakpoint kalau ada beberapa versi (mobile/desktop).
3. Isi `library/<id>/tokens.json` (Edit/Write tool) mengikuti format di atas, kategori demi kategori.
4. Tunjukkan ringkasan token yang berhasil diekstrak ke user (warna-warna utama, skala font, dll) dan konfirmasi sudah sesuai desain aslinya sebelum lanjut ke desain berikutnya — user bilang dia punya "beberapa desain", jadi proses ini kemungkinan diulang beberapa kali untuk beberapa design system berbeda.
5. Refresh System Shelf (lihat alur #7).

### 2. Menambah design system dari deskripsi teks (prompt)

User cerita ingin design system seperti apa tanpa desain jadi (mis. "bikinkan design system buat aplikasi finansial yang tegas dan modern"). Tugas Claude:

1. Rancang nilai-nilainya berdasarkan prinsip desain yang relevan (kontras, rasio skala tipografi yang wajar seperti 1.25/1.333, grid 8pt untuk spacing, dll). Kalau ada keputusan besar yang ambigu (warna brand utama, mood keseluruhan), boleh tanya singkat, tapi kalau sudah cukup jelas, langsung buat draft yang masuk akal.
2. Daftarkan dan isi seperti alur #1, dengan `--source prompt`.
3. Tunjukkan hasilnya secara ringkas dan tanya apakah perlu penyesuaian.

### 3. Menambah design system dari kode/config yang sudah ada

User kasih file config yang sudah ada (mis. `tailwind.config.js`, CSS `:root` variables, Flutter `ThemeData`) dan minta diekstrak jadi design system reusable di library ini. Tugas Claude:

1. Baca konfignya, ekstrak nilai-nilai murni (bukan syntax spesifik framework-nya) ke format JSON generik di atas.
2. Daftarkan dan isi seperti alur #1, dengan `--source code`.

### 4. Melihat daftar / mencari design system

Jalankan `manage_library.py list` (dengan filter tag/kata kunci kalau user menyebutnya), lalu sajikan ke user dalam bentuk yang gampang dipindai: nama dan deskripsi singkat — bukan dump JSON mentah. Kalau user minta lihat token lengkap satu design system tertentu, pakai `get`, atau arahkan ke System Shelf (lihat alur #7).

### 5. Update design system

Cari design system yang dimaksud (`get` atau `list` dulu kalau namanya tidak persis disebut user). Ada dua jenis perubahan:

- **Ubah metadata saja** (deskripsi, tag, atau rename) → pakai `manage_library.py update`.
- **Ubah isi token-nya** (warna, skala, dll) → edit `library/<id>/tokens.json` langsung pakai Edit tool. Kalau perubahannya cukup besar sehingga `description` lama sudah tidak akurat, update juga deskripsinya lewat script supaya tetap sinkron.

Setelah update yang mengubah tampilan tokennya, refresh System Shelf (alur #7).

### 6. Hapus design system

Cari dulu design system yang persis dimaksud kalau ada kemungkinan salah sasaran (nama mirip). Ini operasi yang tidak bisa dibatalkan — konfirmasi singkat dengan user sebelum menjalankan `manage_library.py remove`, kecuali user sudah eksplisit dan spesifik. Setelah dihapus, refresh System Shelf (alur #7).

### 7. Menjaga System Shelf (artifact viewer) tetap sinkron

User punya Artifact bernama **System Shelf** untuk melihat & memilih design system secara visual (daftar di sidebar kiri, spesimen detail di kanan, tombol salin nama/perintah). Artifact ini menyimpan data sebagai snapshot yang di-embed langsung di HTML-nya (`LIBRARY.groups` di dalam `<script>`), bukan baca live dari filesystem. Jadi **setiap kali** ada design system yang ditambah, diubah isinya, atau dihapus dari library ini:

1. Baca ulang `library/index.json` dan tiap `tokens.json` yang relevan.
2. Bangun ulang array `LIBRARY.groups` di file HTML System Shelf, satu entri per design system (`id`, `label`, `description`, `tokens` — struktur token sama persis dengan `tokens.json`, termasuk key metadata `usage`/`notes`/`<kategori>Usage` di atas, tidak perlu ditransformasi/dibuang — render function System Shelf (`pickTokens`/`isMetaKey`) sudah otomatis memfilternya dari tampilan swatch/nilai dan menampilkannya sebagai teks konteks).
3. **Opsional tapi disarankan**: isi juga field `example` di grup itu — satu string HTML lengkap (`<!doctype html>...`) berisi mini-demo (navbar/hero/CTA/komponen relevan) yang dibangun dari token design system tersebut, ditaruh sebagai `const EXAMPLE_<NAMA> = \`...\`;` terpisah lalu direferensikan `example: EXAMPLE_<NAMA>` di object grup. Field ini menyalakan tab "Contoh Penerapan" di System Shelf (di-render via `iframe.srcdoc`, di-set lewat JS bukan atribut HTML supaya tidak perlu escaping). Kalau tidak diisi, tab itu otomatis tidak muncul untuk grup tersebut — tidak wajib, tapi sangat membantu user memvisualisasikan token sebelum dipakai ke project nyata (lihat grup `undangoo-landing`/`rebrew` untuk contoh nyata).
4. Republish artifact itu (pakai `url` artifact yang sama, jangan buat baru) supaya link-nya tetap sama dan user langsung lihat versi terbaru.
5. Kalau user belum pernah bilang mau bikin/refresh System Shelf padahal baru pertama kali menambah design system, tawarkan singkat untuk membuatkannya.

### 8. Menerapkan design system ke project user

Saat user minta pasang design system tersimpan ke project-nya (termasuk pola seperti "buatkan X memakai design system 'abc'"):

1. Cari design system yang dimaksud lewat `get` (persis namanya), atau `list --query ...` kalau user menyebut sebagiannya saja.
2. Lihat stack project target (dari file yang sedang dikerjakan atau konteks project). Terjemahkan nilai JSON generik itu ke idiom stack tersebut:
   - **CSS/Tailwind**: CSS custom properties di `:root` (dan `[data-theme="dark"]` / `prefers-color-scheme` untuk varian dark), atau extend `theme.extend` di `tailwind.config`.
   - **shadcn**: map ke CSS variables yang dikenali shadcn (`--background`, `--foreground`, `--primary`, dst.) kalau semantic naming-nya cocok.
   - **Flutter**: `ThemeData` / `ColorScheme` + konstanta `TextStyle`, `EdgeInsets`, dll.
   - Stack lain: sesuaikan idiomnya, jangan sekadar dump JSON mentah ke file config.
3. Terapkan langsung ke file project yang relevan (jangan cuma menampilkan kode dan minta user pasang sendiri), lalu sebutkan singkat apa yang diubah/ditambahkan dan design system mana yang dipakai sebagai sumbernya.

## Menulis token yang baik

- Pisahkan **primitive** (nilai mentah: `brown-900: #3B2412`) dari **semantic** (alias bermakna: `accent: brown-900`) untuk kategori `color` — ini yang bikin dark mode dan rebranding gampang tanpa ubah semua pemakaian.
- Konsisten dalam satu design system: kalau `spacing` pakai `rem`, jangan campur `px` di kategori lain kecuali memang disengaja (mis. `breakpoint` memang lazim `px`).
- Beri nama design system yang jelas menyebut asal/tujuannya (`rebrew`, bukan `system-1`), supaya gampang dicari lagi nanti dan tidak ambigu saat user merujuknya di perintah lain (`"...menggunakan design system 'rebrew'"`).
- Kalau sebuah design system baru adalah variasi dari yang sudah ada (mis. rebrand ringan dari yang sudah tersimpan), lihat dulu (`get`) yang lama supaya konsisten struktur, alih-alih membuat skema baru dari nol.

## Handoff

- **Design system baru dari PRD** (belum ada token sama sekali, butuh filosofi warna/tipografi/layout dulu): pakai `design-brief` — skill itu menurunkan identitas visual dari tujuan bisnis di PRD, lalu **otomatis mendaftarkan hasilnya ke library ini** (lihat tahap 7 di skill itu). Jangan mulai dari skill ini kalau alasannya belum jelas; token tanpa filosofi di baliknya cuma daftar angka.
- **Menerapkan token ke UI nyata** (komponen/halaman yang sedang dibangun): `uiux-guide` Design mode — skill ini kasih nilainya, `uiux-guide` kasih aturan teknis penerapannya (kontras, grid 8-point, tap target, interaction states).
- **Menyimpan komponen/animasi jadi** yang dibangun dari token ini: `component-library` (markup+style komponen) dan `animation-library` (CSS/JS animasi) — token di sini adalah bahan mentahnya, dua skill itu menyimpan implementasinya.
- **Butuh aturan interaksi/behavior** (kapan pakai radio vs dropdown, pola loading/empty/error): itu `uiux-guide`, bukan skill ini — library ini murni menyimpan nilai visual, bukan aturan perilaku.
