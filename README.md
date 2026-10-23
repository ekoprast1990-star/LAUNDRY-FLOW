# LaundryFlow - Manajemen Laundry Pintar Berbasis Website
> **Aplikasi Sistem Informasi Manajemen (SIM) Berbasis Web Responsif**  
> Dibuat berdasarkan spesifikasi [Blueprint_LaundryFlow (1).md](file:///c:/Users/ELLO/Documents/KULIAH/3BD/SISTEM%20INFORMASI%20MANAJEMEN/LAUNDRY_FLOW/my-framework/Blueprint_LaundryFlow%20%281%29.md)

---

## 1. Ringkasan Aplikasi

**LaundryFlow** adalah sistem informasi manajemen laundry berbasis website modern yang dirancang untuk mengatasi berbagai kendala operasional laundry konvensional, seperti pencatatan manual yang rentan hilang, pakaian yang sulit dilacak, ketidakpastian estimasi selesai, dan rekap keuangan yang rumit.

Aplikasi ini mencakup **3 Peran Pengguna (RBAC)**:
1. **Pemilik Laundry (`OWNER`)**: Memantau dashboard eksekutif, grafik tren omzet, analitik periode ramai (peak hours), efisiensi kapasitas, katalog tarif, data staf, dan audit log integritas data.
2. **Karyawan / Kasir (`STAFF`)**: Menerima pesanan baru, papan antrean Kanban pipeline operasional, memperbarui status pengerjaan, dan mencatat pembayaran.
3. **Pelanggan (`CUSTOMER`)**: Portal mandiri untuk melacak cucian secara real-time, cek perkiraan selesai, rincian tagihan, struk digital, dan notifikasi status.

---

## 2. Fitur Utama & Kepatuhan Blueprint

| Modul Blueprint | Implementasi Fitur | Status |
|---|---|:---:|
| **Autentikasi & RBAC** | Sesi login berbasis peran, proteksi hak akses, dan **Mode Demo Quick-Switcher** (1-klik beralih peran Pemilik/Karyawan/Pelanggan di navbar) untuk presentasi perkuliahan | Selesai |
| **Estimasi Pintar (Smart Estimation)** | Mesin kalkulasi waktu selesai berbasis aturan (`estimation.py`), memperhitungkan beban antrean aktif, durasi layanan, jam buka-tutup outlet (08.00 - 21.00), dan prioritas express | Selesai |
| **Papan Antrean Kanban** | Pipeline visual 4 kolom: *1. Antrean Masuk*, *2. Sedang Dikerjakan*, *3. Siap Diambil*, *4. Selesai Diserahkan*, dilengkapi tombol aksi cepat pembaruan status | Selesai |
| **Formulir Pesanan (Kasir POS)** | Input pelanggan (pilih pelanggan lama / daftar baru), multi-item layanan (kiloan/satuan), perhitungan otomatis subtotal, diskon, biaya tambahan, snapshot harga, dan pembuatan kode unik otomatis `LF-YYYYMMDD-XXXX` | Selesai |
| **Pelacakan Publik (`/track`)** | Pelacakan mandiri tanpa login melalui kode order atau nomor handphone, dilengkapi progress stepper 6 tahap visual | Selesai |
| **Kasir & Struk Nota Digital** | Pembayaran Tunai, Transfer, dan QRIS Dinamis, status tagihan (Lunas, Sebagian, Belum Lunas), serta template struk thermal 58/80mm siap cetak (`window.print()`) | Selesai |
| **Dashboard & Analitik SIM** | 6 KPI metrik harian, grafik tren harian pesanan & omzet (Chart.js), donat distribusi status, analitik jam sibuk (peak hours), dan rekomendasi pintar alokasi staf | Selesai |
| **Audit Log & Integritas Data** | Pencatatan otomatis setiap tindakan penting (pembuatan order, update status, pembayaran, pembatalan) untuk bukti audit sistem | Selesai |
| **Data Demo Realistis** | Dilengkapi script generator data demo Indonesia yang lengkap (outlet Bandung Dipatiukur, 6 akun pengguna, 8 layanan, 19 transaksi order historis, log status, dan pembayaran) | Selesai |

---

## 3. Struktur Direktori Proyek

```
my-framework/
├── app.py                     # Server Flask & REST API endpoints
├── database.py                # Inisialisasi SQLite database, relasi & skema tabel
├── estimation.py              # Mesin estimasi cerdas (queue load & jam kerja outlet)
├── seed_data.py               # Generator data demo realistis untuk demonstrasi SIM
├── test_api.py                # Script pengujian otomatis endpoint dan aturan bisnis
├── requirements.txt           # Dependensi Python (Flask)
├── run.bat                    # Script 1-klik untuk menjalankan aplikasi di Windows
├── static/
│   ├── css/
│   │   └── style.css          # Design system modern (responsive, Kanban, modal, print struk)
│   └── js/
│       ├── app.js             # Logika frontend, state management, modal, kasir POS
│       └── charts.js          # Visualisasi grafik Chart.js dengan fallback native canvas
└── templates/
    └── index.html             # Tampilan aplikasi web utama (Single-Page App Layout)
```

---

## 4. Cara Menjalankan Aplikasi

### Metode 1: Jalankan File Batch (Paling Mudah)
Cukup klik dua kali pada file **`run.bat`** di folder proyek.

### Metode 2: Jalankan via Terminal / PowerShell
```powershell
# Masuk ke direktori
cd "c:\Users\ELLO\Documents\KULIAH\3BD\SISTEM INFORMASI MANAJEMEN\LAUNDRY_FLOW\my-framework"

# Jalankan server menggunakan virtual environment yang tersedia
.\venv\Scripts\python.exe app.py
```

Buka peramban (browser) di:  
👉 **`http://127.0.0.1:5000`**

---

## 5. Akun Demo Bawaan untuk Presentasi

Aplikasi dilengkapi tombol **"Mode Demo"** di bagian atas kanan halaman untuk langsung beralih peran dalam 1 detik tanpa perlu logout-login:

| Peran | Nama Akun | Email Login | Password | Akses & Wewenang |
|---|---|---|---|---|
| **OWNER** | Pak Budi Hartanto | `owner@laundryflow.id` | `owner123` | Akses penuh dashboard eksekutif, analitik omzet, katalog tarif, jam operasional, audit log, reset demo |
| **STAFF** | Siti Rahayu | `siti@laundryflow.id` | `staff123` | Kasir POS, buat pesanan, geser papan antrean Kanban, catat pembayaran kasir, cetak nota |
| **CUSTOMER** | Rian Pratama | `rian@gmail.com` | `customer123` | Portal khusus melihat pesanan miliknya sendiri, estimasi selesai, rincian biaya, notifikasi |

---

## 6. Contoh Alur Pengujian / Presentasi Tugas

1. **Dashboard & Analitik**: Buka aplikasi sebagai **Pemilik** untuk melihat metrik harian, grafik pendapatan, dan rekomendasi SIM mengenai jam sibuk Sabtu/Minggu.
2. **Papan Antrean (Kanban Pipeline)**: Pindah ke tab *Papan Antrean*, klik tombol **"Lanjut Status →"** pada kartu pesanan untuk memajukan proses dari *Diterima* → *Cuci* → *Kering* → *Setrika* → *Siap Ambil* → *Selesai*.
3. **Penerimaan Pesanan Baru**: Klik menu *Buat Pesanan (Kasir)*, pilih pelanggan, tambahkan layanan (misal Cuci Bed Cover atau Cuci Kiloan), perhatikan bagaimana sistem secara cerdas memperkirakan jam selesai berdasarkan antrean aktif.
4. **Cetak Struk**: Buka rincian pesanan dan klik **"Cetak Struk Nota"** untuk memunculkan format struk thermal kasir yang siap print.
5. **Pelacakan Publik**: Masukkan kode order contoh `LF-20261023-0001` di menu *Lacak Pesanan Publik* untuk melihat progress bar real-time tanpa login.
