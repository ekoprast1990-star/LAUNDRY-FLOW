# Blueprint Aplikasi LaundryFlow
## Manajemen Laundry Pintar Berbasis Website

**Versi dokumen:** 1.0  
**Status:** Blueprint awal untuk pengembangan melalui Antigravity  
**Nama produk:** LaundryFlow  
**Platform:** Website responsif (desktop, tablet, dan mobile)  
**Bahasa utama:** Bahasa Indonesia  
**Zona waktu default:** Asia/Jakarta  
**Mata uang default:** Rupiah (IDR)

---

## 1. Ringkasan Produk

LaundryFlow adalah aplikasi manajemen laundry berbasis website untuk membantu usaha laundry kecil hingga menengah mengelola pesanan, pelanggan, pakaian, antrean kerja, status pengerjaan, pembayaran, dan notifikasi secara terpusat.

Aplikasi memiliki tiga kelompok pengguna utama:

1. **Pemilik laundry** — memantau operasional, keuangan, performa layanan, antrean, dan analitik.
2. **Karyawan** — menerima pesanan, mencatat detail pakaian, memperbarui status pengerjaan, dan mengelola serah-terima.
3. **Pelanggan** — melihat status pesanannya, perkiraan selesai, tagihan, dan notifikasi melalui portal pelanggan.

Nilai utama LaundryFlow adalah mengurangi pencatatan manual, meminimalkan pakaian atau pesanan yang sulit dilacak, mengurangi pelanggan yang harus bertanya tentang status cucian, serta membantu pemilik mengambil keputusan berdasarkan data.

### 1.1 Sasaran utama

- Seluruh pesanan tercatat secara digital dan memiliki kode pesanan unik.
- Setiap pesanan dapat dilacak melalui tahapan status yang konsisten.
- Pelanggan dapat mengetahui status dan estimasi selesai tanpa harus menghubungi karyawan.
- Pemilik dapat melihat jumlah pelanggan, pesanan aktif, dan antrean tersisa.
- Sistem menghitung estimasi selesai berdasarkan aturan operasional dan data historis jika tersedia.
- Pemilik mendapatkan ringkasan periode ramai untuk membantu pengaturan staf dan kapasitas.
- Transaksi pembayaran dan perubahan penting tercatat serta dapat diaudit.

### 1.2 Prinsip produk

- **Mudah digunakan:** proses utama dapat dilakukan dengan sedikit langkah.
- **Mobile-first untuk operasional:** karyawan dapat menggunakan website dari ponsel.
- **Data akurat:** status dan pembayaran memiliki riwayat perubahan.
- **Prediksi transparan:** estimasi ditampilkan sebagai perkiraan, bukan janji mutlak.
- **Privasi berdasarkan peran:** pelanggan hanya dapat melihat data miliknya.
- **MVP realistis:** fitur inti harus stabil sebelum fitur prediktif lanjutan ditambahkan.

---

## 2. Masalah dan Solusi

| Masalah | Solusi LaundryFlow | Indikator keberhasilan |
|---|---|---|
| Pesanan ditulis manual dan mudah hilang | Form pesanan digital, nomor order unik, pencarian cepat | Pesanan tercatat dan dapat ditemukan |
| Pakaian sulit dilacak | Label/kode order, jumlah dan catatan item, status pengerjaan | Penurunan pesanan yang tidak diketahui lokasinya |
| Pelanggan tidak tahu cucian selesai | Portal pelanggan dan notifikasi status | Berkurangnya pertanyaan status melalui telepon/chat |
| Antrean sulit dipantau | Papan antrean dan ringkasan pesanan aktif | Pemilik mengetahui beban kerja saat ini |
| Estimasi selesai hanya berdasarkan tebakan | Estimasi berbasis layanan, antrean, jam operasional, dan data historis | Estimasi semakin akurat seiring terkumpulnya data |
| Sulit menentukan waktu ramai | Analitik volume order berdasarkan jam, hari, dan periode | Pemilik dapat menyesuaikan jadwal staf dan kapasitas |
| Pembayaran sulit direkap | Catatan pembayaran, status tagihan, dan laporan | Rekap transaksi lebih konsisten |

---

## 3. Ruang Lingkup Produk

### 3.1 Termasuk dalam MVP

- Autentikasi dan pengelolaan peran.
- Pengaturan profil outlet laundry.
- Data pelanggan.
- Katalog layanan dan tarif.
- Pembuatan pesanan dan kode order.
- Detail berat/jumlah, jenis layanan, catatan khusus, dan estimasi selesai.
- Alur status pengerjaan.
- Papan antrean operasional.
- Pembayaran tunai/transfer/manual dan pencatatan status pembayaran.
- Portal pelanggan untuk melihat pesanan miliknya.
- Notifikasi di dalam aplikasi dan notifikasi berbasis email jika dikonfigurasi.
- Dashboard pemilik.
- Laporan pesanan dan pendapatan dasar.
- Audit log untuk aktivitas penting.
- Desain responsif dan aksesibilitas dasar.

### 3.2 Fitur tahap berikutnya

- Integrasi WhatsApp Business API atau penyedia pesan lain.
- Pembayaran online melalui payment gateway.
- Cetak struk dan label QR/barcode.
- Multi-outlet dan pemindahan pesanan antar-outlet.
- Pengambilan dan pengantaran (pickup/delivery).
- Prediksi waktu selesai berbasis machine learning setelah data historis mencukupi.
- Manajemen stok deterjen dan bahan operasional.
- Program loyalitas, voucher, dan langganan pelanggan.
- Integrasi akuntansi atau ekspor ke aplikasi akuntansi.
- Aplikasi/PWA dengan kemampuan offline terbatas jika kebutuhan sudah tervalidasi.

