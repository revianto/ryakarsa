---
name: design-brief
description: Turn an approved PRD into a visual design brief — color philosophy, typography, and layout system grounded in the PRD's stated business goals and audience (not a generic template), split per screen/feature since different UI areas need different treatment, backed by researched real-world UI references (popular, stable, or cutting-edge design systems/products matching the determined mood), and checked against a genericism/AI-slop gate before finishing. Use when asked to "buat design brief dari PRD", "ubah PRD ke design brief", "tentukan filosofi warna/font/layout dari PRD ini", "cari referensi UI yang cocok untuk PRD ini" — even without the phrase "design brief". Not for interaction/behavior rules without visual identity (use uiux-guide's Standards mode for that), not for creating/tidying the PRD itself (use prd / prd-refine), and not for task backlogs (use prd-to-tasks).
---

# Design Brief

Ubah PRD yang sudah ada menjadi design brief visual — identitas visual (warna, tipografi, layout) yang berakar dari tujuan bisnis di PRD, bukan template generik. Lima tahap wajib, berurutan.

## 1. Baca PRD, tarik sinyal desain

Baca PRD (path dari user, atau `./PRD.md` default). Sebelum menulis apapun, ekstrak dari PRD:
- Tujuan bisnis & metrik sukses (mis. conversion, retention, trust)
- Target audiens (demografi, tingkat literasi digital, konteks pakai — mobile-on-the-go vs desktop-fokus)
- Personality/tone brand kalau disebutkan (playful, professional, luxury, dst.) — kalau tidak disebutkan, JANGAN mengarang; tandai "(perlu konfirmasi: brand personality tidak disebutkan di PRD)"
- Daftar fitur/layar utama (jadi dasar pemecahan brief per kebutuhan UI di tahap 3)
- Kompetitor yang disebut (kalau ada) — jadi acuan differensiasi, bukan ditiru
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

## 2. Tentukan filosofi (bukan cuma pilihan)

Untuk tiga elemen inti, tulis ALASAN dulu baru pilihan — filosofi, bukan daftar token kosong:

- **Warna**: mood apa yang harus dibawa warna ini untuk mencapai tujuan bisnis (mis. "trust + calm" untuk fintech consumer, "urgency + energy" untuk flash-sale e-commerce)? Baru turunkan ke arah palet (warm/cool, saturated/muted, monokromatik/kontras tinggi) dan proporsi 60-30-10 (lihat `uiux-guide` untuk rasionya). Beri 1 palet konkret sebagai starting point (nama warna + peran, belum harus hex final) dengan alasan tiap pilihan diikat ke poin di tahap 1.
- **Tipografi**: apa yang dibutuhkan dari tipe huruf ini — keterbacaan tinggi untuk data-dense app? kepribadian kuat untuk brand-forward landing page? Tentukan arah (grotesque/humanist/serif/display) dulu, baru nama font kalau alasannya sudah jelas.
- **Layout**: kepadatan informasi apa yang sesuai (dashboard padat vs marketing lapang), pola grid, dan ritme visual (whitespace generous vs compact) — diikat ke konteks pakai dari tahap 1 (mis. "dipakai sambil jalan → informasi utama harus scannable dalam <3 detik").

## 3. Pecah brief sesuai kebutuhan UI

Jangan tulis satu brief seragam untuk seluruh produk. Setelah fondasi (warna/tipografi/layout system) di tahap 2 ditetapkan sebagai satu sumber kebenaran, terapkan ke tiap area UI utama dari daftar fitur/layar di tahap 1 secara terpisah — tiap area dapat sub-bagian sendiri yang menjelaskan:

- Bagaimana fondasi diterapkan di sini secara spesifik (mis. dashboard: aksen warna hanya untuk status/alert, angka pakai tabular figures; landing page: aksen warna dipakai lebih bebas untuk CTA, ukuran display type lebih besar)
- Kebutuhan yang unik untuk area ini yang tidak berlaku di area lain (mis. checkout butuh trust signal visual ekstra, onboarding butuh progress indicator)

Area yang tidak relevan (mis. PRD tidak menyebut mobile app) di-skip, jangan dipaksakan.

## 4. Riset referensi UI nyata — bukan istilah kosong

Sebelum finalisasi, cari referensi UI nyata yang cocok dengan mood dari tahap 2 lewat pencarian web:

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

## Output

Tulis ke `./DESIGN-BRIEF.md` kecuali user sebut path lain. Kalau file itu sudah ada, backup dulu ke `DESIGN-BRIEF_old.md` sebelum menimpa — jangan menimpa diam-diam.

