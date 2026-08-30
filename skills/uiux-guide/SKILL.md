---
name: uiux-guide
description: Apply UI/UX design theory — 60-30-10 color proportions, 8-point grid, Gestalt principles, Hick/Fitts/Jakob/Miller laws, thumb zone, WCAG contrast, Nielsen's heuristics, design tokens — whenever creating, designing, building, or reviewing any user interface (screen, page, component, form, dashboard, landing page) in any framework (Flutter, Next.js, React, native). Use whenever the user asks to design or build a UI/layout/screen/component, or to review, critique, or fix an existing interface — phrasings like "review UI", "kenapa UI-nya terasa berantakan", "cek tampilannya", "rapikan layout", "buat halaman X", "desain screen Y", "buat form Z" — even if they never say "UI/UX". Also for questions about spacing, color, typography, motion, dark mode, responsive breakpoints, form validation, or accessibility decisions in a UI. For creating or tidying PRDs, use the prd and prd-refine skills instead.
---

# UI/UX Guide

Apply the UI/UX theory collected in `references/panduan-lengkap.md` (full guide: tables, examples, rationale) when building or reviewing interfaces. Two modes:

- **Design mode** — the user asks you to create something visual (page, screen, component, flow). Apply the rules below *while* constructing, not as an afterthought.
- **Review mode** — the user shows an existing UI (code, screenshot, spec) and wants critique or fixes. Audit it against the numbers table and the ship checklist, then report findings with evidence.

Language: respond in the user's language.

**Ukur, jangan kira-kira.** Jangan menilai kontras, spacing, atau ukuran elemen dari kesan visual. Hitung rasio kontras dari nilai hex aktual di kode/tema (bisa dihitung programatik), dan baca nilai px/spacing/font-size aktual langsung dari kode/CSS. Angka di bawah adalah ambang minimum yang bisa diverifikasi, bukan estimasi.

## Non-negotiable numbers

These thresholds come up in every task; apply them without being asked:

| Rule | Value |
|---|---|
| Color proportions (60-30-10) | 60% dominant (screen/backgrounds) · 30% secondary (cards, nav, supporting) · 10% accent (CTA, badges, alerts) — heuristik, boleh bergeser untuk brand tertentu (mis. fintech) |
| Text contrast (WCAG AA) | ≥ 4.5:1 normal text · ≥ 3:1 large text (≥18pt atau 14pt bold) |
| Non-text contrast (WCAG AA) | ≥ 3:1 untuk border input, ikon, dan batas komponen interaktif (1.4.11) — sering terlewat |
| Status encoding | Never color alone — always add an icon or text label (~8% of men are red-green colorblind) |
| Spacing | 8-point grid: 8/16/24/32/48 · group related items ~8px, separate topics ~32px (Proximity) |
| Tap targets | ≥ 44×44px (48×48 di Android) · ≥ 8px jarak antar target berdekatan · minimum resmi WCAG 2.2 sebenarnya 24×24 — pakai 44/48 karena lebih ketat |
| Primary navigation | ≤ 5 item (Hick) |
| Body text | 14–16px/sp minimum, dukung dynamic type / text scaling |
| Typography metrics | line-height ~1.5 body · ~1.2 heading · panjang baris 45–75 karakter |
| Motion | 200–300ms micro-interaction · 300–500ms transisi antar layar · easing `ease-in-out`/`cubic-bezier`, never linear · sediakan fallback untuk `prefers-reduced-motion` |
| Typography scale | 12/14/16/20/24/32px — jangan ukuran acak per halaman |

## Design mode

