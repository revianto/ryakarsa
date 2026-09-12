---
name: design-brief
description: Turn an approved PRD into a visual design brief — color philosophy, typography, and layout system grounded in the PRD's stated business goals and audience (not a generic template), split per screen/feature since different UI areas need different treatment, backed by researched real-world UI references (popular, stable, or cutting-edge design systems/products matching the determined mood), and checked against a genericism/AI-slop gate before finishing. Use when asked to "buat design brief dari PRD", "ubah PRD ke design brief", "tentukan filosofi warna/font/layout dari PRD ini", "cari referensi UI yang cocok untuk PRD ini" — even without the phrase "design brief". Not for interaction/behavior rules without visual identity (use uiux-guide's Standards mode for that), not for creating/tidying the PRD itself (use prd / prd-refine), and not for task backlogs (use prd-to-tasks).
---

# Design Brief

Ubah PRD yang sudah ada menjadi design brief visual — identitas visual (warna, tipografi, layout) yang berakar dari tujuan bisnis di PRD, bukan template generik.

Alurnya berurutan: **tahap 1** (baca PRD) → **1a/1b** (cek token & aset brand yang sudah ada) → **1c** (wawancara kebutuhan UI — wajib, jangan dilewati) → **2-5** (filosofi, pecah per area UI, riset referensi, slop check) → **6-7** (starter kit komponen/animasi, daftarkan ke `design-tokens`). Tahap 6-7 jalan otomatis setelah brief tersimpan, tidak perlu diminta terpisah.

## 1. Baca PRD, tarik sinyal desain

Baca PRD (path dari user, atau `./PRD.md` default). Sebelum menulis apapun, ekstrak dari PRD:
- Tujuan bisnis & metrik sukses (mis. conversion, retention, trust)
- Target audiens (demografi, tingkat literasi digital, konteks pakai — mobile-on-the-go vs desktop-fokus)
- **Positioning & brand tone** — PRD yang dibuat dengan template terbaru punya section khusus untuk ini (section 5: tone brand, tingkat eksklusivitas mass-market/mid/premium, kompetitor & pembeda); **baca itu dulu**. Kalau PRD-nya versi lama tanpa section itu, cari sinyalnya di Ringkasan Eksekutif/Latar Belakang — dan kalau tetap tidak ada, JANGAN mengarang; tandai "(perlu konfirmasi: brand personality tidak disebutkan di PRD)" dan tanyakan di tahap 1c.
- Daftar fitur/layar utama (jadi dasar pemecahan brief per kebutuhan UI di tahap 3)
- Kompetitor yang disebut (kalau ada, biasanya di section Positioning) — jadi acuan differensiasi, bukan ditiru
- Platform (web/mobile/keduanya) dan constraint teknis yang menyinggung UI (mis. harus offline-first, harus accessible)

Setiap keputusan desain nanti HARUS bisa ditarik balik ke salah satu poin di atas. Kalau PRD tidak cukup detail untuk sebuah keputusan (mis. tidak ada info demografi tapi brief butuh nada visual), tandai eksplisit sebagai asumsi/perlu konfirmasi — jangan diam-diam mengisi dengan default.

## 1a. Cek design system/token yang sudah ada

Sebelum masuk ke tahap filosofi, scan project (working directory saat ini) untuk tanda design system yang sudah dibangun di luar Claude — mis. dari Antigravity/tool lain yang FE-nya sudah di-ACC user:

- File token/config: `tailwind.config.*`, `design-tokens.json`, `theme.json`, CSS variables di `:root`/`globals.css`, `components.json` (shadcn), atau file style-guide lain.
- Kode FE yang sudah jalan (komponen dengan className/style konsisten) yang mengindikasikan warna/tipografi/spacing sudah diputuskan, bukan cuma di-scaffold.

