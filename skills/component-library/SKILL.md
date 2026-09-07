---
name: component-library
description: 'Kelola library komponen UI pribadi milik user (button, card, navbar, form, modal, dst) dalam format HTML/CSS/JS generik yang portable ke stack apa pun. Bisa CRUD penuh — tambah, lihat/cari, update, hapus komponen. Komponen baru bisa dibuat dari tiga sumber — deskripsi teks/prompt ("bikinkan pricing card minimalis"), gambar/screenshot/mockup yang di-attach user, atau kode yang sudah ada yang di-paste/di-attach user dan tinggal disimpan. WAJIB gunakan skill ini setiap kali user menyebut "component library", "simpan komponen ini", "tambahin ke library komponen", "cari komponen yang ada", "komponen apa aja yang tersimpan", "update/ganti komponen X", "hapus komponen X", atau minta dibuatkan komponen UI (button/card/navbar/form/dll) dan/atau memintanya disimpan untuk dipakai lagi nanti — bahkan kalau user tidak menyebut kata "skill" atau "library" secara eksplisit. Skill ini portable: folder yang sama bisa dipasang di Claude.ai maupun Claude Code.'
---

# Component Library

Skill ini memberi Claude sebuah "lemari" berisi komponen UI milik user sendiri, yang terus tumbuh seiring waktu. Setiap komponen disimpan sebagai satu file HTML mandiri (markup + `<style>` + `<script>` di dalamnya sendiri) supaya benar-benar portable — bisa dibuka langsung di browser untuk preview cepat, dan tinggal diterjemahkan ke stack project mana pun (React/Next.js, Flutter, Vue, atau HTML polos) saat dipakai.

Karena lemari ini dipakai berulang-ulang lintas project dan lintas waktu, konsistensi metadata itu penting — bukan supaya rapi doang, tapi supaya nanti gampang dicari lagi ("card pricing yang kemarin itu namanya apa ya?"). Makanya setiap komponen punya identitas: nama unik, kategori, tag, deskripsi singkat, dan catatan dari mana asalnya (prompt, gambar, atau kode yang sudah ada).

## Portable ke Claude Code

Folder skill ini (`component-library/` beserta isinya: `SKILL.md`, `scripts/`, `library/`) tidak bergantung pada fitur khusus Claude.ai. Kalau user mau pakai skill yang sama di Claude Code, cukup salin foldernya ke `~/.claude/skills/component-library/` (personal, lintas project) atau `.claude/skills/component-library/` di root sebuah project (khusus project itu). Isi `library/` ikut terbawa, jadi koleksi komponennya tetap sama di kedua tempat — tidak perlu setup ulang. Kalau user memintanya, bantu siapkan salinan itu (copy folder, jangan symlink, supaya tidak tergantung struktur direktori Claude.ai).

## Struktur library

```
library/
├── index.json           # daftar metadata semua komponen
├── buttons/
│   └── gradient-cta.html
├── cards/
│   └── pricing-minimal.html
└── ...
```

`index.json` adalah satu-satunya sumber kebenaran soal komponen apa saja yang ada. Setiap entri:

```json
{
  "id": "pricing-minimal",
  "name": "pricing-minimal",
  "category": "cards",
  "tags": ["pricing", "minimal", "saas"],
  "source": "prompt",
  "description": "Card pricing 3 kolom, minimalis, highlight di paket tengah, responsive.",
  "file": "cards/pricing-minimal.html"
}
```

`file` adalah path relatif ke folder `library/`, isinya komponen HTML/CSS/JS yang sebenarnya. `source` menandai asal pembuatan (`prompt`, `image`, atau `code`) — berguna untuk konteks kalau nanti perlu dibuat ulang atau disesuaikan lagi.

**Jangan edit `index.json` dengan tangan.** Selalu lewat `scripts/manage_library.py` (lihat di bawah) supaya formatnya tetap valid dan konsisten — script ini satu-satunya yang boleh menulis ke file itu. File komponen itu sendiri (`cards/pricing-minimal.html` dst.) boleh dan memang harus diedit langsung pakai Read/Write/Edit seperti biasa.