**Catatan:** Jangan mengklaim prediksi berbasis AI telah aktif jika sistem hanya menggunakan aturan perkiraan. Pada MVP, gunakan estimasi berbasis aturan dan data historis sederhana; sebut sebagai “estimasi pintar” dan jelaskan dasar estimasinya.

### 3.3 Di luar ruang lingkup awal

- Sistem payroll dan HR lengkap.
- Akuntansi perusahaan penuh.
- Marketplace laundry lintas merek.
- Pelacakan GPS kurir secara real-time.
- Model machine learning kompleks tanpa data historis yang cukup.

---

## 4. Peran Pengguna dan Hak Akses

### 4.1 Pemilik Laundry (`OWNER`)

Dapat:
- Melihat dashboard, antrean, statistik, dan laporan.
- Membuat, mengubah, membatalkan, atau mengoreksi pesanan sesuai aturan.
- Mengelola pelanggan, karyawan, layanan, harga, jam operasional, dan pengaturan outlet.
- Melihat semua transaksi dan status pembayaran.
- Mengakses analitik waktu ramai dan performa estimasi.
- Mengelola template notifikasi.
- Melihat audit log.

### 4.2 Karyawan (`STAFF`)

Dapat:
- Membuat pesanan dan data pelanggan.
- Melihat pesanan yang diperlukan untuk operasional.
- Memperbarui status pengerjaan sesuai urutan yang diizinkan.
- Mencatat berat/jumlah akhir dan catatan penanganan.
- Mencatat pembayaran jika diberi izin.
- Menandai pesanan siap diambil dan telah diserahkan.
- Tidak dapat mengubah konfigurasi sensitif, menghapus audit log, atau melihat laporan keuangan penuh kecuali diberi izin khusus.

### 4.3 Pelanggan (`CUSTOMER`)

Dapat:
- Mendaftar atau masuk dengan metode yang disediakan.
- Melihat daftar dan detail pesanannya sendiri.
- Melihat kode order, layanan, status, estimasi selesai, tagihan, dan status pembayaran.
- Melihat notifikasi dan riwayat status.
- Mengelola informasi profil dasar.
- Tidak dapat melihat pesanan atau data pelanggan lain.
- Tidak dapat mengubah status pengerjaan atau nilai transaksi.

### 4.4 Matriks hak akses

| Fitur | OWNER | STAFF | CUSTOMER |
|---|---:|---:|---:|
| Dashboard operasional | Ya | Ringkas | Tidak |
| Dashboard analitik/pendapatan | Ya | Sesuai izin | Tidak |
| Buat pesanan | Ya | Ya | Tidak, kecuali fitur order mandiri ditambahkan |
| Ubah status pengerjaan | Ya | Ya, sesuai alur | Tidak |
| Kelola layanan dan harga | Ya | Tidak | Tidak |
| Kelola karyawan | Ya | Tidak | Tidak |
| Lihat pesanan pelanggan | Semua outlet yang diizinkan | Sesuai kebutuhan operasional | Milik sendiri |
| Catat pembayaran | Ya | Sesuai izin | Tidak |
| Lihat laporan keuangan | Ya | Terbatas | Hanya tagihan sendiri |
| Audit log | Ya | Tidak | Tidak |
| Pengaturan outlet | Ya | Tidak | Tidak |

Terapkan otorisasi di sisi server untuk setiap endpoint, bukan hanya menyembunyikan menu di antarmuka.

---

## 5. Alur Operasional Utama

### 5.1 Alur pesanan

1. Karyawan memilih pelanggan yang sudah ada atau membuat pelanggan baru.
2. Karyawan memilih layanan, misalnya cuci-kering, cuci-setrika, setrika saja, atau layanan kiloan/satuan.
3. Karyawan memasukkan berat/jumlah, catatan khusus, dan target waktu jika ada.
4. Sistem menghitung subtotal, diskon jika diizinkan, biaya tambahan, total tagihan, serta estimasi selesai.
5. Sistem menyimpan pesanan dan membuat kode order unik yang mudah dibaca.
6. Sistem menampilkan ringkasan pesanan untuk diperiksa sebelum disimpan.
7. Pelanggan menerima bukti order atau dapat melihat order di portal.
8. Karyawan memperbarui status sepanjang proses.
9. Ketika siap diambil, pelanggan mendapat notifikasi.
10. Setelah pembayaran dan serah-terima selesai, pesanan ditandai selesai.

### 5.2 Alur status pesanan

Status yang direkomendasikan:

`RECEIVED` → `QUEUED` → `WASHING` → `DRYING` → `IRONING` → `QUALITY_CHECK` → `READY_FOR_PICKUP` → `COMPLETED`

Status tambahan:
- `ON_HOLD` — ditahan karena kendala, dengan alasan wajib.
- `CANCELLED` — dibatalkan sesuai kebijakan, dengan alasan dan pencatat.
- `DELIVERY` — status pengantaran opsional jika fitur delivery diaktifkan.

Tidak semua layanan harus melewati seluruh status. Contohnya, layanan setrika saja dapat melewati tahap pencucian dan pengeringan. Status yang tersedia harus mengikuti alur layanan yang dikonfigurasi.

Setiap perubahan status wajib menyimpan:
- Status sebelumnya dan status baru.
- Waktu perubahan.
- Pengguna yang melakukan perubahan.
- Catatan opsional atau alasan wajib untuk status tertentu.

### 5.3 Alur pembayaran

Status pembayaran:
- `UNPAID`
- `PARTIALLY_PAID`
- `PAID`
- `REFUNDED`
- `VOID`

Metode pembayaran awal:
- Tunai.
- Transfer bank yang diverifikasi manual.
- QRIS/manual jika pencatatan dilakukan oleh petugas.
- Payment gateway pada fase berikutnya.

Jangan menyimpan nomor kartu, PIN, CVV, atau kredensial perbankan pelanggan. Simpan referensi transaksi seperlunya, nominal, metode, waktu, dan petugas yang mencatat.