**Kalau ditemukan** → masuk **mode extract**, bukan mode generate:
- Tahap 2 (filosofi) diganti: BACA nilai aktual dari token/CSS/config yang ada (hex warna, nama font, scale spacing/radius), lalu tulis filosofi sebagai REKONSTRUKSI kenapa pilihan itu masuk akal untuk tujuan bisnis di tahap 1 — bukan mengarang philosophy baru lalu memaksakan token baru. Kalau ada token yang TIDAK bisa dijelaskan alasannya dari sinyal PRD (mis. warna aksen yang tidak match tujuan bisnis), tandai eksplisit sebagai "(gap: token ini ada tapi tidak match sinyal PRD — perlu klarifikasi user)", jangan diam-diam dibenarkan.
- Tahap 3 (pecah per area UI) tetap jalan seperti biasa, tapi diikat ke pola yang SUDAH ada di kode FE, bukan usulan baru.
- Tahap 4 (riset referensi) tetap jalan, tapi fungsinya bergeser dari "cari arah" jadi "validasi" — apakah sistem yang sudah ada ini konsisten dengan pola matang di industri, sebutkan kalau ada penyimpangan yang berisiko (mis. kontras kurang, skala tipografi tidak sistematis).
- Tahap 5 (slop check) tetap jalan penuh.
- Di ringkasan penutup, sebutkan eksplisit: "Design brief ini didokumentasikan dari design system existing (sumber: [nama file/config yang terdeteksi]), bukan digenerate baru."

**Kalau tidak ditemukan** → lanjut mode generate seperti biasa (tahap 2 di bawah).

## 1b. Cek aset brand yang sudah ada

Terpisah dari 1a (token kode) — cek apakah ada aset brand resmi yang harus jadi **constraint keras**, bukan diusulkan ulang seolah masih terbuka: logo (`logo.*`, `*.svg`/`*.ai` di folder `brand/`, `assets/brand/`, `public/brand/`), brand guideline (`*brand-guideline*`, `*brand-book*`, PDF/Figma link yang disebut di PRD atau README).

- **Kalau ditemukan** (file lokal atau disebutkan user) → warna/font/logo dari situ jadi fondasi wajib di tahap 2, bukan pilihan filosofi dari nol. Filosofi tetap ditulis (kenapa aset ini cocok dengan tujuan bisnis tahap 1), tapi nilainya mengikuti aset, bukan sebaliknya.
- **Kalau tidak ditemukan lewat scan** → tanyakan langsung ke user di tahap 1c di bawah (jangan diam-diam asumsi belum ada, brand guideline sering hidup di luar repo — Figma, Google Drive, dsb).

## 1c. Wawancara kebutuhan UI — wajib sebelum menulis filosofi

Jangan langsung lanjut ke tahap 2 berdasarkan tebakan dari sinyal PRD saja. Tanyakan dulu lewat **AskUserQuestion** (fallback: daftar bernomor) — kategori produk yang beda butuh penekanan desain yang beda, jadi ini bukan basa-basi.

**Rekomendasi per pertanyaan**: tiap pertanyaan di bawah yang sudah punya sinyal dari tahap 1/1a/1b (tujuan bisnis, positioning, token/aset existing) taruh opsi itu di urutan pertama dengan suffix "(Recommended)" — jangan biarkan user memilih dari daftar kosong tanpa arah kalau sinyalnya sudah ada. Pertanyaan yang sinyalnya genuinely kosong (mis. level animasi kalau PRD tidak menyinggung motion sama sekali) tidak perlu dipaksakan rekomendasi.

1. **Prioritas UI produk ini** (skip pertanyaan ini kalau mode extract di 1a aktif — token existing sudah menjawabnya secara implisit):
   - **Estetika & motion** — produk brand-forward/consumer (portfolio, landing kreatif, produk lifestyle/hobi) di mana dampak visual dan animasi adalah bagian dari value proposition-nya sendiri.
   - **Layanan & kepercayaan** — produk B2B/fintech/kesehatan/jasa profesional di mana clarity, sinyal kredibilitas (testimoni, badge, angka konkret, proof), dan kemudahan mengambil keputusan lebih penting daripada motion — animasi jadi sekunder, bukan sorotan.
   - **Utility & efisiensi** — dashboard/tool internal di mana kepadatan informasi dan kecepatan scan lebih penting dari dua kategori di atas.
   - Kalau user tidak yakin, tawarkan tebakan dari sinyal tahap 1 (tujuan bisnis, audiens) dengan alasan konkret, tapi tetap minta konfirmasi eksplisit sebelum dipakai — jangan diam-diam dianggap disetujui.

