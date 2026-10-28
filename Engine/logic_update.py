from PIL import Image


# Cari FPB pakai algoritma Euclidean
def hitung_fpb(a, b):
    if b == 0:
        return a
    return hitung_fpb(b, a % b)


# Pastikan m1, m2, m3 saling koprima (syarat CRT)
def cek_relatif_prima(m1, m2, m3):
    return (
        hitung_fpb(m1, m2) == 1 and hitung_fpb(m1, m3) == 1 and hitung_fpb(m2, m3) == 1
    )


# Cari invers modulo
def invers_modulo(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x


# Rumus utama Chinese Remainder Theorem (CRT)
def china(m1, m2, m3, a1, a2, a3):
    M = m1 * m2 * m3
    M1 = M // m1
    M2 = M // m2
    M3 = M // m3
    y1 = invers_modulo(M1, m1)
    y2 = invers_modulo(M2, m2)
    y3 = invers_modulo(M3, m3)
    return (a1 * M1 * y1 + a2 * M2 * y2 + a3 * M3 * y3) % M


# Bikin deret angka acak chaotic sepanjang jumlah piksel
def generate_logistic_map(x_awal, r, ukuran):
    deret = []
    x = x_awal
    for _ in range(ukuran):
        deret.append(x)
        x = r * x * (1 - x)
    return deret


# Bikin 3 kunci acak dari logistic map buat masing-masing modulus
def logicmap(x, r, m1, m2, m3):
    k = [0, 0, 0]
    x = r * x * (1 - x)
    k[0] = int(x * 1000000) % m1
    x = r * x * (1 - x)
    k[1] = int(x * 1000000) % m2
    x = r * x * (1 - x)
    k[2] = int(x * 1000000) % m3
    return k


# Acak urutan posisi piksel berdasarkan deret chaotic (saat enkripsi)
def acak_indeks(deret_piksel_asli, deret_chaotic):
    indeks = list(range(len(deret_piksel_asli)))
    indeks.sort(key=lambda i: deret_chaotic[i])
    return [deret_piksel_asli[i] for i in indeks]


# Kembalikan posisi piksel ke urutan semula (saat dekripsi)
def permutasi_balik(deret_acak, deret_chaotic):
    indeks = list(range(len(deret_acak)))
    indeks.sort(key=lambda i: deret_chaotic[i])
    asli = [0] * len(deret_acak)
    for posisi, i in enumerate(indeks):
        asli[i] = deret_acak[posisi]
    return asli


# Ubah nilai warna piksel pakai kunci chaotic dan CRT (saat enkripsi)
def proses_difusi(deret_piksel_acak, x_awal, r, m1, m2, m3):
    hasil = []
    x = x_awal
    for warna_asli in deret_piksel_acak:
        kunci = logicmap(x, r, m1, m2, m3)
        a1 = (warna_asli + kunci[0]) % m1
        a2 = (warna_asli + kunci[1]) % m2
        a3 = (warna_asli + kunci[2]) % m3
        hasil.append(china(m1, m2, m3, a1, a2, a3))
        x = r * x * (1 - x)
    return hasil


# Kembalikan nilai warna piksel dari nilai sandi CRT (saat dekripsi)
def proses_difusi_balik(deret_sandi, x_awal, r, m1, m2, m3):
    hasil = []
    x = x_awal
    for c in deret_sandi:
        kunci = logicmap(x, r, m1, m2, m3)
        b1 = (c % m1 - kunci[0]) % m1
        b2 = (c % m2 - kunci[1]) % m2
        b3 = (c % m3 - kunci[2]) % m3
        hasil.append(china(m1, m2, m3, b1, b2, b3))
        x = r * x * (1 - x)
    return hasil


# Baca gambar RGB biasa dan gabung jadi integer 24-bit (dipakai saat enkripsi)
def bongkar_gambar_rgb(img):
    img = img.convert("RGB")
    return [(r << 16) | (g << 8) | b for r, g, b in img.getdata()]


# Baca gambar sandi RGBA dan ambil bit ke-24 dari alpha (dipakai saat dekripsi)
def bongkar_gambar(img):
    has_alpha = img.mode in ("RGBA", "LA")
    img_rgba = img.convert("RGBA")
    deret = []
    for r, g, b, a in img_rgba.getdata():
        if has_alpha:
            if a in (254, 255):
                bit24 = 1 if a == 255 else 0
            elif a in (0, 1):
                bit24 = a
            else:
                bit24 = 0
        else:
            bit24 = 0
        deret.append((bit24 << 24) | (r << 16) | (g << 8) | b)
    return deret


# Ubah deret angka kembali jadi objek gambar RGB atau RGBA
def susun_gambar(deret, lebar, tinggi, simpan_alpha=False):
    if not simpan_alpha:
        img = Image.new("RGB", (lebar, tinggi))
        pixels = [((val >> 16) & 255, (val >> 8) & 255, val & 255) for val in deret]
        img.putdata(pixels)
        return img
    else:
        img = Image.new("RGBA", (lebar, tinggi))
        pixels = []
        for val in deret:
            bit24 = (val >> 24) & 1
            a = 254 + bit24  # 254 jika 0, 255 jika 1 supaya gambar tetap pekat
            r = (val >> 16) & 255
            g = (val >> 8) & 255
            b = val & 255
            pixels.append((r, g, b, a))
        img.putdata(pixels)
        return img