### 5.4 Alur pembatalan dan koreksi

- Pesanan yang sudah masuk proses produksi tidak boleh dihapus permanen dari sistem.
- Pembatalan memerlukan alasan dan pengguna yang bertanggung jawab.
- Koreksi harga atau pembayaran harus tercatat pada audit log.
- Jika sudah ada pembayaran, proses pengembalian dana mengikuti kebijakan yang dikonfigurasi dan dicatat terpisah.

---

## 6. Modul dan Fitur

### 6.1 Autentikasi dan onboarding

- Login/logout.
- Pendaftaran pelanggan.
- Undangan atau pembuatan akun karyawan oleh pemilik.
- Reset kata sandi.
- Verifikasi email atau nomor telepon jika kanal tersedia.
- Pengalihan halaman berdasarkan peran.
- Pengelolaan sesi dan perlindungan terhadap percobaan login berulang.

### 6.2 Dashboard pemilik

Tampilkan kartu ringkasan:
- Pesanan masuk hari ini.
- Pesanan aktif.
- Pesanan siap diambil.
- Pesanan terlambat dari estimasi.
- Jumlah pelanggan unik dalam periode terpilih.
- Antrean yang belum mulai diproses.
- Pendapatan tercatat hari ini/periode terpilih.
- Status pembayaran belum lunas.

Visualisasi:
- Grafik pesanan per hari.
- Grafik pendapatan per hari.
- Distribusi status pesanan.
- Periode ramai berdasarkan jam dan hari.
- Perbandingan estimasi waktu selesai dengan waktu aktual, bila datanya tersedia.

Filter dashboard:
- Hari ini, 7 hari, 30 hari, dan rentang tanggal khusus.
- Outlet jika multi-outlet diaktifkan.
- Layanan.

### 6.3 Dashboard karyawan

- Daftar pekerjaan yang perlu dikerjakan sekarang.
- Antrean berdasarkan prioritas dan waktu masuk.
- Pesanan yang mendekati tenggat.
- Tombol cepat untuk memperbarui status.
- Pencarian berdasarkan kode order, nama pelanggan, atau nomor kontak.
- Peringatan jika status tidak dapat dilanjutkan karena alur layanan.

### 6.4 Manajemen pesanan

- Buat, lihat, dan ubah pesanan dengan validasi.
- Kode order unik, misalnya `LF-20261024-0001`.
- Simpan snapshot harga saat pesanan dibuat agar perubahan harga katalog tidak mengubah pesanan lama.
- Detail item, layanan, kuantitas/berat, tarif, biaya tambahan, diskon, total, catatan, dan target waktu.
- Riwayat status dan pembayaran.
- Cetak/unduh bukti pesanan sebagai fitur tambahan.
- Pencarian, filter, pengurutan, dan pagination.
- Hindari penghapusan permanen untuk transaksi yang telah tercatat.

### 6.5 Manajemen pelanggan

- Nama pelanggan.
- Nomor telepon dan email opsional.
- Catatan layanan yang relevan dan tidak sensitif.
- Tanggal bergabung.
- Jumlah pesanan dan nilai transaksi agregat jika diperlukan.
- Riwayat pesanan.
- Status pelanggan aktif/nonaktif.
- Deduplikasi berdasarkan nomor telepon yang dinormalisasi, dengan opsi koreksi oleh pemilik.

### 6.6 Katalog layanan dan tarif

Contoh kategori yang dapat dikonfigurasi:
- Laundry kiloan.
- Cuci dan setrika.
- Cuci saja.
- Setrika saja.
- Laundry satuan.
- Express.
- Layanan khusus.

Setiap layanan dapat memiliki:
- Nama dan deskripsi.
- Satuan tarif: kg, item, paket, atau layanan.
- Harga dasar.
- Estimasi durasi.
- Kapasitas atau batas layanan opsional.
- Urutan status yang harus dilalui.
- Status aktif/nonaktif.

Harga dan durasi harus dapat diatur pemilik; jangan hard-code harga contoh sebagai harga tetap.

### 6.7 Antrean dan kapasitas

Antrean menampilkan:
- Jumlah pesanan menunggu proses.
- Jumlah pesanan yang sedang dikerjakan.
- Jumlah pesanan siap diambil.
- Pesanan berdasarkan layanan, prioritas, dan target selesai.
- Perkiraan beban kerja berdasarkan estimasi durasi.
- Peringatan antrean tinggi.

Definisi yang harus konsisten:
- **Pelanggan hari ini:** pelanggan unik yang memiliki pesanan pada tanggal terpilih.
- **Pesanan aktif:** pesanan belum `COMPLETED` atau `CANCELLED`.
- **Antrean tersisa:** pesanan yang belum memulai tahap operasional utama, sesuai definisi status yang ditetapkan outlet.
- **Kapasitas:** jumlah pekerjaan atau estimasi beban kerja yang dapat ditangani berdasarkan konfigurasi outlet.

Jangan mencampur jumlah pelanggan dengan jumlah pesanan. Label metrik harus jelas dan memiliki rentang waktu.

### 6.8 Estimasi waktu selesai

#### Tahap 1 — estimasi berbasis aturan

Perkiraan waktu selesai dihitung dari:
- Durasi dasar layanan.
- Waktu antrean yang ada.
- Jam operasional dan hari libur.
- Beban kerja saat ini.
- Layanan express atau prioritas yang sah.
- Batas kapasitas mesin/staf jika dikonfigurasi.
- Waktu tambahan untuk pemeriksaan kualitas dan penyerahan.

Contoh pendekatan:
`estimasi_selesai = waktu_mulai_terprediksi + durasi_layanan + buffer_operasional`

Aturan harus memperhitungkan jam tutup. Jika durasi melewati jam operasional, lanjutkan perhitungan pada jam operasional berikutnya.

