# PRD template

Fill every section from the interview + the approved plan. Headings below are Indonesian — render them in the user's language. Guidance comments (`<!-- -->`) are instructions for you; delete them from the output. Leave no section empty.

# PRD — <Nama Produk>

| | |
|---|---|
| Versi | 1.0 (draft) |
| Tanggal | <tanggal> |
| Status | Draft — menunggu review |
| Disusun | Hasil interview & plan bersama <nama tool/AI> |

## 1. Ringkasan Eksekutif
<!-- 2–4 kalimat: masalah → solusi → untuk siapa → pembeda utama. -->

## 2. Latar Belakang & Masalah
<!-- Situasi sekarang, pain utama, kutip jawaban interview sebagai bukti, kenapa solusi existing kurang. -->

## 3. Tujuan & Non-Tujuan
<!-- Goals = outcome, bukan fitur (3–5 butir). Non-goals = daftar eksplisit yang TIDAK dikerjakan, dari bagian out of scope di plan. -->

## 4. Pengguna Sasaran
<!-- Tabel persona: nama, konteks, cara ngatasi masalah sekarang, kebutuhan, kenyamanan teknologi. Persona utama dulu. -->

## 5. Cerita Pengguna & Alur Utama
<!-- 3–5 user story: "Sebagai <persona>, aku ingin <aksi> agar <manfaat>." -->
<!-- 1 happy-path flow bernomor untuk core job #1 dari interview. -->

## 6. Kebutuhan Fungsional
<!-- Dari feature tree yang sudah disetujui, dikelompokkan per fase. -->
<!-- ID = F<fase>.<nomor>. Priority: P0 (MVP) / P1 / P2. Format per fitur: -->

### F1.1 — <Nama Fitur> (P0)
<1–2 kalimat deskripsi.>
- <sub-fitur>
- <sub-fitur>

Acceptance criteria:
- [ ] <kondisi yang bisa dites>
- [ ] <kondisi lain>

<!-- Contoh kualitas yang diharapkan: -->
### F1.1 — Editor Undangan (P0)
Pengguna mengisi data acara, memilih tema, dan mengunggah foto untuk membuat undangan.
- Isi nama pengantin, tanggal & lokasi acara
- Pilih tema warna
- Unggah foto

Acceptance criteria:
- [ ] Data tersimpan otomatis; isi tidak hilang saat halaman di-refresh
- [ ] Ganti tema langsung terlihat di preview
- [ ] Foto > 5 MB ditolak dengan pesan yang jelas

<!-- Fitur P1/P2 boleh acceptance criteria satu baris. -->

## 7. Kebutuhan Non-Fungsional
<!-- Hanya yang relevan untuk produk ini; sisanya tulis "N/A". Performance, security, privacy & data, availability, accessibility, i18n. -->

## 8. Metrik Keberhasilan
<!-- Tabel: metrik, target, cara ukur. 2–4 baris, sesuai jawaban success signal. -->

## 9. Teknologi
<!-- Per layer: pilihan + alasan satu baris. Jika user memilih "Biarkan AI pilih", catat proposal final di sini. -->

## 10. Rencana Rilis
<!-- Per fase dari plan: cakupan bullet + definition of done per fase. -->

## 11. Risiko & Mitigasi
<!-- 3–5 risiko: risiko, dampak, mitigasi. -->

## 12. Pertanyaan Terbuka
<!-- Semua yang di-skip user atau diasumsikan. Format: pertanyaan — kenapa penting — default yang disarankan. -->
