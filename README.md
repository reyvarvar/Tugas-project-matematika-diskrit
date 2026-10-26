# ChaosCRT: Enkripsi & Dekripsi Citra Digital

Aplikasi Kriptografi Citra Digital berbasis Web yang menggabungkan algoritma **Chaos Logistic Map** (Permutasi / *Confusion*) dan **Chinese Remainder Theorem / Teorema Sisa Cina (CRT)** (Difusi / *Diffusion*).

Proyek ini dikembangkan sebagai Tugas Proyek Mata Kuliah **Matematika Diskrit II**, Program Studi Informatika, Universitas Sebelas Maret (UNS).

---

## 👥 Anggota Kelompok

| NIM | Nama Mahasiswa |
| :--- | :--- |
| **L0125009** | DWIANDRA ALFA SYARIF RAMADHAN |
| **L0125025** | MUHAMMAD HAIDAR AMRU |
| **L0125029** | REYHAN DIANDRA ALVARO |
| **L0125057** | NADHIRA KAMALIA ATHIYA RIFA'I |
| **L0125098** | FARRELL LUTHFI ADRIANSYAH |

---

## 📌 Gambaran Umum Program

ChaosCRT mengimplementasikan sistem kriptografi simetris dua tahap untuk mengamankan data gambar:

1. **Tahap Permutasi (Confusion)**: Mengacak posisi spasial piksel citra secara deterministik menggunakan deret bilangan acak semu dari persamaan *Logistic Map*.
2. **Tahap Difusi (Diffusion)**: Mengubah nilai intensitas warna piksel menggunakan kongruensi linier dan sistem kongruensi serempak berdasarkan *Chinese Remainder Theorem* (CRT) dengan modulus yang saling relatif prima.

Program ini menjamin proses rekonstruksi citra saat dekripsi bersifat **100% *Lossless*** (citra asli dapat dipulihkan persis sama tanpa penurunan kualitas).

---

## 🧮 Teori & Konsep Matematika Diskrit

### 1. Chaos Logistic Map
Persamaan polinomial non-linear orde dua yang memodelkan perilaku dinamis dan sensitif terhadap kondisi awal:
$$x_{n+1} = r \cdot x_n \cdot (1 - x_n)$$

- **Kunci Rahasia**: Parameter kondisi awal $x_0 \in (0, 1)$ dan parameter laju pertumbuhan $r \in [3.57, 4.0]$ (zona *chaotic*).
- **Penggunaan**:
  - Menghasilkan deret chaotic sepanjang jumlah piksel untuk mengacak urutan indeks piksel (*pixel shuffling*).
  - Menghasilkan kunci dinamis $(k_1, k_2, k_3)$ untuk proses difusi tiap piksel.

### 2. Teorema Sisa Cina (Chinese Remainder Theorem - CRT)
Diberikan tiga bilangan bulat positif $m_1, m_2, m_3$ yang saling prima berpasangan:
$$\text{FPB}(m_1, m_2) = \text{FPB}(m_1, m_3) = \text{FPB}(m_2, m_3) = 1$$

Syarat penting pada sistem ini:
$$M = m_1 \times m_2 \times m_3 \ge 2^{24} = 16.777.216$$
Syarat ini memastikan ruang kongruensi CRT dapat mencakup seluruh kemungkinan nilai warna piksel 24-bit RGB ($256 \times 256 \times 256$).

#### Enkripsi (Difusi):
Untuk setiap piksel asli $W = (R \ll 16) \mid (G \ll 8) \mid B$:
$$a_1 = (W + k_1) \pmod{m_1}$$
$$a_2 = (W + k_2) \pmod{m_2}$$
$$a_3 = (W + k_3) \pmod{m_3}$$

Solusi tunggal modulo $M$ dihitung dengan rumus CRT:
$$C = \left( a_1 M_1 y_1 + a_2 M_2 y_2 + a_3 M_3 y_3 \right) \pmod{M}$$
di mana $M_i = \frac{M}{m_i}$ dan $y_i = M_i^{-1} \pmod{m_i}$ dihitung menggunakan *Algoritma Euclidean Diperluas*.

#### Dekripsi (Difusi Balik):
Dari nilai sandi $C$:
$$b_1 = (C \pmod{m_1} - k_1) \pmod{m_1}$$
$$b_2 = (C \pmod{m_2} - k_2) \pmod{m_2}$$
$$b_3 = (C \pmod{m_3} - k_3) \pmod{m_3}$$

Dengan merekonstruksi $(b_1, b_2, b_3)$ via CRT, diperoleh kembali nilai piksel asli $W$ secara eksak.

### 3. Penanganan Representasi Citra & RGBA
Karena $M > 2^{24}$, ciphertext $C \in [0, M-1]$ dapat memiliki bit ke-24 bernilai `1` ketika $C \ge 16.777.216$. Citra terenkripsi disimpan dalam format PNG dengan channel Alpha yang diatur solid ($A \in \{254, 255\}$):
- $A = 254$ mewakili bit ke-24 bernilai `0`.
- $A = 255$ mewakili bit ke-24 bernilai `1`.

Metode ini memastikan citra sandi **tidak transparan** (tetap tampil padat sebagai *noise* visual di layar) dan tidak ada bit ciphertext yang hilang.

---

## 📁 Struktur Repositori

```text
├── Engine/
│   ├── logic_update.py      # Implementasi algoritma (Logistic Map, CRT, Invers Modulo, Bit Handler)
│   └── main_update.py       # REST API Backend menggunakan Flask (Endpoint Enkripsi & Dekripsi)
├── frontend/
│   └── index.html           # Tampilan Web UI (Upload gambar, visualisasi preview, tombol download)
├── .gitignore               # Daftar berkas yang diabaikan Git (cache Python, file biner)
└── README.md                # Dokumentasi proyek
```

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Syarat Utama
Pastikan Python 3.8+ telah terinstal pada sistem Anda. Pasang pustaka yang diperlukan:
```bash
pip install flask flask-cors pillow
```

### 2. Menjalankan Backend (Flask API)
Buka terminal dan jalankan server engine:
```bash
python Engine/main_update.py
```
Server akan berjalan secara lokal di: `http://127.0.0.1:8080/`

### 3. Membuka Frontend
Cukup buka berkas `frontend/index.html` langsung di peramban web (browser) favorit Anda (Google Chrome, Mozilla Firefox, Microsoft Edge, dll).

### 4. Menggunakan Aplikasi
1. **Pilih Gambar**: Klik tombol pilih berkas untuk mengunggah gambar yang ingin diamankan.
2. **Atur Parameter (Opsional)**:
   - Nilai default modulus: $m_1 = 256$, $m_2 = 257$, $m_3 = 259$ (saling relatif prima dan $M \ge 2^{24}$).
   - Parameter chaotic: $x = 0.35$, $r = 3.99$.
3. **Enkripsi**: Klik **🔒 Enkripsi**. Gambar terenkripsi akan muncul pada panel hasil.
4. **Unduh**: Klik **📥 Download Gambar Sandi** untuk menyimpan hasil enkripsi berupa PNG.
5. **Dekripsi**: Unggah gambar sandi tersebut kembali, lalu klik **🔓 Dekripsi** untuk mengembalikan gambar ke bentuk aslinya.