#### Tahap 2 — penyesuaian dari data historis

Setelah data mencukupi, sistem dapat menghitung median atau persentil durasi aktual berdasarkan layanan, hari, dan beban antrean. Hindari memakai rata-rata sederhana jika terdapat pencilan besar.

Data yang dicatat:
- Waktu order diterima.
- Waktu setiap status dimulai/selesai.
- Waktu order siap diambil.
- Waktu order benar-benar diserahkan.
- Jenis layanan dan kondisi antrean saat order masuk.

Tampilkan:
- Estimasi selesai.
- Label tingkat keyakinan seperti “perkiraan awal” atau “berdasarkan riwayat yang cukup”.
- Alasan umum perubahan estimasi, misalnya antrean meningkat.
- Waktu estimasi terakhir diperbarui.

Jangan menampilkan persentase akurasi yang tidak dihitung dari data nyata. Pemilik harus dapat mengoreksi estimasi dengan alasan; koreksi disimpan untuk evaluasi.

### 6.9 Analitik periode ramai

Analitik dapat mengelompokkan:
- Jumlah order per jam.
- Jumlah order per hari dalam seminggu.
- Pendapatan per hari/jam bila relevan.
- Rata-rata durasi pengerjaan per layanan.
- Rasio order terlambat dari estimasi.
- Rata-rata antrean.
- Perbandingan periode sebelumnya.

Rekomendasi operasional contoh:
- “Order paling banyak tercatat pada Sabtu pukul 10.00–12.00.”
- “Pertimbangkan menambah satu petugas pada periode ini.”
- “Layanan express memiliki keterlambatan lebih tinggi pada jam sibuk.”

Rekomendasi harus didasarkan pada data yang tersedia, menyebut rentang waktu analisis, dan tidak mengarang kesimpulan saat sampel terlalu sedikit. Jika data belum memadai, tampilkan pesan “Data belum cukup untuk analisis yang andal.”

### 6.10 Notifikasi pelanggan

Jenis notifikasi:
- Pesanan berhasil dibuat.
- Status berubah.
- Estimasi selesai berubah secara signifikan.
- Cucian siap diambil.
- Pembayaran tercatat.
- Pengingat pesanan belum diambil, jika diaktifkan.

Kanal:
1. Notifikasi dalam portal sebagai baseline.
2. Email jika konfigurasi tersedia.
3. WhatsApp/SMS melalui provider resmi pada fase lanjutan.

Persyaratan:
- Simpan status pengiriman: menunggu, terkirim, gagal.
- Percobaan ulang dengan batas yang jelas.
- Jangan mengirim notifikasi duplikat untuk event yang sama.
- Simpan template dan waktu pengiriman.
- Sediakan preferensi notifikasi yang sesuai.
- Jangan menampilkan data pelanggan lain pada isi notifikasi.

### 6.11 Pembayaran dan laporan

- Catat nominal tagihan, pembayaran, sisa tagihan, metode, waktu, dan petugas.
- Mendukung pembayaran penuh atau sebagian jika kebijakan outlet mengizinkan.
- Rekap pendapatan berdasarkan transaksi yang benar-benar tercatat, dengan definisi jelas apakah laporan memakai tanggal pembayaran atau tanggal pesanan.
- Filter tanggal, layanan, dan status.
- Ekspor CSV untuk laporan dasar.
- Tampilkan ringkasan pembatalan/refund secara terpisah.
- Jangan menganggap pesanan selesai sebagai otomatis sudah lunas.

### 6.12 Pengaturan outlet

- Nama dan logo laundry.
- Alamat dan kontak.
- Jam operasional per hari.
- Hari libur.
- Mata uang dan format tanggal.
- Prefix kode order.
- Tarif, biaya tambahan, dan kebijakan pembatalan.
- Kapasitas kerja.
- Template bukti order dan notifikasi.
- Pengaturan zona waktu.

---

## 7. Struktur Halaman dan Navigasi

### 7.1 Halaman publik

- `/` — landing page/halaman informasi.
- `/login` — masuk.
- `/register` — pendaftaran pelanggan.
- `/forgot-password` — pemulihan kata sandi.
- `/track` — pencarian pesanan dengan kode order dan verifikasi tambahan, jika fitur pelacakan publik diaktifkan.

### 7.2 Area pemilik

- `/owner/dashboard`
- `/owner/orders`
- `/owner/orders/new`
- `/owner/orders/:id`
- `/owner/customers`
- `/owner/services`
- `/owner/payments`
- `/owner/reports`
- `/owner/analytics`
- `/owner/staff`
- `/owner/settings`
- `/owner/audit-logs`

### 7.3 Area karyawan

- `/staff/dashboard`
- `/staff/queue`
- `/staff/orders`
- `/staff/orders/new`
- `/staff/orders/:id`
- `/staff/payments` — hanya jika diberi izin.

### 7.4 Area pelanggan

- `/customer/dashboard`
- `/customer/orders`
- `/customer/orders/:id`
- `/customer/notifications`
- `/customer/profile`

Semua rute privat harus memeriksa autentikasi, peran, dan kepemilikan data. ID pada URL tidak boleh menjadi cara untuk mengakses data pengguna lain.

---

## 8. Rekomendasi UI/UX

### 8.1 Arah visual

- Kesan bersih, modern, ramah, dan profesional.
- Palet yang disarankan: biru atau teal sebagai warna utama, putih/abu-abu muda sebagai latar, warna status dengan kontras memadai.
- Tipografi sans-serif yang mudah dibaca.
- Gunakan ikon konsisten dan label teks untuk status penting.
- Hindari tampilan dashboard yang terlalu padat.

### 8.2 Layout