## Menggunakan `scripts/manage_library.py`

Semua operasi terhadap metadata (tambah entri, cari, hapus, ubah field) lewat script ini, bukan ditulis manual sebagai JSON — supaya tidak ada typo struktur atau id yang bentrok:

```bash
# Tambah entri baru (file komponennya harus sudah kamu tulis duluan)
python scripts/manage_library.py add --name pricing-minimal --category cards \
  --tags pricing,minimal,saas --file cards/pricing-minimal.html \
  --description "Card pricing 3 kolom, minimalis, highlight paket tengah" \
  --source prompt

# Lihat semua, atau filter
python scripts/manage_library.py list
python scripts/manage_library.py list --category cards
python scripts/manage_library.py list --query pricing

# Lihat detail satu komponen (metadata + isi kode)
python scripts/manage_library.py get --name pricing-minimal

# Update salah satu field metadata (mis. rename, ganti deskripsi/tag/kategori)
python scripts/manage_library.py update --name pricing-minimal --description "..."

# Hapus entri (otomatis hapus file komponennya juga)
python scripts/manage_library.py remove --name pricing-minimal
```

Jalankan dari dalam folder skill ini (`component-library/`) supaya path relatif ke `library/` benar.

## Alur kerja

### 1. Menambah komponen dari deskripsi teks (prompt)

User cerita komponen seperti apa yang dia mau, dengan bahasa natural — bukan spesifikasi teknis. Tugas Claude:

1. Rancang markup, style, dan (kalau perlu interaksi) script-nya sebagai satu file HTML mandiri. Kalau ada detail penting yang ambigu (warna/brand, ukuran, ada varian dark mode atau tidak), boleh tanya singkat, tapi kalau sudah cukup jelas, langsung buat draft yang masuk akal daripada menahan progres dengan banyak pertanyaan.
2. Tulis file-nya ke `library/<category>/<nama>.html` (Write tool), lalu daftarkan lewat `manage_library.py add` dengan `--source prompt`.
3. Tunjukkan hasilnya ke user secara singkat (potongan kode atau ringkasan visual) dan konfirmasi nama/kategorinya sudah pas.

### 2. Menambah komponen dari gambar/screenshot/mockup

User attach gambar (screenshot desain, mockup Figma, foto UI referensi) dan minta dibuatkan komponennya. Tugas Claude:

1. Amati gambarnya dengan teliti: layout, spacing, warna, tipografi, state (hover/active kalau terlihat), dan elemen-elemen di dalamnya. Jangan menebak detail yang jelas terlihat di gambar — cocokkan sedekat mungkin.
2. Bangun sebagai HTML/CSS/JS mandiri seperti alur #1. Kalau ada bagian gambar yang ambigu (misalnya teks placeholder atau ikon yang tidak jelas), pakai asumsi wajar dan sebutkan singkat ke user, jangan berhenti untuk bertanya hal kecil.
3. Simpan file + daftarkan lewat script dengan `--source image`, sama seperti alur pertama.
4. Tunjukkan hasilnya dan tanya apakah sudah cukup dekat dengan gambar aslinya — desain dari gambar biasanya butuh satu ronde penyesuaian kecil (warna persis, jarak, dll).

### 3. Menambah komponen dari kode yang sudah ada

User kasih (paste atau attach file) kode komponen yang sudah jadi dan minta disimpan ke library. Tugas Claude:

1. Baca kodenya, pahami fungsinya secara garis besar (ini penting untuk mengisi `description` dan `tags` yang berguna nanti, bukan cuma menyalin mentah).
2. Kalau kode aslinya dalam bentuk komponen framework (React/Vue/Flutter widget), bungkus jadi versi HTML/CSS/JS mandiri yang merepresentasikan tampilan & perilakunya, supaya tetap portable lintas stack di library ini — tapi jangan ubah desain/perilakunya, hanya bentuk pembungkusnya.
3. Kalau user belum kasih nama/kategori, usulkan salah satu berdasarkan isi kodenya, tapi konfirmasi dulu — nama komponen itu identitas yang akan dipakai user untuk mencarinya lagi nanti.
4. Simpan file + daftarkan lewat script dengan `--source code`, sama seperti alur pertama.