2. **Kebutuhan blok konten UI** — elemen apa saja yang perlu didesain treatment-nya: CTA, carousel/slider, testimonial, pricing table, FAQ accordion, stat/angka besar, dll. Kalau user tidak yakin, tawarkan opsi "Claude yang rekomendasikan dari fitur-fitur di PRD" — tapi tetap sebutkan daftar rekomendasinya secara eksplisit untuk dikonfirmasi user, jangan diam-diam menambah blok yang tidak pernah disebut atau disetujui.

3. **Tingkat ornamen visual** — sumbu yang BERDIRI SENDIRI, jangan disamakan dengan poin 1 atau level animasi di poin 4: produk "layanan & kepercayaan" pun bisa sangat berornamen kalau positioning-nya eksklusif (private banking, wedding premium), sebaliknya produk "estetika & motion" bisa sengaja brutalis-polos. **Kalau PRD punya section "Positioning & Brand Tone"** (template PRD terbaru punya ini di section 5), tarik default-nya dari situ — mass-market → condong Polos/Sedang, premium-eksklusif → condong Kaya — lalu konfirmasi, jangan tanya dari nol. Opsi:
   - **Polos/utilitarian** — permukaan flat, tanpa gradient/tekstur/ornamen dekoratif; setiap elemen visual punya fungsi. Cocok untuk tool, dashboard, produk yang dipakai berjam-jam (ornamen jadi beban visual).
   - **Sedang** — aksen halus: shadow lembut, gradient tipis di satu-dua tempat, ilustrasi/ikon seperlunya. Default paling aman untuk kebanyakan produk consumer.
   - **Kaya/eksklusif** — ornamen dekoratif jadi bagian identitas: tekstur, foil/gradient, border dekoratif, ilustrasi custom, detail mewah. Dipakai kalau eksklusivitas/craft memang bagian dari yang dijual — bukan sekadar "biar cantik". Sebutkan konsekuensinya ke user: butuh aset visual nyata (ilustrasi/tekstur/foto custom) yang harus diproduksi atau digenerate terpisah, tidak cukup dari CSS saja.
   - Tingkat ini mengikat tahap 2 (terutama bullet *Surface treatment*) dan tahap 3 — jangan generate ornamen berat untuk yang pilih "Polos", dan jangan kasih hasil datar-polos kalau user pilih "Kaya".

4. **Level animasi** — tanyakan HANYA kalau animasi/motion relevan (prioritas "Estetika & motion" dari poin 1, atau PRD/user menyinggung interaksi-animasi meski kategorinya lain). Jangan tanya kalau prioritasnya "Utility & efisiensi" murni tanpa singgungan animasi sama sekali — skip diam-diam, jangan basa-basi. Opsi:
   - **Minimal** — animasi murni fungsional (feedback state: loading, disabled, sukses/gagal), tanpa polesan dekoratif. Cocok default untuk "Layanan & kepercayaan"/"Utility & efisiensi" kalau tetap butuh sedikit motion.
   - **Sedang** — ditambah entrance/scroll-reveal halus dan hover feedback (fade, scale kecil, slide singkat) — motion terasa tapi tidak jadi sorotan utama.
   - **Kaya/immersive** — motion jadi bagian dari storytelling: scroll-driven sequence (mis. video/image-sequence scrubbing ala Apple product page), orchestrated entrance, parallax, ambient motion. Butuh effort implementasi jauh lebih besar (lihat pembahasan GSAP+ScrollTrigger/video-scrub sebelumnya) — sebutkan trade-off effort ini ke user saat menawarkan opsi ini, jangan cuma menyebut nama levelnya.
   - Level ini menentukan seberapa jauh rekomendasi motion di tahap 2 dan starter kit animasi di tahap 6 (lihat di bawah) — jangan generate animasi "Kaya" kalau user pilih "Minimal", dan sebaliknya jangan kasih animasi seadanya kalau user eksplisit minta "Kaya".