- Desktop: sidebar navigasi, header, area konten utama.
- Mobile: navigasi ringkas, tombol tindakan utama mudah dijangkau, tabel berubah menjadi kartu/list.
- Dashboard menggunakan kartu metrik, grafik sederhana, dan daftar pesanan prioritas.
- Form pesanan dibagi menjadi langkah atau bagian yang jelas.
- Status harus dibedakan dengan teks dan warna; jangan mengandalkan warna saja.

### 8.3 Komponen UI yang perlu dibuat

- App shell/layout berdasarkan peran.
- Sidebar dan mobile navigation.
- Kartu metrik.
- Tabel pesanan dengan filter dan pagination.
- Form pesanan.
- Status badge.
- Timeline riwayat status.
- Dialog konfirmasi untuk pembatalan/koreksi.
- Form pembayaran.
- Grafik analitik.
- Panel antrean.
- Empty state, loading state, error state, dan success feedback.
- Notifikasi/toast.
- Modal detail pelanggan dan order.

### 8.4 Prinsip interaksi

- Setelah menyimpan pesanan, tampilkan kode order dan ringkasan.
- Berikan konfirmasi sebelum membatalkan pesanan atau mengubah pembayaran.
- Tampilkan kesalahan validasi dekat dengan field terkait.
- Gunakan format rupiah yang konsisten.
- Gunakan tanggal dan jam lokal Asia/Jakarta.
- Sediakan pencarian cepat berdasarkan kode order.
- Jangan mengandalkan data dummy pada produksi; tandai data demo secara jelas.

---

## 9. Arsitektur Teknis yang Direkomendasikan

Blueprint ini tidak mewajibkan satu framework tertentu. Jika Antigravity meminta pilihan teknologi, gunakan stack modern yang mendukung pengembangan full-stack, autentikasi, database relasional, dan deployment yang jelas.

### 9.1 Opsi stack

**Opsi rekomendasi untuk implementasi cepat:**
- Frontend: Next.js + TypeScript.
- UI: Tailwind CSS dan komponen UI yang aksesibel.
- Backend: Next.js server actions/API routes atau backend service terpisah jika kompleksitas meningkat.
- Database: PostgreSQL.
- ORM: Prisma atau Drizzle.
- Validasi: Zod atau library validasi sejenis.
- Grafik: library chart yang kompatibel dengan React.
- Autentikasi: solusi session-based yang aman atau provider autentikasi terkelola.
- Penyimpanan file: object storage untuk logo/berkas jika dibutuhkan.
- Deployment: platform yang mendukung aplikasi web dan PostgreSQL.

Stack dapat disesuaikan dengan standar proyek Antigravity, tetapi semua pilihan harus ditetapkan secara konsisten sebelum implementasi.

### 9.2 Pola arsitektur

Gunakan arsitektur modular:
- Presentation/UI layer.
- Application/service layer untuk aturan bisnis.
- Data-access layer.
- Database relasional.
- Notification adapter.
- Analytics/estimation service.
- Audit logging.

Jangan menaruh seluruh aturan bisnis di komponen UI. Validasi harga, perubahan status, pembayaran, dan otorisasi harus dijalankan di server.

### 9.3 Lingkungan

- Development.
- Staging/testing.
- Production.

Gunakan environment variables untuk rahasia dan konfigurasi. Jangan memasukkan API key, password database, atau secret ke source code, repository, maupun output browser.

### 9.4 Persyaratan kualitas

- Type safety untuk kode TypeScript.
- Validasi input di sisi server.
- Error handling yang konsisten.
- Logging terstruktur tanpa membocorkan data sensitif.
- Migrasi database yang dapat diulang dan ditinjau.
- Backup database dan prosedur pemulihan.
- Monitoring error aplikasi.
- Pagination untuk daftar besar.
- Indeks database pada kolom pencarian dan filter yang sering dipakai.

---

## 10. Desain Database Awal

Gunakan UUID atau ID unik yang aman sebagai primary key. Nama kolom berikut adalah rancangan konseptual dan dapat disesuaikan dengan ORM.

### 10.1 `users`

- `id`
- `name`
- `email` (nullable jika login tidak memakai email)
- `phone` (nullable)
- `password_hash` atau referensi provider autentikasi
- `role` (`OWNER`, `STAFF`, `CUSTOMER`)
- `is_active`
- `created_at`
- `updated_at`
- `last_login_at`

### 10.2 `outlets`

- `id`
- `name`
- `code`
- `address`
- `phone`
- `timezone`
- `opening_hours` atau relasi ke tabel jam operasional
- `is_active`
- `created_at`
- `updated_at`

### 10.3 `outlet_members`

Untuk menghubungkan pengguna dengan outlet:
- `id`
- `outlet_id`
- `user_id`
- `role`
- `permissions` (opsional, bila menggunakan izin granular)
- `created_at`

### 10.4 `customers`

- `id`
- `user_id` (nullable jika pelanggan dibuat oleh staf tanpa akun portal)
- `outlet_id`
- `name`
- `phone_normalized`
- `email`
- `notes`
- `is_active`
- `created_at`
- `updated_at`

### 10.5 `services`

- `id`
- `outlet_id`
- `name`
- `description`
- `pricing_unit` (`KG`, `ITEM`, `PACKAGE`, `SERVICE`)
- `price`
- `estimated_duration_minutes`
- `workflow_config`
- `is_express`
- `is_active`
- `created_at`
- `updated_at`

### 10.6 `orders`

- `id`
- `outlet_id`
- `customer_id`
- `order_code`
- `created_by_user_id`
- `status`
- `payment_status`
- `subtotal`
- `discount_amount`
- `extra_charge`
- `total_amount`
- `paid_amount`
- `received_at`
- `estimated_ready_at`
- `actual_ready_at`
- `completed_at`
- `customer_notes`
- `internal_notes`
- `cancelled_at`
- `cancellation_reason`
- `created_at`
- `updated_at`

