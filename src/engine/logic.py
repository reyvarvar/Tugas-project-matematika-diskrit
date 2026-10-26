from PIL import Image

def hitung_fpb(a, b):
    if b == 0:
        return a
    return hitung_fpb(b, a % b)

def cek_relatif_prima(m1, m2, m3):
    if hitung_fpb(m1, m2) == 1 and hitung_fpb(m1, m3) == 1 and hitung_fpb(m2, m3) == 1:
        return True
    return False

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

def bongkar_gambar(img):
    img = img.convert('RGBA')
    pixels = list(img.getdata())
    deret = []
    for r, g, b, a in pixels:
        argb = (a << 24) | (r << 16) | (g << 8) | b
        if argb >= 2**31:
            argb -= 2**32
        deret.append(argb)
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
    deret_piksel_acak = [deret_piksel_asli[i] for i in indeks]
    return deret_piksel_acak

def proses_difusi(deret_piksel_acak, x_awal, r, m1, m2, m3):
    deret_piksel_sandi = []
    x = x_awal
    for warna_asli in deret_piksel_acak:
        warna_asli = abs(warna_asli)
        kunci = logicmap(x, r, m1, m2, m3)
        a1 = (warna_asli + kunci[0]) % m1
        a2 = (warna_asli + kunci[1]) % m2
        a3 = (warna_asli + kunci[2]) % m3
        warna_baru = china(m1, m2, m3, a1, a2, a3)
        deret_piksel_sandi.append(warna_baru)
        x = r * x * (1 - x)
    return deret_piksel_sandi

def susun_gambar(deret, lebar, tinggi):
    img = Image.new('RGBA', (lebar, tinggi))
    pixels = []
    for argb in deret:
        if argb < 0:
            argb += 2**32
        a = (argb >> 24) & 255
        r = (argb >> 16) & 255
        g = (argb >> 8) & 255
        b = argb & 255
        pixels.append((r, g, b, a))
    img.putdata(pixels)
    return img.convert('RGB')