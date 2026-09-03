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

Tulis ke `./DESIGN-BRIEF.md` kecuali user sebut path lain. Kalau file itu sudah ada, backup dulu ke `DESIGN-BRIEF_old.md` sebelum menimpa — jangan menimpa diam-diam. Tutup dengan ringkasan ≤6 baris: path file, filosofi inti (1 kalimat warna+tipografi+layout), berapa area UI yang di-cover, berapa referensi riset dipakai, dan berapa item "(perlu konfirmasi)" yang tersisa.

## Handoff

- Belum ada PRD: `prd` untuk bikin dari ide mentah, `prd-refine` untuk merapikan yang sudah ada.
- Setelah design brief ini ada, penerapan ke UI nyata (komponen, halaman) pakai `uiux-guide` Design mode — brief ini kasih arah visual, `uiux-guide` kasih aturan teknis penerapannya (kontras, grid, tap target, dst.).
- Butuh dokumen behavior/interaction standard tanpa identitas visual (bukan ini): `uiux-guide` Standards mode.
- Butuh breakdown task/test-case dari PRD, bukan desain: `prd-to-tasks`.