Ketentuan:
- `order_code` unik pada cakupan yang ditentukan (global atau per outlet).
- Simpan harga dan total sebagai snapshot transaksi.
- Nilai uang menggunakan tipe decimal/numeric, bukan floating point.
- Pastikan `paid_amount` dan total tervalidasi oleh aturan bisnis.

### 10.7 `order_items`

- `id`
- `order_id`
- `service_id`
- `service_name_snapshot`
- `pricing_unit_snapshot`
- `unit_price`
- `quantity`
- `line_total`
- `notes`

### 10.8 `order_status_history`

- `id`
- `order_id`
- `from_status`
- `to_status`
- `changed_by_user_id`
- `note`
- `changed_at`

### 10.9 `payments`

- `id`
- `order_id`
- `amount`
- `method`
- `status`
- `reference_code`
- `recorded_by_user_id`
- `paid_at`
- `notes`
- `created_at`
- `updated_at`

### 10.10 `notifications`

- `id`
- `user_id` (nullable untuk notifikasi yang ditujukan ke kontak pelanggan tanpa akun)
- `customer_id`
- `order_id`
- `channel`
- `template_key`
- `destination_masked`
- `status`
- `provider_reference`
- `sent_at`
- `failure_reason`
- `created_at`

### 10.11 `audit_logs`

- `id`
- `outlet_id`
- `actor_user_id`
- `action`
- `entity_type`
- `entity_id`
- `before_data` (JSON yang telah disaring)
- `after_data` (JSON yang telah disaring)
- `ip_address` (jika sah dan diperlukan)
- `created_at`

Jangan simpan password, token, atau data pembayaran sensitif dalam audit log.

### 10.12 `operating_hours`

- `id`
- `outlet_id`
- `day_of_week`
- `opens_at`
- `closes_at`
- `is_closed`

### 10.13 `holidays`

- `id`
- `outlet_id`
- `date`
- `name`
- `is_closed`
- `special_open_time`
- `special_close_time`

### 10.14 `estimation_records`

- `id`
- `order_id`
- `method` (`RULE_BASED`, `HISTORICAL`, `MANUAL_OVERRIDE`)
- `estimated_at`
- `predicted_ready_at`
- `actual_ready_at`
- `features_snapshot` (data agregat yang diperlukan, tanpa data pribadi berlebihan)
- `confidence_label`
- `override_reason`
- `created_at`

### 10.15 Relasi utama

- Satu outlet memiliki banyak layanan, pesanan, pelanggan, dan anggota staf.
- Satu pelanggan dapat memiliki banyak pesanan.
- Satu pesanan memiliki banyak item, riwayat status, pembayaran, dan catatan estimasi.
- Satu pengguna dapat terhubung ke satu atau beberapa outlet melalui `outlet_members`.
- Satu pesanan dapat memiliki beberapa pembayaran jika pembayaran sebagian diaktifkan.

Tambahkan foreign key, indeks, unique constraints, dan kebijakan penghapusan yang sesuai. Pertimbangkan soft delete untuk data master, tetapi jangan gunakan soft delete untuk menyamarkan perubahan transaksi.

---

## 11. API/Server Actions Konseptual

Nama endpoint di bawah adalah usulan; dapat diwujudkan sebagai REST API atau server actions.

### Auth
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `POST /api/auth/register`
- `POST /api/auth/forgot-password`

### Orders
- `GET /api/orders`
- `POST /api/orders`
- `GET /api/orders/:id`
- `PATCH /api/orders/:id`
- `POST /api/orders/:id/status`
- `POST /api/orders/:id/cancel`
- `GET /api/orders/:id/history`

### Customers
- `GET /api/customers`
- `POST /api/customers`
- `GET /api/customers/:id`
- `PATCH /api/customers/:id`

### Services
- `GET /api/services`
- `POST /api/services`
- `PATCH /api/services/:id`
- `POST /api/services/:id/deactivate`

### Payments
- `GET /api/orders/:id/payments`
- `POST /api/orders/:id/payments`
- `POST /api/payments/:id/void` atau proses refund sesuai kebijakan

### Dashboard dan analitik
- `GET /api/dashboard/summary`
- `GET /api/analytics/orders`
- `GET /api/analytics/peak-periods`
- `GET /api/analytics/estimation-performance`

### Notifications
- `GET /api/notifications`
- `POST /api/notifications/:id/retry` (khusus role berizin)

Setiap request harus:
- Memvalidasi autentikasi dan peran.
- Memastikan pengguna memiliki akses ke outlet dan data terkait.
- Memvalidasi payload.
- Menggunakan transaksi database untuk perubahan multi-tabel yang harus konsisten.
- Menghasilkan error yang konsisten tanpa membocorkan detail internal.
- Mencatat audit log untuk perubahan penting.

---

## 12. Keamanan, Privasi, dan Keandalan

- Hash kata sandi menggunakan algoritma modern yang sesuai; jangan menyimpan kata sandi mentah.
- Gunakan HTTPS pada semua lingkungan yang dapat diakses melalui jaringan publik.
- Terapkan proteksi CSRF jika relevan dengan metode autentikasi, rate limiting, dan pembatasan percobaan login.
- Terapkan validasi dan sanitasi input.
- Cegah SQL injection dengan query terparameterisasi/ORM.
- Cegah akses lintas pelanggan melalui pemeriksaan kepemilikan data di server.
- Terapkan least privilege untuk karyawan.
- Rahasia hanya disimpan di environment secrets.
- Gunakan cookie sesi `HttpOnly`, `Secure`, dan `SameSite` jika menggunakan session cookie.
- Batasi jenis dan ukuran file upload.
- Buat backup terjadwal dan uji pemulihan secara berkala.
- Tetapkan kebijakan retensi data dan prosedur permintaan penghapusan data.
- Hindari mengumpulkan data pribadi yang tidak dibutuhkan.
- Jangan memasukkan nomor telepon/email lengkap ke log publik.
- Catat perubahan transaksi dan status untuk kebutuhan penelusuran.

