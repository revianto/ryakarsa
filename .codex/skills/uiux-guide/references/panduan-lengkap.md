# Panduan Teori UI/UX untuk Pembuatan Antarmuka

Panduan ini merangkum teori-teori inti yang saling berkolaborasi untuk memastikan antarmuka estetik, fungsional, terukur, dan minim hambatan interaksi. Disusun sebagai referensi cepat saat mendesain, membangun, atau melakukan review UI.

> **Cara pakai panduan ini saat review:** jangan menilai kontras warna, spacing, atau ukuran elemen dari kira-kira mata. Hitung rasio kontras dari nilai hex secara programatik, dan baca nilai px/spacing/font-size aktual langsung dari kode/CSS/tema. Angka di dokumen ini adalah ambang minimum yang bisa diverifikasi, bukan estimasi.
>
> **Saat tidak ada brand kit/warna dari user:** jangan mengarang palet secara diam-diam. Nyatakan secara eksplisit token/asumsi apa yang dipilih (misal: "primary color diasumsikan biru #2563EB karena tidak ada brand guideline yang diberikan") agar mudah dikoreksi user.

---

## 1. Teori Warna & Proporsi (Aturan 60-30-10)

Metode menyeimbangkan harmoni visual tanpa membuat antarmuka berantakan. Sifatnya heuristik fleksibel — rasio bisa bergeser tergantung identitas brand (misal aplikasi fintech kadang memakai warna aksen >10% untuk elemen kepercayaan/trust signal).

| Proporsi | Fungsi Utama | Contoh Penerapan UI |
|---|---|---|
| **60% (Dominan)** | Pemersatu desain, area istirahat mata | Background layar, background container utama |
| **30% (Sekunder)** | Kedalaman & hierarki informasi | Cards, bilah navigasi, sub-judul, elemen pendukung |
| **10% (Aksen)** | Titik fokus utama, mengundang interaksi | Tombol CTA, badge notifikasi, pesan error/sukses |

### 1.1 Kontras & Aksesibilitas Warna (WCAG)
- Rasio kontras teks-ke-background minimal **4.5:1** untuk teks normal, **3:1** untuk teks besar (≥18pt atau 14pt bold) — WCAG AA (1.4.3).
- **Non-text contrast minimal 3:1** untuk komponen UI seperti border input, ikon, dan batas komponen interaktif lainnya — WCAG AA (1.4.11). Poin ini sering terlewat karena fokus biasanya hanya ke kontras teks.
- Jangan mengandalkan warna saja untuk menyampaikan status (merah/hijau untuk error/sukses) — sertakan ikon atau label teks, karena ~8% pria mengalami buta warna merah-hijau.
- Uji palet dengan color-blindness simulator sebelum finalisasi.

---

## 2. Manajemen Ruang Kosong (White Space & Grid)

Pengelolaan jarak untuk mengurangi beban kognitif dan menjaga keterbacaan.

- **Micro spacing**: jarak sempit di dalam satu komponen (spasi teks, jarak ikon ke label).
- **Macro spacing**: struktur besar layar (margin kiri/kanan, jarak antar komponen berbeda).

### 2.1 Sistem Grid 8-Point
Standar tata letak menggunakan kelipatan 8 (8, 16, 24, 32, 48, dst.) untuk margin dan padding. Memastikan elemen tetap proporsional, tajam, dan seragam saat di-build lintas resolusi layar dan platform.

### 2.2 Spacing Antar Tap Target
Selain ukuran tap target itu sendiri (lihat Hukum Fitts di bawah), jarak **antar** target berdekatan minimal **8px** untuk mencegah mis-tap — penting saat banyak icon button berdempetan.

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
| **Hukum Fitts** | Kecepatan & akurasi sentuh ditentukan jarak & ukuran elemen | Tap target min. **44x44px** (Apple HIG) / **48x48dp** (Material Design). Catatan: standar minimum resmi WCAG 2.2 AA (2.5.8) sebenarnya 24x24 CSS px — 44/48 lebih ketat dan lebih aman, jadi tetap dipakai sebagai target, bukan diturunkan |
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

## 5. Interaction States

Setiap elemen interaktif **wajib** punya definisi visual untuk seluruh state-nya — bukan cuma tampilan default. Ini area yang paling sering dilewatkan saat build UI:

