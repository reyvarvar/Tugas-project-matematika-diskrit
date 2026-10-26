from PIL import Image

def hitung_fpb(a, b):
    if b == 0:
        return a
    return hitung_fpb(b, a % b)

def cek_relatif_prima(m1, m2, m3):
    return hitung_fpb(m1, m2) == 1 and hitung_fpb(m1, m3) == 1 and hitung_fpb(m2, m3) == 1

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

def china(m1, m2, m3, a1, a2, a3):
    M = m1 * m2 * m3
    M1 = M // m1
    M2 = M // m2
    M3 = M // m3
    y1 = invers_modulo(M1, m1)
    y2 = invers_modulo(M2, m2)
    y3 = invers_modulo(M3, m3)
    return (a1 * M1 * y1 + a2 * M2 * y2 + a3 * M3 * y3) % M

def logicmap(x, r, m1, m2, m3):
    k = [0, 0, 0]
    x = r * x * (1 - x)
    k[0] = int(x * 1000000) % m1
    x = r * x * (1 - x)
    k[1] = int(x * 1000000) % m2
    x = r * x * (1 - x)
    k[2] = int(x * 1000000) % m3
    return k

# Baca gambar RGB biasa (dipakai saat ENKRIPSI)
def bongkar_gambar_rgb(img):
    img = img.convert('RGB')
    return [(r << 16) | (g << 8) | b for r, g, b in img.getdata()]

# Baca gambar RGBA (dipakai saat DEKRIPSI)
def bongkar_gambar(img):
    img = img.convert('RGBA')
    deret = []
    for r, g, b, a in img.getdata():
        deret.append((a << 24) | (r << 16) | (g << 8) | b)
    return deret

def generate_logistic_map(x_awal, r, ukuran):
    deret = []
    x = x_awal
    for _ in range(ukuran):
        deret.append(x)
        x = r * x * (1 - x)
    return deret

def skibiditoilet(deret_piksel_asli, deret_chaotic):
    indeks = list(range(len(deret_piksel_asli)))
    indeks.sort(key=lambda i: deret_chaotic[i])
    return [deret_piksel_asli[i] for i in indeks]

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

def permutasi_balik(deret_acak, deret_chaotic):
    indeks = list(range(len(deret_acak)))
    indeks.sort(key=lambda i: deret_chaotic[i])
    asli = [0] * len(deret_acak)
    for posisi, i in enumerate(indeks):
        asli[i] = deret_acak[posisi]
    return asli

def susun_gambar(deret, lebar, tinggi, simpan_alpha=False):
    img = Image.new('RGBA', (lebar, tinggi))
    pixels = []
    for argb in deret:
        a = (argb >> 24) & 255
        r = (argb >> 16) & 255
        g = (argb >> 8) & 255
        b = argb & 255
        pixels.append((r, g, b, a))
    img.putdata(pixels)
    return img if simpan_alpha else img.convert('RGB')