---

## 13. Aturan Bisnis dan Validasi Penting

1. Kode pesanan harus unik dan tidak dapat diedit sembarangan.
2. Pesanan harus terhubung ke outlet dan pelanggan yang valid.
3. Harga transaksi mengambil snapshot harga pada saat order dibuat.
4. Perubahan status hanya boleh mengikuti workflow layanan, kecuali override oleh role berizin dengan alasan.
5. Status `COMPLETED` hanya dapat diberikan setelah syarat penyelesaian outlet terpenuhi.
6. Status pembayaran dihitung dari tagihan dan pembayaran yang sah; jangan hanya mengandalkan input status manual.
7. Total tagihan tidak boleh negatif.
8. Nilai kuantitas/berat harus lebih besar dari nol, kecuali ada alasan bisnis yang secara eksplisit mendukung nol.
9. Pembatalan harus menyimpan alasan dan pengguna yang melakukan.
10. Estimasi harus diperbarui bila terjadi perubahan antrean yang berdampak signifikan.
11. Jam operasional dan hari libur wajib diperhitungkan dalam estimasi.
12. Pelanggan hanya dapat membaca pesanan miliknya sendiri.
13. Semua perubahan sensitif dicatat di audit log.
14. Laporan pendapatan harus menjelaskan apakah dihitung berdasarkan tanggal order, tanggal pembayaran, atau tanggal penyelesaian.
15. Data dummy harus dipisahkan dari data produksi.

---

## 14. Dashboard dan Definisi Metrik

| Metrik | Definisi |
|---|---|
| Order masuk | Jumlah order yang dibuat dalam rentang waktu terpilih |
| Pelanggan unik | Jumlah customer berbeda yang memiliki order dalam rentang waktu |
| Order aktif | Order yang belum selesai atau dibatalkan |
| Antrean menunggu | Order yang belum memulai tahap kerja sesuai workflow |
| Siap diambil | Order dengan status `READY_FOR_PICKUP` |
| Pendapatan diterima | Total pembayaran valid yang tercatat pada rentang tanggal pembayaran |
| Tagihan belum lunas | Total sisa tagihan pada order yang belum lunas |
| Durasi pengerjaan | Selisih waktu order diterima dengan order siap diambil |
| Keterlambatan | Order yang waktu siap aktualnya melewati estimasi yang berlaku |
| Periode ramai | Periode dengan volume order relatif tinggi berdasarkan data historis |

Setiap grafik harus memiliki label, rentang tanggal, satuan, tooltip, dan empty state. Jangan menampilkan grafik seolah-olah berisi data nyata bila hanya menggunakan seed/demo data.

---

## 15. Strategi Implementasi Bertahap

### Fase 0 — Persiapan

- Tetapkan framework, database, autentikasi, dan deployment.
- Buat desain skema database dan migrasi awal.
- Definisikan peran dan matriks akses.
- Siapkan design system dan struktur route.
- Siapkan data demo yang jelas ditandai sebagai demo.

**Hasil:** proyek dapat dijalankan lokal, halaman dasar, skema database, dan aturan akses terdokumentasi.

### Fase 1 — MVP Operasional

- Login dan role-based access.
- Pengaturan outlet dasar.
- Pelanggan dan layanan.
- Pembuatan dan pencarian pesanan.
- Alur status dan riwayat status.
- Antrean kerja.
- Pembayaran manual.
- Portal pelanggan.
- Notifikasi dalam aplikasi.
- Dashboard ringkas.
- Audit log dasar.

**Kriteria selesai:** pemilik dan karyawan dapat menjalankan alur pesanan dari penerimaan hingga serah-terima tanpa spreadsheet tambahan untuk proses inti.

### Fase 2 — Pelaporan dan estimasi

- Laporan pesanan dan pembayaran.
- Grafik periode ramai.
- Estimasi berbasis aturan.
- Penghitungan durasi aktual.
- Evaluasi akurasi estimasi.
- Notifikasi perubahan estimasi yang signifikan.

**Kriteria selesai:** estimasi dan laporan memakai data database yang sebenarnya, definisi metrik terdokumentasi, dan data kosong ditangani dengan baik.

### Fase 3 — Integrasi dan optimasi

- Integrasi WhatsApp/email provider.
- Payment gateway.
- QR/barcode dan cetak label.
- Multi-outlet jika dibutuhkan.
- Penyesuaian estimasi menggunakan data historis yang cukup.
- Optimasi performa, monitoring, dan backup.

### Fase 4 — Prediksi lanjutan

- Evaluasi kecukupan data dan kualitas label waktu.
- Bandingkan model dengan baseline berbasis aturan.
- Gunakan validasi pada data yang tidak dipakai untuk pelatihan.
- Pantau error estimasi dan bias antarjenis layanan.
- Aktifkan model hanya jika lebih baik daripada baseline dan dapat dijelaskan.

---

## 16. Rencana Pengujian

### 16.1 Unit test

- Perhitungan harga dan diskon.
- Perhitungan sisa pembayaran.
- Validasi transisi status.
- Perhitungan estimasi yang melewati jam tutup.
- Perhitungan metrik dashboard.
- Otorisasi berdasarkan peran dan outlet.

### 16.2 Integration test

- Membuat pesanan beserta item.
- Menambahkan pembayaran dan memperbarui status pembayaran.
- Mengubah status dan membuat riwayat.
- Membuat notifikasi setelah event tertentu.
- Pembatalan dan koreksi transaksi.
- Penghitungan dashboard dari data database.

### 16.3 End-to-end test