| State | Wajib untuk | Catatan |
|---|---|---|
| **Default** | Semua elemen interaktif | Baseline |
| **Hover** | Elemen di platform dengan mouse/pointer (web/desktop) | Tidak berlaku untuk touch-only mobile |
| **Focus** | Semua elemen interaktif, terutama untuk keyboard navigation | Gunakan `focus-visible`, bukan menghilangkan outline focus demi estetika — ini pelanggaran aksesibilitas yang sangat umum |
| **Pressed / Active** | Tombol, tab, item yang bisa ditekan | Beri feedback instan (scale-down, perubahan warna) agar terasa responsif |
| **Disabled** | Tombol/field yang belum bisa diinteraksi | Kontras visual jelas dari state aktif, dan jangan hilangkan sepenuhnya dari alur (tetap terlihat, tidak hilang) |
| **Loading** | Aksi yang menunggu proses async | Sebaiknya disable elemen selama loading untuk cegah double-submit |

---

## 6. Form UX

Form adalah salah satu elemen UI yang paling sering dibuat, tapi juga paling sering salah diimplementasi. Aturan konkret:

- **Label di atas field**, bukan menjadikan placeholder sebagai satu-satunya label — placeholder hilang begitu user mulai mengetik, sehingga konteks field ikut hilang.
- **Validasi on-blur** (setelah user meninggalkan field), bukan per-keystroke — validasi real-time yang terlalu agresif terasa menghakimi dan mengganggu saat user masih mengetik.
- **Pesan error ditempatkan dekat field terkait**, bukan hanya di atas/bawah form, dan harus menyertakan cara memperbaikinya (bukan sekadar "Input tidak valid").
- **Gunakan `input type` dan keyboard yang sesuai** — `email`, `tel`, `number` — agar keyboard mobile otomatis menyesuaikan.
- **Gunakan atribut `autocomplete`** yang tepat (`name`, `email`, `tel`, `new-password`, dst.) agar browser/password manager bisa membantu isi otomatis.
- **Toggle show/hide password** — jangan paksa user mengetik password tanpa bisa memverifikasi apa yang mereka ketik.

---

## 7. Responsive & Breakpoint

- **Mobile-first**: desain dan bangun dari layar terkecil dulu, lalu perbesar (progressive enhancement), bukan sebaliknya (graceful degradation dari desktop).
- **Breakpoint standar** yang umum dipakai: `640px` (mobile besar/small tablet), `768px` (tablet), `1024px` (laptop kecil), `1280px` (desktop).
- Yang **berubah** antar breakpoint bukan cuma ukuran, tapi juga pola interaksi:
  - Navigasi horizontal di desktop → berubah jadi drawer/bottom nav di mobile.
  - Hover state tidak ada gunanya di touch device — pastikan semua fungsi penting tidak bergantung pada hover saja.
  - Beberapa pattern desktop (multi-column table, tooltip on hover) perlu di-drop atau diganti pattern lain di mobile (misal table jadi card list).

---

## 8. Dark Mode / Theming

Dark mode **bukan sekadar inversi warna** dari light mode. Prinsip yang perlu dipegang:

- Gunakan konsep **surface/elevation** (permukaan makin terang saat makin "naik" secara elevasi), bukan mengandalkan shadow seperti di light mode — shadow nyaris tidak terlihat di atas background gelap.
- **Turunkan saturasi warna aksen** di dark mode — warna terang/saturated yang nyaman di light mode bisa terasa menyilaukan (vibrating) di atas background gelap.
- **Uji ulang rasio kontras** di dark mode secara terpisah — rasio yang lolos AA di light mode tidak otomatis lolos di kombinasi warna dark mode.
- Hindari pure black (`#000000`) untuk background utama — biasanya dark grey (`#121212` dsb.) lebih nyaman di mata dan membuat elevasi lebih terlihat.

---

## 9. Aksesibilitas & Inklusivitas

- Ukuran font minimum untuk body text: 14-16sp/px agar tetap terbaca tanpa zoom.
- Dukung dynamic type / text scaling tanpa merusak layout.
- Pastikan semua elemen interaktif dapat diakses via keyboard/screen reader (khusus web/Next.js: gunakan atribut ARIA yang sesuai).
- Sediakan **alt text** deskriptif untuk semua gambar informatif; gambar dekoratif diberi alt kosong (`alt=""`) agar screen reader melewatinya.
- Hindari flashing/blinking content yang bisa memicu photosensitive seizure.
- **Hormati `prefers-reduced-motion`**: pengguna dengan preferensi ini (termasuk yang punya vestibular disorder) bisa terganggu oleh animasi/transisi apa pun, bahkan yang easing-nya halus. Sediakan fallback tanpa motion atau motion minimal saat preferensi ini aktif.

---

## 10. Motion & Micro-interaction