5. **Referensi/inspirasi visual yang sudah ada** — apakah user sudah punya arah visual (link produk, nama brand, screenshot) yang ingin dijadikan acuan? Kalau ada, tahap 4 (riset referensi) berubah fungsi dari "cari dari nol" jadi "**nilai** referensi itu": dipakai penuh, dipakai sebagian, atau ditolak dengan alasan — bukan diabaikan lalu diganti pilihan sendiri diam-diam, tapi juga bukan diterima mentah-mentah tanpa dinilai (lihat tahap 4 untuk aturan vonisnya). Kalau user tidak punya referensi, tahap 4 tetap jalan seperti biasa (riset dari nol berdasarkan mood yang ditentukan di tahap 2).

6. **Target dark mode** — tanyakan eksplisit, jangan diasumsikan dari kategori produk. Opsi:
   - **Ya, sejak awal** — palet warna di tahap 2 WAJIB ditulis sebagai pasangan light/dark per peran warna (background, foreground, accent, dst.), bukan cuma light lalu dark ditambah belakangan — ini mengubah cara token ditulis sejak awal (semantic naming yang tahan banting, bukan hex tunggal).
   - **Tidak** — produk sengaja satu visual world (lihat contoh `undangoo-landing` yang sengaja light-only dengan satu spread gelap sebagai bagian dari identitas, bukan mode terpisah) — boleh pakai warna literal tanpa pasangan dark, tandai eksplisit di brief bahwa ini keputusan sadar.
   - **Nanti/belum tahu** — desain light dulu, tapi tetap strukturkan token dengan semantic naming (bukan nama warna mentah) supaya varian dark gampang ditambah belakangan tanpa rombak total.
   - Jawaban ini menentukan struktur token warna di tahap 2 dan format `tokens.json` kalau nanti didaftarkan ke `design-tokens` (lihat tahap 7).

Keenam jawaban ini mengikat tahap 2-4 di bawah — jangan mulai menulis filosofi sebelum semuanya dikonfirmasi user.

## 2. Tentukan filosofi (bukan cuma pilihan)

Untuk tiga elemen inti, tulis ALASAN dulu baru pilihan — filosofi, bukan daftar token kosong. Jawaban prioritas UI dari tahap 1c (estetika & motion / layanan & kepercayaan / utility & efisiensi) menentukan bobot tiap elemen di bawah — sebutkan eksplisit di brief prioritas mana yang dipakai dan kenapa:

- **Warna**: mood apa yang harus dibawa warna ini untuk mencapai tujuan bisnis (mis. "trust + calm" untuk fintech consumer, "urgency + energy" untuk flash-sale e-commerce)? Baru turunkan ke arah palet (warm/cool, saturated/muted, monokromatik/kontras tinggi) dan proporsi 60-30-10 (lihat `uiux-guide` untuk rasionya). Beri 1 palet konkret sebagai starting point (nama warna + peran, belum harus hex final) dengan alasan tiap pilihan diikat ke poin di tahap 1. Untuk prioritas "layanan & kepercayaan", condongkan ke palet lebih restrained/muted dengan warna aksen dipakai hemat untuk sinyal kepercayaan (bukan dekorasi); untuk "estetika & motion", palet boleh lebih berani/kontras tinggi karena warna ikut jadi bagian dari daya tarik.
- **Surface treatment** (cara warna itu dipasang ke permukaan komponen, bukan cuma nilai warnanya): tentukan default di sini — solid fill, outline/border-only, ghost (transparan sampai hover), glass/translucent, atau ada highlight tambahan (shine/gloss di tepi atas, gradient tipis, inner glow). Ini keputusan filosofis, bukan detail teknis nanti: "shiny highlight" biasanya menyiratkan premium/tactile, "outline tipis" menyiratkan restrained/tidak memaksa, "solid flat tanpa efek" menyiratkan utilitarian/jelas. Ikat ke prioritas UI tahap 1c yang sama — "estetika & motion" boleh punya treatment lebih kaya (shine, gradient), "layanan & kepercayaan"/"utility & efisiensi" biasanya lebih aman di flat/outline supaya tidak terlihat murah atau mengalihkan perhatian dari isi. Sebutkan treatment default untuk minimal CTA primer & sekunder di sini — detail per-komponen lain menyusul di tahap 3.
- **Tipografi**: apa yang dibutuhkan dari tipe huruf ini — keterbacaan tinggi untuk data-dense app? kepribadian kuat untuk brand-forward landing page? Tentukan arah (grotesque/humanist/serif/display) dulu, baru nama font kalau alasannya sudah jelas.
- **Layout**: kepadatan informasi apa yang sesuai (dashboard padat vs marketing lapang), pola grid, dan ritme visual (whitespace generous vs compact) — diikat ke konteks pakai dari tahap 1 (mis. "dipakai sambil jalan → informasi utama harus scannable dalam <3 detik").
- **Motion**: turunkan langsung dari level animasi yang dikonfirmasi di tahap 1c (Minimal/Sedang/Kaya), jangan tentukan ulang dari nol di sini. Untuk "Kaya", jabarkan arah motion konkret (entrance sequence, scroll-driven section mana yang jadi showcase, ambient motion) sebagai bagian dari filosofi inti, bukan sekadar polesan di tahap 6. Untuk "Sedang", cukup sebutkan pola umum (scroll-reveal halus, hover feedback). Untuk "Minimal", sebutkan eksplisit bahwa motion dibatasi ke feedback state saja — supaya tahap 6 tidak generate animasi dekoratif yang tidak diminta.