1. Pemilik login dan membuat layanan.
2. Karyawan membuat pelanggan dan pesanan.
3. Karyawan memproses pesanan melalui status yang valid.
4. Pelanggan login dan melihat pesanan miliknya.
5. Sistem menampilkan status siap diambil.
6. Pembayaran dicatat dan status pembayaran diperbarui.
7. Pesanan diserahkan dan ditandai selesai.
8. Pemilik melihat pesanan di laporan.

### 16.4 Pengujian keamanan

- Pelanggan A tidak dapat membuka pesanan pelanggan B.
- Karyawan tidak dapat mengakses halaman pengaturan pemilik.
- Pengguna tanpa login tidak dapat mengakses endpoint privat.
- Payload invalid ditolak.
- Percobaan akses outlet yang tidak diizinkan ditolak.
- Perubahan harga/pembayaran meninggalkan audit log.

### 16.5 Kriteria penerimaan MVP

- Semua peran diarahkan ke dashboard yang tepat.
- Pembuatan order menghasilkan kode unik.
- Status mengikuti workflow dan riwayat tersimpan.
- Harga dan pembayaran konsisten.
- Pelanggan hanya melihat datanya sendiri.
- Dashboard menghitung data nyata dari database.
- Aplikasi dapat digunakan pada layar mobile dan desktop.
- Loading, error, empty, dan success state tersedia.
- Tidak ada secret yang disimpan di source code.
- Migrasi, seed demo, dan petunjuk setup terdokumentasi.

---

## 17. Data Demo dan Seed

Buat data demo secukupnya untuk memperlihatkan seluruh alur, misalnya:
- Satu outlet laundry demo.
- Satu akun owner demo.
- Dua akun staff demo.
- Beberapa pelanggan demo.
- Beberapa layanan dengan harga contoh yang dapat diedit.
- Pesanan pada berbagai status.
- Pembayaran penuh, sebagian, dan belum dibayar.
- Data historis beberapa minggu untuk demonstrasi grafik.

Persyaratan:
- Beri label “DATA DEMO”.
- Jangan gunakan nomor telepon atau email orang nyata.
- Jangan mengisi dashboard produksi dengan data seed.
- Sediakan langkah untuk menghapus/reset data demo dengan aman pada lingkungan development.

---

## 18. Instruksi Implementasi untuk Antigravity

Gunakan dokumen ini sebagai spesifikasi produk dan teknis utama. Bangun aplikasi yang benar-benar berfungsi, bukan sekadar mockup visual.

### 18.1 Instruksi utama

1. Baca seluruh blueprint sebelum membuat perubahan.
2. Buat rencana implementasi dan daftar tugas berdasarkan fase.
3. Tentukan stack teknologi yang konsisten dan jelaskan alasan singkatnya.
4. Bangun fondasi proyek, skema database, migrasi, autentikasi, dan otorisasi terlebih dahulu.
5. Implementasikan fitur secara bertahap, mulai dari alur MVP.
6. Gunakan komponen UI yang dapat digunakan kembali.
7. Buat halaman responsif untuk desktop dan mobile.
8. Hubungkan seluruh form, tabel, tombol, filter, dan grafik ke fungsi yang benar.
9. Gunakan database dan API/server actions nyata; jangan membuat tombol yang hanya dekoratif.
10. Terapkan validasi server dan pemeriksaan akses untuk setiap operasi data.
11. Tambahkan data demo hanya pada development/demo mode.
12. Tulis test untuk aturan bisnis dan alur utama.
13. Jalankan pemeriksaan lint, type check, test, dan build.
14. Perbaiki error sebelum menyatakan fitur selesai.
15. Dokumentasikan variabel lingkungan yang diperlukan menggunakan `.env.example` tanpa nilai rahasia.
16. Buat README berisi instalasi, setup database, migrasi, seed demo, menjalankan aplikasi, pengujian, dan deployment.
17. Jangan mengklaim integrasi email, WhatsApp, payment gateway, atau AI telah aktif sebelum benar-benar terkonfigurasi dan diuji.
18. Jika ada keputusan yang belum ditentukan, pilih default yang aman dan sederhana, dokumentasikan keputusan tersebut, dan jangan menghentikan implementasi untuk pertanyaan kecil yang dapat diputuskan secara wajar.

### 18.2 Urutan implementasi yang disarankan

- Tahap A: project setup, design system, database, autentikasi, RBAC.
- Tahap B: outlet, layanan, pelanggan.
- Tahap C: order creation, order items, kode order, status history.
- Tahap D: antrean dan dashboard operasional.
- Tahap E: pembayaran dan audit log.
- Tahap F: portal pelanggan dan notifikasi internal.
- Tahap G: laporan, periode ramai, dan estimasi berbasis aturan.
- Tahap H: test menyeluruh, responsivitas, keamanan, dokumentasi, dan build produksi.

### 18.3 Definisi “selesai”

Sebuah fitur baru boleh dianggap selesai jika:
- UI tersedia dan responsif.
- Data tersimpan dan dibaca dari database yang benar.
- Validasi sisi server diterapkan.
- Hak akses diuji.
- Loading, error, empty, dan success state tersedia.
- Aturan bisnis penting memiliki test.
- Tidak ada error build/type yang belum diselesaikan.
- Dokumentasi diperbarui.

---

## 19. Ringkasan Prioritas

**Prioritas tertinggi:** pencatatan pesanan, pelacakan status, antrean, pembayaran, dan portal pelanggan.

**Prioritas menengah:** notifikasi otomatis, laporan, dan estimasi berbasis aturan.

**Prioritas lanjutan:** integrasi WhatsApp/payment gateway, multi-outlet, serta model prediksi yang lebih canggih.

Prinsip akhir: LaundryFlow harus lebih dahulu menjadi sistem operasional laundry yang akurat dan dapat dipercaya. Kemampuan analitik dan prediksi akan semakin bermanfaat ketika data operasional telah konsisten dan cukup berkualitas.
