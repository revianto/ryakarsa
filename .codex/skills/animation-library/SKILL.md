---
name: animation-library
description: Kelola library animasi CSS/JS pribadi milik user dan terapkan animasi itu ke project mereka. Bisa menambah snippet animasi baru dari deskripsi teks (mis. "fade in pelan dari bawah") atau dari kode animasi yang sudah ada, menampilkan daftar animasi tersimpan (dengan filter kategori/tag), memperbarui animasi yang sudah ada, dan menghapusnya. Juga menerapkan animasi (yang sudah tersimpan atau yang baru dibuat saat itu juga) langsung ke elemen, gambar/ikon, file project, atau potongan kode yang disebut/dilampirkan user. WAJIB gunakan skill ini setiap kali user menyebut kata seperti "animasi", "animate", "transition", "keyframe", "hover effect", "fade in/out", "bounce", "spin", "micro-interaction", atau minta hal-hal seperti "tambahin animasi ke tombol/logo/gambar ini", "bikin animasi buat card ini", "lihat animasi apa aja yang udah ada", "update/ganti animasi X", atau "hapus animasi X" — bahkan kalau user tidak menyebut kata "skill" atau "library" secara eksplisit.
---

# Animation Library

Skill ini memberi Claude sebuah "lemari" berisi snippet animasi CSS/JS milik user sendiri, yang terus tumbuh seiring waktu. User bisa menambah animasi baru, melihat isi lemarinya, mengubah, menghapus, dan yang paling sering: minta animasi itu (atau animasi baru) langsung dipasang ke project mereka.

Karena lemari ini dipakai berulang-ulang lintas project dan lintas waktu, konsistensi penamaan dan metadata itu penting — bukan supaya rapi doang, tapi supaya nanti gampang dicari lagi ("animasi yang kayak kemarin itu apa namanya ya?"). Makanya setiap snippet punya identitas: nama unik, kategori, tag, deskripsi singkat, dan stack (vanilla CSS/JS, Tailwind, GSAP, React/framer-motion, atau Motion).

## Struktur library

```
library/
├── index.json          # daftar metadata semua snippet
├── entrance/            # folder per kategori, berisi file kode aktual
│   └── fade-in-slow.css
├── loading/
│   └── spinner-basic.css
└── ...
```

`index.json` adalah satu-satunya sumber kebenaran soal snippet apa saja yang ada. Setiap entri:

```json
{
  "id": "fade-in-slow",
  "name": "fade-in-slow",
  "category": "entrance",
  "tags": ["fade", "subtle", "card"],
  "stack": "vanilla-css",
  "description": "Fade in sambil geser naik dari bawah, durasi 0.8s, cocok untuk card/section muncul saat load atau scroll.",
  "file": "entrance/fade-in-slow.css"
}
```

`file` adalah path relatif ke folder `library/`, isinya kode animasi yang sebenarnya (CSS murni, JS, atau komponen, tergantung `stack`).

**Jangan edit `index.json` dengan tangan.** Selalu lewat `scripts/manage_library.py` (lihat di bawah) supaya formatnya tetap valid dan konsisten — script ini satu-satunya yang boleh menulis ke file itu. File kode animasi itu sendiri (`entrance/fade-in-slow.css` dst.) boleh dan memang harus diedit langsung pakai Read/Write/Edit seperti biasa.

## Menggunakan `scripts/manage_library.py`

Semua operasi terhadap metadata (tambah entri, cari, hapus, ubah field) lewat script ini, bukan ditulis manual sebagai JSON — supaya tidak ada typo struktur atau id yang bentrok:

```bash
# Tambah entri baru (file kode-nya harus sudah kamu tulis duluan)
python scripts/manage_library.py add --name fade-in-slow --category entrance \
  --tags fade,subtle,card --stack vanilla-css --file entrance/fade-in-slow.css \
  --description "Fade in sambil geser naik dari bawah, durasi 0.8s"

# Lihat semua, atau filter
python scripts/manage_library.py list
python scripts/manage_library.py list --category entrance
python scripts/manage_library.py list --query bounce

# Lihat detail satu snippet (metadata + isi kode)
python scripts/manage_library.py get --name fade-in-slow

# Update salah satu field metadata (mis. rename atau ganti deskripsi)
python scripts/manage_library.py update --name fade-in-slow --description "Durasi 1.2s"

# Hapus entri (otomatis hapus file kode-nya juga)
python scripts/manage_library.py remove --name fade-in-slow
```