- Durasi transisi standar: **200-300ms** untuk micro-interaction (tombol, toggle), **300-500ms** untuk transisi antar layar.
- Gunakan easing curve seperti `ease-in-out` atau `cubic-bezier` — hindari linear karena terasa kaku/robotic.
- Motion menjaga kontinuitas Gestalt saat elemen berpindah/muncul (misal: elemen yang di-tap "membesar" menjadi halaman baru, bukan tiba-tiba berganti).
- Gunakan motion secukupnya — motion berlebihan justru menambah beban kognitif dan terasa mengganggu.
- Selalu sediakan jalur tanpa motion untuk `prefers-reduced-motion` (lihat Bagian 9).

---

## 11. Loading, Empty, & Error State

Diperjelas dari Nielsen #1 (visibility of system status) menjadi aturan konkret:

- **Skeleton screen** lebih baik dari spinner untuk daftar/list konten — memberi gambaran struktur konten yang akan muncul, bukan cuma "sedang menunggu".
- **Optimistic UI** untuk aksi ringan (like, bookmark, toggle) — tampilkan hasil akhir seketika, lalu rollback diam-diam jika request gagal, agar terasa instan.
- **Empty state wajib punya CTA**, bukan cuma teks "Belum ada data" — beri aksi jelas untuk mengisi state tersebut (misal "Tambah item pertama").
- **Error state** harus menyertakan solusi/langkah selanjutnya, bukan hanya menyatakan bahwa terjadi error.

---

## 12. Microcopy

- Label tombol dimulai dengan **kata kerja** yang jelas ("Simpan Perubahan", bukan "OK" atau "Submit").
- Pesan error **tidak menyalahkan user** dan menyertakan solusi ("Email belum terdaftar. Coba daftar akun baru?" bukan "Error: invalid input").
- Gunakan **sentence case** untuk label/judul UI (bukan Title Case atau UPPERCASE) agar terasa lebih natural dibaca.
- Konsisten dengan istilah — jangan bergantian menyebut fitur yang sama dengan istilah berbeda di halaman berbeda.

---

## 13. Tipografi

- **Line-height**: ~1.5 untuk body text, ~1.2 untuk heading — di luar rentang ini keterbacaan menurun signifikan.
- **Panjang baris (line length)**: idealnya 45-75 karakter per baris untuk teks panjang — baris terlalu panjang membuat mata sulit menemukan baris berikutnya.
- Skala tipografi konsisten, contoh: 12/14/16/20/24/32px — hindari ukuran font acak per halaman.

---

## 14. Konsistensi Sistem — Nielsen's 10 Usability Heuristics

1. **Visibility of system status** — selalu beri feedback (loading indicator, progress bar, toast notification). Lihat Bagian 11 untuk detail konkret.
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

## 15. Design Tokens & Konsistensi Sistem

Untuk implementasi lintas platform (relevan untuk stack Flutter + Next.js):

- Definisikan **design tokens** terpusat: warna (primary/secondary/accent/semantic), spacing (kelipatan 8), radius, shadow, typography scale.
- Satu sumber kebenaran (single source of truth) agar konsisten di web dan mobile — hindari hardcode nilai berulang di tiap komponen.
- Terapkan skala tipografi yang konsisten (lihat Bagian 13).
- **Elevasi / z-index scale** — definisikan urutan lapisan secara eksplisit agar tidak tabrakan, contoh urutan naik: tooltip < dropdown < modal < toast/snackbar.

---

## 16. Platform Convention Divergence (Material vs Cupertino)

Relevan khusus untuk pengembangan mobile lintas platform (misal Flutter):

- Android (Material Design) dan iOS (Human Interface Guidelines/Cupertino) punya konvensi berbeda untuk: posisi & gaya back button, style switch/toggle, alert/dialog, animasi transisi antar halaman, dan style bottom sheet.
- Ada dua pendekatan sah: (1) **ikuti konvensi native tiap platform** (app terasa "native" di masing-masing OS, tapi butuh dua set komponen), atau (2) **satu gaya konsisten lintas platform** (lebih mudah maintain, tapi terasa kurang "native" di salah satu OS).
- Pilihan ini harus dinyatakan eksplisit di awal project — jangan campur aduk tanpa sengaja (misal back button Android tapi switch iOS-style).

---

## 17. Gesture & Safe Area (Mobile)

- **Gesture standar** — pakai konvensi yang sudah dikenal user: swipe-to-dismiss (menutup card/notification), pull-to-refresh (memuat ulang list), long-press (memunculkan context menu). Hindari menciptakan gesture custom untuk aksi yang sudah punya konvensi umum, karena melanggar Jakob's Law.
- **Safe area handling** — elemen penting (CTA, teks, navigasi) tidak boleh terpotong atau tertutup oleh notch, dynamic island, status bar, atau home indicator pada device modern. Selalu render di dalam safe area, bukan full-bleed untuk elemen interaktif.

