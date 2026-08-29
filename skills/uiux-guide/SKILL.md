---
name: uiux-guide
description: Apply UI/UX design theory — 60-30-10 color proportions, 8-point grid, Gestalt principles, Hick/Fitts/Jakob/Miller laws, thumb zone, WCAG contrast, Nielsen's heuristics, design tokens — whenever creating, designing, building, or reviewing any user interface (screen, page, component, form, dashboard, landing page) in any framework (Flutter, Next.js, React, native). Use whenever the user asks to design or build a UI/layout/screen/component, or to review, critique, or fix an existing interface — phrasings like "review UI", "kenapa UI-nya terasa berantakan", "cek tampilannya", "rapikan layout", "buat halaman X", "desain screen Y" — even if they never say "UI/UX". Also for questions about spacing, color, typography, motion, or accessibility decisions in a UI. For creating or tidying PRDs, use the prd and prd-refine skills instead.
---

# UI/UX Guide

Apply the UI/UX theory collected in `references/panduan-lengkap.md` (full guide: tables, examples, rationale) when building or reviewing interfaces. Two modes:

- **Design mode** — the user asks you to create something visual (page, screen, component, flow). Apply the rules below *while* constructing, not as an afterthought.
- **Review mode** — the user shows an existing UI (code, screenshot, spec) and wants critique or fixes. Audit it against the numbers table and the ship checklist, then report findings with evidence.

Language: respond in the user's language.

## Non-negotiable numbers

These thresholds come up in every task; apply them without being asked:

| Rule | Value |
|---|---|
| Color proportions (60-30-10) | 60% dominant (screen/backgrounds) · 30% secondary (cards, nav, supporting) · 10% accent (CTA, badges, alerts) — heuristik, boleh bergeser untuk brand tertentu (mis. fintech) |
| Text contrast (WCAG AA) | ≥ 4.5:1 normal text · ≥ 3:1 large text (≥18pt atau 14pt bold) |
| Status encoding | Never color alone — always add an icon or text label (~8% of men are red-green colorblind) |
| Spacing | 8-point grid: 8/16/24/32/48 · group related items ~8px, separate topics ~32px (Proximity) |
| Tap targets | ≥ 44×44px (48×48 di Android) · ≥ 8px jarak antar target berdekatan |
| Primary navigation | ≤ 5 item (Hick) |
| Body text | 14–16px/sp minimum, dukung dynamic type / text scaling |
| Motion | 200–300ms micro-interaction · 300–500ms transisi antar layar · easing `ease-in-out`/`cubic-bezier`, never linear |
| Typography scale | 12/14/16/20/24/32px — jangan ukuran acak per halaman |

## Design mode

1. **Tokens first.** Before writing any component, define design tokens: color roles (primary/secondary/accent/semantic), spacing scale, radius, shadow, typography scale. One source of truth lintas platform (Flutter + Next.js) — jangan hardcode nilai berulang di tiap komponen.
2. **Compose on the 8-point grid.** All margins and padding are multiples of 8. Use spacing to group: dekat = satu kesatuan (Proximity), Common Region (card/border/background) saat jarak saja tidak cukup.
3. **Paint with 60-30-10.** Pick the dominant surface first, then secondary, then one accent reserved for actions you want noticed (Von Restorff: yang menonjol diingat dan diklik).
4. **Check the reading pattern.** Satu aksi utama (landing, onboarding) → pola Z, CTA mendarat di kanan bawah. Penuh konten (list, artikel, dashboard) → pola F; taruh item terpenting di awal/akhir list, bukan tengah (Serial Position).
5. **Place for thumbs (mobile).** CTA dan navigasi utama di zona jangkauan ibu jari (bawah-tengah); jangan taruh aksi kritis di pojok atas berlawanan tangan dominan.
6. **Stay familiar (Jakob).** Keranjang kanan-atas, hamburger menu, swipe-to-delete: pakai pola yang sudah dikenal pengguna; pola baru hanya dengan alasan kuat.
7. **Respect the limits.** Nav ≤ 5 item; pecah form panjang jadi beberapa step (Miller 7±2); setiap elemen interaktif ≥ 44×44px dengan jarak ≥ 8px; semua yang bisa diklik seragam gayanya (Similarity).
8. **Show system status (Nielsen #1).** Desain state loading, empty, error, success untuk setiap aksi async. Cegah error daripada hanya melaporkannya: disable submit sebelum form valid, konfirmasi aksi destruktif, sediakan undo. Akhiri flow dengan momen memuaskan (Peak-End: animasi sukses di akhir checkout/onboarding lebih diingat daripada seluruh perjalanan).
9. **Motion with intent.** Durasi dan easing dari tabel di atas; motion menjaga kontinuitas (card yang di-tap membesar menjadi halaman baru, bukan tiba-tiba berganti). Motion yang sekadar dekorasi menambah beban kognitif — buang.
10. **Finish the details.** Keyboard/screen-reader access di web (ARIA sesuai kebutuhan), tanpa konten flashing, dan polish visual tetap penting (Aesthetic-Usability: yang estetik dipersepsikan lebih usable).

## Review mode

Audit the UI against the numbers table above and the ship checklist in `references/panduan-lengkap.md`, then report:

1. **Findings first** — each with the rule broken, where (element/file/area screenshot), and a concrete fix: "padding 10px → 16px agar masuk grid 8-point", bukan "perbaiki spacing".
2. **Severity** — pelanggaran aksesibilitas (kontras, tap target, status warna-saja) = blocking; proporsi warna dan motion = polish.
3. **What passes** — sebutkan juga yang sudah benar, agar user tahu apa yang jangan diubah.

Jangan menulis ulang seluruh UI kecuali diminta; ajukan perbaikan yang tertarget.

## Full reference

Untuk tabel lengkap — enam prinsip Gestalt, semua hukum kognitif (Hick, Fitts, Miller, Jakob, Von Restorff, Peak-End, Serial Position, Aesthetic-Usability) beserta implikasi desainnya, 10 heuristik Nielsen, pola baca Z/F, peta thumb zone, dan checklist ship — baca `references/panduan-lengkap.md`. Baca sebelum melakukan review UI yang non-trivial, atau saat mode desain menyentuh area yang tidak dicakup ringkasan di atas.