Jalankan dari dalam folder skill ini (`animation-library/`) supaya path relatif ke `library/` benar.

## Alur kerja

### 1. Menambah animasi dari deskripsi teks (prompt)

User cerita animasi seperti apa yang dia mau, dengan bahasa natural — bukan spesifikasi teknis. Tugas Claude:

1. Terjemahkan deskripsi itu ke kode. Kalau ada detail yang ambigu dan penting (durasi, easing, trigger seperti on-load vs on-scroll vs on-hover), boleh tanya singkat, tapi kalau sudah cukup jelas, langsung buat draft yang masuk akal daripada menahan progres dengan banyak pertanyaan.
2. Pilih `stack` yang sesuai — default ke vanilla CSS/JS kecuali user menyebut Tailwind, GSAP, React/framer-motion, atau Motion, atau project yang sedang dikerjakan jelas-jelas pakai salah satunya. Kalau user cuma minta "yang ringan/performant" tanpa nama library spesifik dan animasinya butuh JS (bukan CSS murni), pertimbangkan `motion` dulu sebelum `gsap` — lebih kecil bundle-nya untuk kebutuhan animasi umum (lihat `references/stacks.md`).
3. Tulis file kodenya ke `library/<category>/<name>.<ext>` (Write tool), lalu daftarkan lewat `manage_library.py add`.
4. Tunjukkan hasil kodenya ke user secara singkat dan konfirmasi nama/kategorinya sudah pas.

### 2. Menambah animasi dari kode yang sudah ada

User kasih (paste atau attach file) kode animasi yang sudah jadi dan minta disimpan ke library. Tugas Claude:

1. Baca kodenya, pahami efeknya secara garis besar (ini penting untuk mengisi `description` dan `tags` yang berguna nanti, bukan cuma menyalin mentah).
2. Kalau user belum kasih nama/kategori, usulkan salah satu berdasarkan isi kodenya, tapi konfirmasi dulu — nama snippet itu identitas yang akan dipakai user untuk mencarinya lagi nanti, jadi lebih baik user yang menentukan kata terakhir.
3. Rapikan kode secukupnya (format konsisten, komentar singkat kalau efeknya tidak jelas dari nama variabel) tanpa mengubah perilaku animasinya — ini kode milik user, bukan draft Claude.
4. Simpan file + daftarkan lewat script, sama seperti alur pertama.

### 3. Melihat daftar animasi

Jalankan `manage_library.py list` (dengan filter kalau user menyebut kategori/kata kunci tertentu), lalu sajikan ke user dalam bentuk yang gampang dipindai: nama, kategori, dan deskripsi singkat tiap animasi — bukan dump JSON mentah.

### 4. Update animasi

Cari snippet yang dimaksud (`get` atau `list` dulu kalau namanya tidak persis disebut user). Ada dua jenis perubahan:

- **Ubah metadata saja** (deskripsi, tag, kategori, atau rename) → pakai `manage_library.py update`.
- **Ubah kode animasinya** (durasi, easing, keyframe, dll) → edit file kodenya langsung pakai Edit tool. Kalau efeknya jadi cukup berbeda sehingga `description` lama sudah tidak akurat, update juga deskripsinya lewat script supaya tetap sinkron.

### 5. Hapus animasi

Cari dulu snippet yang persis dimaksud kalau ada kemungkinan salah sasaran (nama mirip, atau user cuma menyebut kategori). Ini operasi yang tidak bisa dibatalkan — konfirmasi singkat dengan user sebelum menjalankan `manage_library.py remove`, kecuali user sudah eksplisit dan spesifik ("hapus fade-in-slow dari library").

### 6. Menerapkan animasi ke project user

Ini alur yang paling sering dipakai, dan paling banyak variasinya. User bisa merujuk ke target dengan cara apa saja: menyebut nama file ("di index.html"), menyebut gambar/ikon yang mau dianimasikan ("animasikan logo.png ini", "kasih efek ke icon-nya"), atau menempelkan potongan kode langsung di chat.

Langkah umum:

1. **Cari tahu efek yang diinginkan.** Kalau user menyebut nama snippet yang persis ada di library, pakai itu. Kalau cuma menyebut jenis efek ("bikin logo-nya muncul dengan mantul"), cari yang paling cocok lewat `manage_library.py list --query ...` atau berdasarkan kategori/tag. Kalau tidak ada yang cocok di library, buat animasi baru untuk kebutuhan ini (ikuti alur #1), lalu di akhir tawarkan untuk disimpan ke library juga — jangan simpan otomatis tanpa tanya, karena tidak semua animasi sekali pakai perlu masuk koleksi permanen.
2. **Cari target di project.** Kalau user menyebut nama file, buka file itu. Kalau user menyebut gambar/ikon (mis. `logo.png`, `icon-cart.svg`), cari di mana file itu direferensikan (`<img src=...>`, `background-image`, import komponen, dll) — gunakan Grep/Read untuk menemukannya kalau user tidak menyebut file spesifik. Kalau user menempel kode langsung di pesan tanpa menyebut file, targetnya adalah kode itu sendiri, bukan file di disk.
3. **Terapkan.** Sesuai jawaban default: kalau ada file project yang jelas, **langsung edit file itu** (bungkus elemen dengan class/wrapper kalau perlu, sisipkan keyframes/CSS ke stylesheet yang relevan atau `<style>` block yang sudah ada, atau tambahkan kode JS/komponen sesuai stack-nya) — jangan cuma menampilkan kode dan minta user pasang sendiri. Kalau targetnya cuma potongan kode di chat (tidak ada file), kembalikan versi kode yang sudah diberi animasi sebagai balasan.
4. Sebutkan singkat apa yang diubah (nama elemen, file, animasi yang dipakai) supaya user bisa cross-check, tapi tidak perlu menjelaskan ulang seluruh kode baris demi baris.

## Menulis kode animasi yang baik

Ini bukan sekadar preferensi gaya — beberapa hal ini menentukan apakah animasinya terasa mulus atau malah patah-patah/berat di browser user:

- Utamakan animasikan `transform` dan `opacity` dibanding properti lain (`width`, `top`, `left`, dst.) karena browser bisa meng-compositing keduanya tanpa layout reflow — animasi jadi jauh lebih smooth, apalagi di perangkat low-end.
- Sertakan durasi dan easing sebagai CSS custom property (`--duration`, `--ease`) kalau masuk akal, supaya orang yang pakai snippet ini nanti gampang tweak tanpa bongkar keyframes.
- Hormati `prefers-reduced-motion` — tambahkan media query yang menonaktifkan/menyederhanakan animasi untuk user yang mengaktifkan setting itu di OS-nya, kecuali animasinya memang sudah sangat minimal.
- Nama class harus spesifik dan namespaced (mis. `.anim-fade-in-slow` bukan `.fade`), supaya kecil kemungkinan bentrok dengan class lain di project user.
- Untuk stack selain vanilla CSS/JS (Tailwind, GSAP, React/framer-motion, Motion), lihat `references/stacks.md` untuk pola dan contoh yang idiomatis di masing-masing — jangan tulis animasi GSAP dengan gaya vanilla CSS dipaksakan jadi JS, atau sebaliknya.

## Dari mana durasi/easing diambil

**Jangan tentukan durasi/easing acak kalau sudah ada sumbernya.** Urutan mencari:

1. **User menyebut design system tertentu**, atau animasi ini turunan dari sebuah design brief → cek `design-tokens` (`manage_library.py get --name <nama>`) untuk kategori `motion` (`duration`/`easing`). Kalau design system itu punya level animasi yang sudah ditetapkan (Minimal/Sedang/Kaya — lihat skill `design-brief`), hormati itu: jangan bikin animasi showcase untuk design system yang levelnya "Minimal".
2. **Project yang sedang dibuka** punya konvensi animasi sendiri (keyframes di `globals.css`, durasi yang berulang di komponen lain) → ikuti pola itu supaya konsisten.
3. **Tidak ada keduanya** → pakai default `uiux-guide`: 200–300ms untuk micro-interaction, 300–500ms untuk transisi antar layar, easing `ease-in-out`/`cubic-bezier` (jangan pernah `linear`), dan selalu sediakan fallback `prefers-reduced-motion`.

## Handoff

- **Nilai motion token** (durasi/easing dari design system tersimpan): `design-tokens`, kategori `motion`.
- **Aturan kapan motion boleh dipakai** (durasi wajar, reduced-motion, motion yang justru menambah beban kognitif): `uiux-guide`.
- **Komponen yang dianimasikan**: `component-library` — simpan komponennya di sana, animasinya di sini, supaya animasi yang sama bisa dipasang ke beberapa komponen.

## Referensi

- `references/stacks.md` — pola dan contoh kode untuk tiap stack (vanilla CSS/JS, Tailwind, GSAP, React/framer-motion, Motion), dan kapan masing-masing lebih cocok dipakai.
