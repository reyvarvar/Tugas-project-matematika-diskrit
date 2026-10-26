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