### 4. Melihat daftar / mencari komponen

Jalankan `manage_library.py list` (dengan filter kalau user menyebut kategori/kata kunci tertentu), lalu sajikan ke user dalam bentuk yang gampang dipindai: nama, kategori, dan deskripsi singkat tiap komponen — bukan dump JSON mentah. Kalau user minta lihat kode lengkap satu komponen tertentu, pakai `get`.

### 5. Update komponen

Cari komponen yang dimaksud (`get` atau `list` dulu kalau namanya tidak persis disebut user). Ada dua jenis perubahan:

- **Ubah metadata saja** (deskripsi, tag, kategori, atau rename) → pakai `manage_library.py update`.
- **Ubah tampilan/perilaku komponennya** (warna, layout, interaksi) → edit file HTML-nya langsung pakai Edit tool. Kalau perubahannya cukup besar sehingga `description` lama sudah tidak akurat, update juga deskripsinya lewat script supaya tetap sinkron.

### 6. Hapus komponen

Cari dulu komponen yang persis dimaksud kalau ada kemungkinan salah sasaran (nama mirip, atau user cuma menyebut kategori). Ini operasi yang tidak bisa dibatalkan — konfirmasi singkat dengan user sebelum menjalankan `manage_library.py remove`, kecuali user sudah eksplisit dan spesifik ("hapus pricing-minimal dari library").

### 7. Menerapkan komponen ke project user

Komponen di library ditulis sebagai HTML/CSS/JS generik supaya netral terhadap stack, tapi kebanyakan pemakaian sebenarnya adalah menempelkannya ke project yang pakai stack tertentu. Saat user minta pasang komponen tersimpan ke project-nya:

1. Cari komponennya lewat `get` (persis namanya) atau `list --query ...` (kalau cuma menyebut jenisnya, mis. "pasang card pricing yang tersimpan").
2. Lihat stack project target (React/Next.js, Flutter, Vue, dll — dari file yang sedang dikerjakan atau konteks project). Terjemahkan markup/CSS/JS generik itu ke idiom stack tersebut: misalnya jadi komponen React dengan className dan props, atau widget Flutter dengan `Container`/`Column`/state setara — bukan sekadar menempel tag HTML mentah ke dalam file `.jsx` atau `.dart`.
3. Kalau target project-nya sendiri HTML polos, bisa ditempel hampir langsung, sesuaikan penamaan class supaya tidak bentrok dengan class lain di project.
4. Terapkan langsung ke file project yang relevan (jangan cuma menampilkan kode dan minta user pasang sendiri), lalu sebutkan singkat apa yang diubah/ditambahkan.

## Menulis komponen yang baik

Ini bukan sekadar preferensi gaya — beberapa hal ini menentukan apakah komponennya gampang dipakai ulang atau malah merepotkan saat ditempel ke project lain:

- Satu file HTML mandiri per komponen: markup di `<body>`, style di `<style>` (bukan inline style bertebaran, biar gampang di-scan), dan script (kalau ada interaksi) di `<script>` di bagian bawah.
- Gunakan HTML semantik (`<button>`, `<nav>`, `<article>`, dst.) dan atribut aksesibilitas dasar (`aria-label`, `alt`) yang relevan — komponen ini akan dipakai di project nyata, bukan cuma demo sekali pakai.
- Buat responsive secara default (pakai relative units, flexbox/grid, media query kalau perlu) kecuali user memang minta ukuran fixed.
- Nama class harus spesifik dan namespaced (mis. `.comp-pricing-card` bukan `.card`), supaya kecil kemungkinan bentrok dengan class lain saat ditempel ke project user.
- Pakai CSS custom property untuk nilai yang mungkin sering di-tweak (warna brand, radius, spacing utama), supaya gampang dikustomisasi tanpa bongkar seluruh style.
- Kalau komponennya extend dari sesuatu yang sudah ada di library (mis. varian lain dari card yang sudah tersimpan), lihat dulu komponen itu (`get`) supaya konsisten gaya, alih-alih membangun dari nol dengan konvensi yang beda.