1. **Tokens first.** Before writing any component, define design tokens: color roles (primary/secondary/accent/semantic), spacing scale, radius, shadow, typography scale, dan z-index/elevation scale (urutan naik: tooltip < dropdown < modal < toast). One source of truth lintas platform (Flutter + Next.js) — jangan hardcode nilai berulang. Tanpa brand kit dari user, nyatakan asumsi token secara eksplisit (mis. "primary diasumsikan #2563EB karena tidak ada brand guideline") — jangan mengarang diam-diam.
2. **Compose on the 8-point grid.** All margins and padding are multiples of 8. Use spacing to group: dekat = satu kesatuan (Proximity), Common Region (card/border/background) saat jarak saja tidak cukup.
3. **Paint with 60-30-10.** Pick the dominant surface first, then secondary, then one accent reserved for actions you want noticed (Von Restorff: yang menonjol diingat dan diklik).
4. **Check the reading pattern.** Satu aksi utama (landing, onboarding) → pola Z, CTA mendarat di kanan bawah. Penuh konten (list, artikel, dashboard) → pola F; taruh item terpenting di awal/akhir list, bukan tengah (Serial Position).
5. **Place for thumbs (mobile).** CTA dan navigasi utama di zona jangkauan ibu jari (bawah-tengah); jangan taruh aksi kritis di pojok atas berlawanan tangan dominan. Elemen penting dan interaktif selalu di dalam safe area (notch, dynamic island, status bar, home indicator), bukan full-bleed.
6. **Stay familiar (Jakob).** Keranjang kanan-atas, hamburger menu, swipe-to-delete: pakai pola dan gesture standar (swipe-to-dismiss, pull-to-refresh, long-press) yang sudah dikenal pengguna; pola baru hanya dengan alasan kuat. Untuk mobile lintas platform, pilih sadar antara konvensi native per-OS (Material vs Cupertino) atau satu gaya konsisten lintas platform — nyatakan pilihannya, jangan tercampur tanpa sengaja.
7. **Respect the limits.** Nav ≤ 5 item; pecah form panjang jadi beberapa step (Miller 7±2); setiap elemen interaktif ≥ 44×44px dengan jarak ≥ 8px; semua yang bisa diklik seragam gayanya (Similarity).
8. **Define every interaction state.** Setiap elemen interaktif wajib punya definisi visual untuk: default, hover (hanya platform dengan pointer), focus (`focus-visible` — jangan pernah hapus outline focus demi estetika), pressed/active (feedback instan), disabled (tetap terlihat di alur), dan loading (disable untuk mencegah double-submit).
9. **Build forms right.** Label di atas field — placeholder bukan label; validasi on-blur, bukan per-keystroke; pesan error dekat field terkait dan menyertakan cara memperbaiki; `input type`/keyboard sesuai (`email`, `tel`, `number`); atribut `autocomplete` yang tepat; toggle show/hide password.
10. **Design mobile-first & responsive.** Bangun dari layar terkecil lalu perbesar; breakpoint umum 640/768/1024/1280. Yang berubah antar breakpoint adalah pola, bukan cuma ukuran: nav horizontal → drawer/bottom nav, table multi-kolom → card list, dan tidak ada fungsi penting yang hanya bisa lewat hover.
11. **Theme dark mode, don't invert.** Gunakan surface/elevation (makin "naik" makin terang), bukan shadow yang nyaris tak terlihat di background gelap; turunkan saturasi accent; uji ulang rasio kontras secara terpisah dari light mode; hindari pure black `#000000` untuk background utama.
12. **Show system status (Nielsen #1).** Skeleton > spinner untuk list; optimistic UI untuk aksi ringan (like, bookmark) dengan rollback diam-diam saat gagal; empty state wajib punya CTA; error state menyertakan solusi; render progresif — skeleton dulu, isi bertahap, prioritaskan above-the-fold. Cegah error daripada hanya melaporkannya: disable submit sebelum form valid, konfirmasi aksi destruktif, sediakan undo. Akhiri flow dengan momen memuaskan (Peak-End).
13. **Motion with intent.** Durasi dan easing dari tabel di atas; motion menjaga kontinuitas (card yang di-tap membesar menjadi halaman baru, bukan tiba-tiba berganti). Selalu sediakan jalur tanpa motion untuk `prefers-reduced-motion`. Motion yang sekadar dekorasi menambah beban kognitif — buang.
14. **Finish the details.** Keyboard/screen-reader access (ARIA sesuai kebutuhan), alt text deskriptif untuk gambar informatif dan `alt=""` untuk yang dekoratif, `aria-label`/`accessibilityLabel` untuk tombol icon-only, tanpa konten flashing. Microcopy: tombol dimulai kata kerja ("Simpan Perubahan", bukan "OK"), pesan error tidak menyalahkan user + menyertakan solusi, sentence case, istilah konsisten lintas halaman. Polish visual tetap penting (Aesthetic-Usability).

Area kondisional — multi-bahasa (sediakan ruang text expansion 30–50%, hindari fixed-width per bahasa) dan search/filter (debounce 300–500ms, tampilkan jumlah hasil, no-results state dengan saran): lihat Bagian 20–21 di `references/panduan-lengkap.md` saat menyentuhnya.

## Review mode

Audit the UI against the numbers table above and the ship checklist in `references/panduan-lengkap.md`. Verifikasi dari nilai aktual: hitung rasio kontras dari hex di kode/tema, dan baca px/spacing/font-size dari kode — jangan menilai dari kira-kira. Untuk review dari screenshot, tandai temuan yang tidak bisa diverifikasi dari kode sebagai perkiraan.

Then report:

1. **Findings first** — each with the rule broken, where (element/file/area screenshot), and a concrete fix: "padding 10px → 16px agar masuk grid 8-point", bukan "perbaiki spacing".
2. **Severity** — pelanggaran aksesibilitas (kontras teks & non-text, tap target, status warna-saja, outline focus dihilangkan, alt text/aria-label hilang) = blocking; proporsi warna, microcopy, dan motion = polish.
3. **What passes** — sebutkan juga yang sudah benar, agar user tahu apa yang jangan diubah.

Jangan menulis ulang seluruh UI kecuali diminta; ajukan perbaikan yang tertarget.

## Full reference

Untuk tabel lengkap — enam prinsip Gestalt, semua hukum kognitif (Hick, Fitts, Miller, Jakob, Von Restorff, Peak-End, Serial Position, Aesthetic-Usability) beserta implikasi desainnya, 10 heuristik Nielsen, pola baca Z/F, peta thumb zone, interaction states, form UX, responsive & breakpoint, dark mode/theming, konvensi platform Material vs Cupertino, gesture & safe area, icon-only button accessibility, perceived performance, i18n, search & filter UX, dan checklist ship — baca `references/panduan-lengkap.md`. Baca sebelum melakukan review UI yang non-trivial, atau saat mode desain menyentuh area yang tidak dicakup ringkasan di atas.