---

## 18. Icon-Only Button Accessibility

- Tombol yang hanya berisi ikon tanpa label teks **wajib** punya `accessibilityLabel` (mobile) atau `aria-label` (web) — ikon sendirian sering ambigu maknanya walau sudah konsisten secara visual (Similarity dari Gestalt menjamin konsistensi, bukan kejelasan makna).
- Di web, tambahkan `title`/tooltip untuk ikon-only button agar pengguna mouse juga dapat konfirmasi visual atas fungsi tombol.

---

## 19. Perceived Performance

Berbeda dari loading state (Bagian 11) yang soal *tampilan saat menunggu* — ini soal *urutan render*:

- Tampilkan skeleton/placeholder secepat mungkin begitu navigasi terjadi, lalu isi konten secara progresif begitu data tersedia (progressive rendering) — jangan menunggu seluruh data siap baru merender semuanya sekaligus.
- Prioritaskan render konten above-the-fold lebih dulu.
- Pendekatan ini membuat aplikasi *terasa* lebih cepat meski total waktu loading sama.

---

## 20. Internasionalisasi (i18n) — Jika Relevan

Jika ada rencana multi-bahasa:

- Sediakan ruang untuk **text expansion** — teks dalam bahasa Indonesia/Jerman/dsb. bisa 30-50% lebih panjang dari bahasa Inggris untuk makna yang sama.
- Jangan hardcode lebar container/tombol berdasarkan panjang teks satu bahasa saja — gunakan lebar fleksibel/minimum, bukan fixed-width yang pas hanya untuk satu bahasa.
- Perhatikan format tanggal, angka, dan mata uang yang berbeda per lokal.

---

## 21. Search & Filter UX

Untuk fitur dengan data dalam jumlah besar:

- **Debounce** input search (misal 300-500ms setelah user berhenti mengetik) — jangan query ke server/database per-keystroke.
- Tampilkan **jumlah hasil** yang ditemukan agar user tahu seberapa luas/sempit pencarian mereka.
- Sediakan **"no results" state** dengan saran perbaikan (misal "coba kata kunci lain" atau tampilkan filter yang sedang aktif), bukan sekadar halaman kosong.

---

## Checklist Ringkas Sebelum Ship

- [ ] Rasio warna 60-30-10 terpenuhi, kontras teks memenuhi WCAG AA (4.5:1), non-text contrast ≥ 3:1
- [ ] Semua spacing mengikuti kelipatan 8-point grid
- [ ] Navigasi utama ≤ 5 item (Hukum Hick)
- [ ] Tap target ≥ 44x44px, jarak antar target ≥ 8px (Hukum Fitts)
- [ ] CTA & navigasi utama berada di thumb zone (mobile)
- [ ] Elemen interaktif punya gaya visual seragam (Similarity), dan punya semua state: hover/focus/pressed/disabled/loading
- [ ] Grouping informasi jelas via jarak/border (Proximity, Common Region)
- [ ] Form: label di atas field, validasi on-blur, error dekat field + solusi, autocomplete tepat
- [ ] Layout responsive dites di breakpoint 640/768/1024/1280, pattern hover tidak jadi satu-satunya jalur di mobile
- [ ] Dark mode diuji kontrasnya terpisah, tidak sekadar invert warna
- [ ] Status sistem selalu terlihat (skeleton untuk list, empty state dengan CTA, error state dengan solusi)
- [ ] Transisi/motion halus (200-300ms, easing non-linear), dan hormati `prefers-reduced-motion`
- [ ] Tidak mengandalkan warna saja untuk status (ada ikon/label pendukung), alt text tersedia untuk gambar
- [ ] Line-height ~1.5 body/~1.2 heading, panjang baris 45-75 karakter
- [ ] Design tokens & elevasi/z-index scale terdefinisi & konsisten lintas platform
- [ ] Kontras/spacing/ukuran diverifikasi dari nilai aktual di kode, bukan estimasi visual
- [ ] Konvensi platform (Material/Cupertino) dipilih secara sadar & konsisten, tidak tercampur tanpa sengaja
- [ ] Gesture standar dipakai (swipe/pull-to-refresh/long-press), elemen penting berada di dalam safe area
- [ ] Tombol icon-only punya `accessibilityLabel`/`aria-label`
- [ ] Konten dirender progresif (skeleton dulu, isi bertahap), bukan menunggu semua data siap
- [ ] Jika multi-bahasa: layout mengakomodasi text expansion, tidak fixed-width per bahasa
- [ ] Search di-debounce, tampilkan jumlah hasil, dan sediakan no-results state dengan saran
