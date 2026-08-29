# Panduan Teori UI/UX untuk Pembuatan Antarmuka

Panduan ini merangkum teori-teori inti yang saling berkolaborasi untuk memastikan antarmuka estetik, fungsional, terukur, dan minim hambatan interaksi. Disusun sebagai referensi cepat saat mendesain atau melakukan review UI.

---

## 1. Teori Warna & Proporsi (Aturan 60-30-10)

Metode menyeimbangkan harmoni visual tanpa membuat antarmuka berantakan. Sifatnya heuristik fleksibel — rasio bisa bergeser tergantung identitas brand (misal aplikasi fintech kadang memakai warna aksen >10% untuk elemen kepercayaan/trust signal).

| Proporsi | Fungsi Utama | Contoh Penerapan UI |
|---|---|---|
| **60% (Dominan)** | Pemersatu desain, area istirahat mata | Background layar, background container utama |
| **30% (Sekunder)** | Kedalaman & hierarki informasi | Cards, bilah navigasi, sub-judul, elemen pendukung |
| **10% (Aksen)** | Titik fokus utama, mengundang interaksi | Tombol CTA, badge notifikasi, pesan error/sukses |

### 1.1 Kontras & Aksesibilitas Warna (WCAG)
Sering terlewat padahal krusial secara hukum & etika desain:
- Rasio kontras teks-ke-background minimal **4.5:1** untuk teks normal, **3:1** untuk teks besar (≥18pt atau 14pt bold) — standar WCAG AA.
- Jangan mengandalkan warna saja untuk menyampaikan status (merah/hijau untuk error/sukses) — sertakan ikon atau label teks, karena ~8% pria mengalami buta warna merah-hijau.
- Uji palet dengan color-blindness simulator sebelum finalisasi.

---

## 2. Manajemen Ruang Kosong (White Space & Grid)

Pengelolaan jarak untuk mengurangi beban kognitif dan menjaga keterbacaan.

- **Micro spacing**: jarak sempit di dalam satu komponen (spasi teks, jarak ikon ke label).
- **Macro spacing**: struktur besar layar (margin kiri/kanan, jarak antar komponen berbeda).

### 2.1 Sistem Grid 8-Point
Standar tata letak menggunakan kelipatan 8 (8, 16, 24, 32, 48, dst.) untuk margin dan padding. Memastikan elemen tetap proporsional, tajam, dan seragam saat di-build lintas resolusi layar dan platform (khususnya penting saat bekerja dengan Flutter/Next.js di banyak breakpoint).

### 2.2 Spacing Antar Tap Target
Selain ukuran tap target itu sendiri (lihat Hukum Fitts), jarak **antar** target berdekatan minimal **8px** untuk mencegah mis-tap — penting saat banyak icon button berdempetan.

---

## 3. Psikologi Visual & Perilaku Pengguna

Aturan yang memanfaatkan kebiasaan alami otak manusia dalam memproses informasi.

### 3.1 Hierarki Visual & Pola Baca
Mengatur bobot elemen (ukuran font, ketebalan, kontras, warna).

| Pola | Kapan Dipakai | Karakteristik |
|---|---|---|
| **Pola Z** | Layar berpusat pada satu aksi (landing page, onboarding) | Mata menyapu kiri→kanan atas, diagonal ke kiri bawah, berakhir di CTA kanan bawah |
| **Pola F** | Layar penuh konten (list, artikel, dashboard) | Mata menyapu horizontal di atas, lalu turun vertikal di sisi kiri, scan horizontal lebih pendek berikutnya |

### 3.2 Prinsip Gestalt (Lengkap)
| Prinsip | Penjelasan | Contoh |
|---|---|---|
| **Proximity (Kedekatan)** | Elemen berspasi dekat (±8px) dianggap satu kesatuan; jauh (±32px) menandakan pergantian topik | Grouping form fields vs section baru |
| **Similarity (Kesamaan)** | Elemen yang bisa diklik harus seragam gaya visualnya | Semua tombol sekunder pakai style yang sama |
| **Closure** | Otak melengkapi bentuk yang tidak utuh | Logo yang sengaja "terputus" tapi tetap terbaca |
| **Common Region** | Elemen dalam satu batas visual (card/border/background block) dianggap satu grup meski jaraknya tidak dekat | Card dengan border/shadow mengelompokkan info di dalamnya |
| **Figure-Ground** | Kontras antara elemen fokus (figure) dan latar (ground) | Overlay gelap di belakang modal/dialog |
| **Continuity** | Mata mengikuti garis/alur yang kontinu | Progress bar, stepper horizontal |

### 3.3 Hukum & Heuristik Kognitif

| Hukum | Isi | Implikasi Desain |
|---|---|---|
| **Hukum Hick** | Waktu pengambilan keputusan sebanding dengan jumlah opsi | Batasi navigasi utama maks. 4-5 item |
| **Hukum Fitts** | Kecepatan & akurasi sentuh ditentukan jarak & ukuran elemen | Tap target min. 44x44 atau 48x48px, tempatkan di jangkauan alami ibu jari |
| **Miller's Law (7±2)** | Kapasitas memori kerja manusia terbatas | Chunking: pecah form panjang jadi beberapa step, kelompokkan menu jadi kategori |
| **Jakob's Law** | Pengguna menghabiskan waktu di produk lain, mengharapkan pola serupa | Ikon keranjang di kanan atas, hamburger menu, swipe-to-delete di mobile |
| **Von Restorff Effect** | Elemen yang menonjol beda dari sekitarnya lebih diingat | CTA warna kontras tinggi di antara elemen netral |
| **Aesthetic-Usability Effect** | Desain estetik dipersepsikan lebih usable, bahkan sebelum diuji fungsinya | Polish visual tetap penting meski fungsi sudah jalan |
| **Peak-End Rule** | Pengguna mengingat momen puncak & momen akhir, bukan rata-rata pengalaman | Animasi sukses yang memuaskan di akhir checkout/onboarding |
| **Serial Position Effect** | Item di awal & akhir list lebih diingat dibanding tengah | Taruh opsi/fitur terpenting di posisi awal atau akhir list |