## 3. Pecah brief sesuai kebutuhan UI

Jangan tulis satu brief seragam untuk seluruh produk. Setelah fondasi (warna/tipografi/layout system) di tahap 2 ditetapkan sebagai satu sumber kebenaran, terapkan ke tiap area UI utama dari daftar fitur/layar di tahap 1 secara terpisah — tiap area dapat sub-bagian sendiri yang menjelaskan:

- Bagaimana fondasi diterapkan di sini secara spesifik (mis. dashboard: aksen warna hanya untuk status/alert, angka pakai tabular figures; landing page: aksen warna dipakai lebih bebas untuk CTA, ukuran display type lebih besar)
- Kebutuhan yang unik untuk area ini yang tidak berlaku di area lain (mis. checkout butuh trust signal visual ekstra, onboarding butuh progress indicator)
- Treatment spesifik untuk tiap blok konten yang dikonfirmasi di tahap 1c (CTA, carousel, testimonial, pricing table, dll) yang relevan di area ini — jelaskan posisi, gaya, dan alasan pakai fondasi tahap 2, bukan cuma menyebut nama bloknya. Untuk elemen interaktif (button, chip, badge, input) sebutkan surface treatment-nya eksplisit (solid/outline/ghost/shine, dst. — turunan dari tahap 2), termasuk kalau beda dari default global (mis. CTA di dalam pricing card populer boleh dapat treatment lebih menonjol daripada CTA biasa di tempat lain) — jangan biarkan ini diam-diam ditebak nanti saat komponennya dibuat.

Area yang tidak relevan (mis. PRD tidak menyebut mobile app) di-skip, jangan dipaksakan.

## 4. Riset referensi UI nyata — bukan istilah kosong

**Kalau user sudah kasih referensi/inspirasi di tahap 1c** — jangan cari dari nol, tapi **jangan juga terima mentah-mentah**. Buka/analisis referensi yang diberikan (link, screenshot, atau nama produk yang disebut), lalu **nilai kecocokannya secara eksplisit** terhadap sinyal tahap 1 (tujuan bisnis, audiens, positioning) dan filosofi tahap 2 — bukan sekadar mengelaborasi apa yang sudah ada di situ.

Tiap referensi user wajib dapat salah satu dari tiga vonis, ditulis terus terang di brief:

- **Cocok penuh** — arah visualnya memang pas untuk produk ini. Sebutkan pola spesifik apa yang diambil dan kenapa, seperti riset biasa di bawah.
- **Cocok sebagian** (paling sering terjadi) — sebutkan **bagian mana yang dipakai** (mis. "struktur navigasi dan cara mereka handle empty state") dan **bagian mana yang sengaja TIDAK dipakai** beserta alasannya yang ditarik ke tahap 1-2 (mis. "palet high-contrast neon mereka tidak dipakai — audiens produk ini 40+ dan konteks pakainya di luar ruangan, kontras ekstrem itu melelahkan; ambil struktur layout-nya saja, warnanya tetap dari filosofi tahap 2").
- **Tidak cocok** — katakan langsung, jangan dipaksakan supaya terlihat akomodatif. Jelaskan benturannya secara konkret (mis. "referensi ini dashboard data-dense, sedangkan produk ini marketing site yang butuh satu aksi dominan per layar — meniru kepadatannya akan mengubur CTA"), lalu tawarkan 1-2 alternatif yang mendekati *maksud* user di balik referensi itu. Tanya balik apa yang sebenarnya menarik dari referensi tersebut — sering yang dia suka cuma satu aspek (mis. "rasanya mahal"), bukan keseluruhan eksekusinya.

**Jangan mengarang keberatan** demi terlihat kritis: kalau referensinya memang cocok, bilang cocok. Yang dilarang itu menerima tanpa dinilai, bukan menyetujui. Boleh validasi dengan 0-2 referensi tambahan sebagai pembanding kalau perlu.

**Kalau user tidak punya referensi** — cari referensi UI nyata yang cocok dengan mood dari tahap 2 lewat pencarian web:

- Cari yang **populer** (dipakai luas, dikenal), **stabil** (design system matang, bukan tren yang keburu basi), atau **terbaru** (tren desain yang sedang relevan dengan mood ini) — sebutkan mana dari tiga kategori ini tiap referensi masuk.
- Prioritaskan design system/produk konkret yang bisa disebut namanya (mis. shadcn/ui, Radix, Material 3, Linear, Stripe Dashboard, Untitled UI) dibanding istilah genre kosong ("modern minimalist").
- Untuk tiap referensi: sebutkan APA yang relevan diambil (pola spesifik — card elevation, cara mereka handle empty state, skala tipografi) dan KENAPA itu cocok dengan mood/tujuan dari tahap 1-2 — bukan sekadar link-dump.
- 2-4 referensi cukup; kedalaman lebih penting dari jumlah.

## 5. Slop check — wajib sebelum output final

Sebelum menyimpan file, audit brief sendiri terhadap tanda-tanda AI slop, revisi kalau kena:

- **Traceability**: acak 3 keputusan desain di brief — bisakah masing-masing ditunjuk balik ke baris spesifik di PRD (tahap 1)? Kalau jawabannya "itu cuma best-practice umum" tanpa kaitan ke PRD ini, itu tanda generik — perkuat atau buang.
- **Klise default**: waspada pola default AI — Inter/Poppins + gradient ungu-ke-biru + rounded-2xl card + "clean and modern" tanpa spesifik. Kalau brief ini bisa langsung dipakai untuk produk lain tanpa mengubah kata apapun, itu terlalu generik — persempit sampai spesifik ke produk ini.
- **Bahasa kosong**: cari kata sifat tanpa isi ("seamless", "intuitive", "sleek", "modern") yang tidak diikuti definisi konkret (angka, contoh, mekanisme) — ganti atau hapus.
- **Asumsi diam-diam**: pastikan semua tebakan (brand personality, warna belum dikonfirmasi, dst.) ditandai eksplisit "(asumsi)"/"(perlu konfirmasi)", bukan ditulis seolah fakta dari PRD.
- **Referensi user dinilai, bukan dirasionalisasi**: kalau user memberi referensi di tahap 1c, cek apakah brief ini benar-benar memberi vonis (cocok penuh / cocok sebagian dengan bagian yang ditolak disebutkan / tidak cocok), atau cuma menjelaskan ulang isi referensi itu dengan bahasa yang lebih meyakinkan. Kalau semua referensi user kebetulan "cocok penuh" tanpa satupun catatan, curigai diri sendiri — periksa ulang apakah memang begitu atau kamu sedang menghindari ketidaksetujuan.

## Output

Tulis ke `./DESIGN-BRIEF.md` kecuali user sebut path lain. Kalau file itu sudah ada, backup dulu ke `DESIGN-BRIEF_old.md` sebelum menimpa — jangan menimpa diam-diam.