## 6. Auto-generate starter kit (component-library + animation-library)

Setelah `DESIGN-BRIEF.md` tersimpan, lanjutkan otomatis — jangan berhenti dan menunggu user memintanya secara terpisah. Turunkan starter kit dasar dari filosofi yang baru ditetapkan di tahap 2, bukan generate ulang seluruh brief.

**Kecuali mode extract (tahap 1a) dan FE existing sudah punya komponen button/card/nav yang jalan** — skip starter kit ini sepenuhnya (jangan generate ulang yang sudah ada), sebutkan di ringkasan penutup bahwa starter kit dilewati karena komponen setara sudah ada di FE existing. Kalau mode extract tapi FE existing belum punya salah satu dari ketiga komponen itu, tetap generate yang hilang saja (bukan ketiganya).

- **3 komponen** lewat `component-library` (alur "tambah dari deskripsi teks"): primary button, card dasar, nav/header. Deskripsi yang dikirim ke skill itu HARUS mengutip filosofi warna/tipografi/layout dari brief ini (mis. "button primer, warna aksen [X] dari brief, radius sesuai arah layout [Y]"), bukan deskripsi generik.
- **2 animasi** lewat `animation-library`: satu entrance/fade yang cocok dengan ritme visual brief (whitespace generous → transisi lebih lambat/lembut; compact/dashboard → cepat/snappy), satu hover/interaction feedback yang cocok dengan tone (playful → bounce halus; professional/trust → fade/scale halus).
- **Penamaan**: prefix nama produk dari PRD ke setiap nama entry (mis. `acme-btn-primary`, bukan `btn-primary`) supaya tidak bentrok atau ketiban entry dari brief produk lain.
- **Source**: tandai `prompt` seperti alur normal kedua skill itu.
- **Fallback**: kalau `component-library` atau `animation-library` tidak terpasang di environment ini, skip bagian itu saja secara diam-diam (jangan gagalkan design-brief), dan sebutkan di ringkasan penutup bahwa bagian itu dilewati.
- Ini starter kit dasar (5 item), BUKAN generate komponen untuk tiap layar/fitur di PRD — jangan diperluas lebih dari itu di sini; komponen spesifik per layar tetap dibuat manual lewat `component-library` saat user memang memintanya nanti.

**Cek React Bits (kondisional, bukan default)**: hanya pertimbangkan kalau DUA syarat ini terpenuhi —
1. Stack-nya React/Next.js (disebutkan eksplisit di PRD, atau terdeteksi dari `package.json`/`components.json` di project saat ini)
2. Brief ini butuh visual motion-heavy (landing page, hero section, scroll-reveal, background animasi) — BUKAN untuk dashboard padat/utility app

Kalau dua syarat itu terpenuhi: sebut di brief (bagian riset referensi atau starter kit) rekomendasi komponen React Bits (reactbits.dev) yang cocok dengan mood — mis. background animasi untuk hero, fade-on-scroll untuk section reveal — sebagai alternatif ke entry `animation-library` buatan tangan untuk kebutuhan itu spesifik. **Jangan auto-install** — ini cuma rekomendasi tertulis; pemasangan registry `@react-bits` ke `components.json` project (lihat memory `reference-react-bits-mcp`) tetap harus dikonfirmasi user dulu karena mengubah config project. Kalau salah satu syarat tidak terpenuhi, jangan sebut React Bits sama sekali — jangan dipaksakan.

Tutup dengan ringkasan ≤8 baris: path file brief, filosofi inti (1 kalimat warna+tipografi+layout), berapa area UI yang di-cover, berapa referensi riset dipakai, berapa item "(perlu konfirmasi)" yang tersisa, daftar nama komponen/animasi yang berhasil dibuat (atau catatan kalau di-skip), dan kalau relevan — rekomendasi React Bits yang disebutkan.

## Handoff

- Belum ada PRD: `prd` untuk bikin dari ide mentah, `prd-refine` untuk merapikan yang sudah ada.
- Setelah design brief ini ada, `component-library` & `animation-library` otomatis terpicu untuk starter kit dasar (lihat tahap 6) — tidak perlu diminta terpisah.
- Penerapan lanjutan ke UI nyata (komponen lain, halaman penuh) pakai `uiux-guide` Design mode — brief ini kasih arah visual, `uiux-guide` kasih aturan teknis penerapannya (kontras, grid, tap target, dst.).
- Butuh dokumen behavior/interaction standard tanpa identitas visual (bukan ini): `uiux-guide` Standards mode.
- Butuh breakdown task/test-case dari PRD, bukan desain: `prd-to-tasks`.