---

## 4. Ergonomi Mobile — Thumb Zone Map

Pengembangan dari Hukum Fitts, berdasarkan riset Steven Hoober tentang jangkauan ibu jari di layar mobile:

- **Zona mudah dijangkau**: bawah-tengah layar → tempatkan CTA utama & navigasi di sini.
- **Zona perlu peregangan**: bagian tengah-atas layar.
- **Zona sulit dijangkau**: pojok atas berlawanan dengan tangan dominan → hindari aksi penting di sini (biasanya area status bar/back button saja).

Ini alasan tren app mobile modern menaruh bottom navigation bar dan FAB (Floating Action Button) di bawah, bukan di atas.

---

## 5. Aksesibilitas & Inklusivitas (Ringkasan Tambahan)

- Ukuran font minimum untuk body text: 14-16sp/px agar tetap terbaca tanpa zoom.
- Dukung dynamic type / text scaling tanpa merusak layout.
- Pastikan semua elemen interaktif dapat diakses via keyboard/screen reader (khusus web/Next.js: gunakan atribut ARIA yang sesuai).
- Hindari flashing/blinking content yang bisa memicu photosensitive seizure.

---

## 6. Motion & Micro-interaction

Belum tentu disadari tapi berdampak besar ke persepsi kualitas produk:

- Durasi transisi standar: **200-300ms** untuk micro-interaction (tombol, toggle), **300-500ms** untuk transisi antar layar.
- Gunakan easing curve seperti `ease-in-out` atau `cubic-bezier` — hindari linear karena terasa kaku/robotic.
- Motion menjaga kontinuitas Gestalt saat elemen berpindah/muncul (misal: elemen yang di-tap "membesar" menjadi halaman baru, bukan tiba-tiba berganti).
- Gunakan motion secukupnya — motion berlebihan justru menambah beban kognitif dan terasa mengganggu.

---

## 7. Konsistensi Sistem — Nielsen's 10 Usability Heuristics (Poin Relevan)

Kerangka klasik yang melengkapi hukum-hukum di atas:

1. **Visibility of system status** — selalu beri feedback (loading indicator, progress bar, toast notification).
2. **Match between system and real world** — gunakan bahasa & konsep yang familiar bagi pengguna, bukan jargon teknis/internal.
3. **User control and freedom** — sediakan jalan keluar/undo yang jelas (tombol back, cancel).
4. **Consistency and standards** — selaras dengan Jakob's Law; jangan menciptakan pola baru tanpa alasan kuat.
5. **Error prevention** — lebih baik cegah error (disable tombol submit sebelum form valid) daripada hanya menampilkan pesan error yang bagus.
6. **Recognition rather than recall** — tampilkan opsi yang bisa dipilih, jangan memaksa pengguna mengingat informasi.
7. **Flexibility and efficiency of use** — sediakan shortcut untuk power user tanpa membebani pengguna baru.
8. **Aesthetic and minimalist design** — hanya tampilkan informasi yang relevan; setiap elemen tambahan bersaing dengan elemen esensial.
9. **Help users recognize, diagnose, and recover from errors** — pesan error harus jelas, dalam bahasa manusia, dan menyertakan solusi.
10. **Help and documentation** — meski idealnya UI self-explanatory, sediakan bantuan kontekstual saat dibutuhkan.

---

## 8. Design Tokens & Konsistensi Sistem

Untuk implementasi lintas platform (relevan untuk stack Flutter + Next.js):

- Definisikan **design tokens** terpusat: warna (primary/secondary/accent/semantic), spacing (kelipatan 8), radius, shadow, typography scale.
- Satu sumber kebenaran (single source of truth) agar konsisten di web dan mobile — hindari hardcode nilai berulang di tiap komponen.
- Terapkan skala tipografi yang konsisten (misal: 12/14/16/20/24/32px) daripada ukuran font acak per halaman.

---

## Checklist Ringkas Sebelum Ship

- [ ] Rasio warna 60-30-10 terpenuhi, kontras teks memenuhi WCAG AA (4.5:1)
- [ ] Semua spacing mengikuti kelipatan 8-point grid
- [ ] Navigasi utama ≤ 5 item (Hukum Hick)
- [ ] Tap target ≥ 44x44px, jarak antar target ≥ 8px (Hukum Fitts)
- [ ] CTA & navigasi utama berada di thumb zone (mobile)
- [ ] Elemen interaktif punya gaya visual seragam (Similarity)
- [ ] Grouping informasi jelas via jarak/border (Proximity, Common Region)
- [ ] Status sistem selalu terlihat (loading, error, success state)
- [ ] Transisi/motion halus (200-300ms, easing non-linear)
- [ ] Tidak mengandalkan warna saja untuk status (ada ikon/label pendukung)
- [ ] Design tokens terdefinisi & konsisten lintas platform