## 6. Auto-generate starter kit (component-library + animation-library)

Setelah `DESIGN-BRIEF.md` tersimpan, lanjutkan otomatis — jangan berhenti dan menunggu user memintanya secara terpisah. Turunkan starter kit dasar dari filosofi yang baru ditetapkan di tahap 2, bukan generate ulang seluruh brief.

**Kecuali mode extract (tahap 1a) dan FE existing sudah punya komponen button/card/nav yang jalan** — skip starter kit ini sepenuhnya (jangan generate ulang yang sudah ada), sebutkan di ringkasan penutup bahwa starter kit dilewati karena komponen setara sudah ada di FE existing. Kalau mode extract tapi FE existing belum punya salah satu dari ketiga komponen itu, tetap generate yang hilang saja (bukan ketiganya).

- **3 komponen** lewat `component-library` (alur "tambah dari deskripsi teks"): primary button, card dasar, nav/header. Deskripsi yang dikirim ke skill itu HARUS mengutip filosofi warna/tipografi/layout dari brief ini (mis. "button primer, warna aksen [X] dari brief, radius sesuai arah layout [Y]"), bukan deskripsi generik — **dan HARUS menyebutkan surface treatment eksplisit dari tahap 2/3** (solid fill, outline, shine/highlight, dst. — bukan cuma "warna X", karena "warna X sebagai solid fill" dan "warna X cuma di border" adalah dua komponen yang sangat berbeda). Kalau tahap 2/3 belum cukup spesifik soal treatment untuk salah satu dari ketiga komponen ini, putuskan di sini berdasar filosofi yang sudah ada (jangan default ke solid fill begitu saja) dan sebutkan alasannya singkat di ringkasan penutup.
- **2 animasi** lewat `animation-library`, disesuaikan level animasi dari tahap 1c: satu entrance/fade yang cocok dengan ritme visual brief (whitespace generous → transisi lebih lambat/lembut; compact/dashboard → cepat/snappy), satu hover/interaction feedback yang cocok dengan tone (playful → bounce halus; professional/trust → fade/scale halus). Untuk level **Minimal**, kedua entry ini tetap dibuat tapi versi paling ringan/singkat (feedback state saja, bukan showcase). Untuk level **Kaya**, sebutkan di ringkasan penutup bahwa starter kit 2 animasi ini cuma basic default — motion showcase sesungguhnya (scroll-driven sequence, orchestrated entrance) perlu dibangun manual lewat `animation-library`/kode langsung saat user memang memintanya, bukan otomatis dari sini.
- **Penamaan**: prefix nama produk dari PRD ke setiap nama entry (mis. `acme-btn-primary`, bukan `btn-primary`) supaya tidak bentrok atau ketiban entry dari brief produk lain.
- **Source**: tandai `prompt` seperti alur normal kedua skill itu.
- **Fallback**: kalau `component-library` atau `animation-library` tidak terpasang di environment ini, skip bagian itu saja secara diam-diam (jangan gagalkan design-brief), dan sebutkan di ringkasan penutup bahwa bagian itu dilewati.
- Ini starter kit dasar (5 item), BUKAN generate komponen untuk tiap layar/fitur di PRD — jangan diperluas lebih dari itu di sini; komponen spesifik per layar tetap dibuat manual lewat `component-library` saat user memang memintanya nanti.

**Cek React Bits (kondisional, bukan default)**: hanya pertimbangkan kalau DUA syarat ini terpenuhi —
1. Stack-nya React/Next.js (disebutkan eksplisit di PRD, atau terdeteksi dari `package.json`/`components.json` di project saat ini)
2. Brief ini butuh visual motion-heavy (landing page, hero section, scroll-reveal, background animasi) — BUKAN untuk dashboard padat/utility app

Kalau dua syarat itu terpenuhi: sebut di brief (bagian riset referensi atau starter kit) rekomendasi komponen React Bits (reactbits.dev) yang cocok dengan mood — mis. background animasi untuk hero, fade-on-scroll untuk section reveal — sebagai alternatif ke entry `animation-library` buatan tangan untuk kebutuhan itu spesifik. **Jangan auto-install** — ini cuma rekomendasi tertulis; pemasangan registry `@react-bits` ke `components.json` project (lihat memory `reference-react-bits-mcp`) tetap harus dikonfirmasi user dulu karena mengubah config project. Kalau salah satu syarat tidak terpenuhi, jangan sebut React Bits sama sekali — jangan dipaksakan.

## 7. Daftarkan ke `design-tokens` (kalau skill itu terpasang)

Setelah tahap 6 selesai, lanjutkan otomatis (sama seperti tahap 6, jangan berhenti menunggu diminta terpisah) — **kecuali** skill `design-tokens` tidak terpasang di environment ini, atau mode extract (tahap 1a) aktif dan design system yang sesuai sudah terdaftar di library-nya (cek dulu lewat `list`/`get` sebelum menambah — jangan duplikat).

1. Turunkan `tokens.json` langsung dari filosofi tahap 2 — bukan menulis ulang dari nol: warna (primitive+semantic, ikuti keputusan dark-mode dari tahap 1c — pasangan light/dark per peran kalau user pilih "Ya"/"Nanti", literal tunggal kalau pilih "Tidak" dan ditandai sebagai keputusan sadar seperti contoh `undangoo-landing`), tipografi (fontFamily/scale/weight dari tahap 2), spacing/radius/shadow/breakpoint/motion kalau brief menyebutkannya secara spesifik (jangan mengarang angka yang tidak ada di brief — kosongkan kategori itu kalau memang belum diputuskan, ikuti pola `spacingUsage`/`breakpointUsage` notes-only di skill `design-tokens` untuk kategori yang belum ada nilainya).
2. Daftarkan lewat `manage_library.py add --name <nama-produk-dari-PRD> --description "..." --source prompt` (skill `design-brief` yang jadi sumbernya, jadi `prompt` bukan `code`/`design`), lalu isi `tokens.json` hasil turunan itu.
3. Kalau user punya viewer design system yang sudah dipublish sebelumnya (mis. artifact seperti System Shelf) — ikuti alur "jaga viewer tetap sinkron" yang sudah ada di `SKILL.md` skill `design-tokens` (alur #7 di skill itu): update data grup dan republish ke URL yang sama. Kalau belum ada viewer sama sekali, jangan bikin baru inisiatif sendiri di sini — cukup sebutkan di ringkasan penutup bahwa design system sudah terdaftar di library dan viewer bisa dibuat kalau diminta.
4. **Fallback**: kalau `design-tokens` tidak terpasang, skip tahap ini secara diam-diam (jangan gagalkan design-brief), sebutkan di ringkasan penutup bahwa bagian ini dilewati.

Tutup dengan ringkasan ≤9 baris: path file brief, filosofi inti (1 kalimat warna+tipografi+layout), berapa area UI yang di-cover, berapa referensi riset dipakai, berapa item "(perlu konfirmasi)" yang tersisa, daftar nama komponen/animasi yang berhasil dibuat (atau catatan kalau di-skip), kalau relevan — rekomendasi React Bits yang disebutkan, dan status pendaftaran ke `design-tokens` (nama design system yang terdaftar, atau catatan kalau dilewati).

## Handoff

- Belum ada PRD: `prd` untuk bikin dari ide mentah, `prd-refine` untuk merapikan yang sudah ada.
- Setelah design brief ini ada, `component-library` & `animation-library` otomatis terpicu untuk starter kit dasar (lihat tahap 6) — tidak perlu diminta terpisah. `design-tokens` juga otomatis terpicu (lihat tahap 7) untuk mendaftarkan design system-nya supaya bisa dipakai ulang di project lain.
- Penerapan lanjutan ke UI nyata (komponen lain, halaman penuh) pakai `uiux-guide` Design mode — brief ini kasih arah visual, `uiux-guide` kasih aturan teknis penerapannya (kontras, grid, tap target, dst.).
- Butuh dokumen behavior/interaction standard tanpa identitas visual (bukan ini): `uiux-guide` Standards mode.
- Butuh breakdown task/test-case dari PRD, bukan desain: `prd-to-tasks`.
