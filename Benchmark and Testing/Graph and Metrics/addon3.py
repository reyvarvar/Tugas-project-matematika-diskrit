import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

def muat_citra_grayscale(path):
    """Memuat citra dan mengonversinya ke Grayscale ('L') untuk analisis statistik standar."""
    try:
        img = Image.open(path).convert('L')
        return np.array(img)
    except FileNotFoundError:
        print(f"[Error] File dengan path '{path}' tidak ditemukan. Periksa kembali nama file Anda.")
        exit()

def hitung_entropi(citra_array):
    """Menghitung Entropi Shannon dari citra (Nilai ideal maksimal = 8.0)."""
    histogram, _ = np.histogram(citra_array.flatten(), bins=256, range=[0, 256])
    probabilitas = histogram / np.sum(histogram)
    probabilitas = probabilitas[probabilitas > 0] # Menghindari log(0)
    entropi = -np.sum(probabilitas * np.log2(probabilitas))
    return entropi

def hitung_korelasi(citra_array, sampel=3000):
    """Menghitung koefisien korelasi piksel bertetangga (Horizontal, Vertikal, Diagonal)."""
    h, w = citra_array.shape
    
    x_hor, y_hor = [], []
    x_ver, y_ver = [], []
    x_diag, y_diag = [], []
    
    for _ in range(sampel):
        r = random.randint(0, h - 2)
        c = random.randint(0, w - 2)
        
        # Horizontal
        x_hor.append(citra_array[r, c])
        y_hor.append(citra_array[r, c + 1])
        
        # Vertikal
        x_ver.append(citra_array[r, c])
        y_ver.append(citra_array[r + 1, c])
        
        # Diagonal
        x_diag.append(citra_array[r, c])
        y_diag.append(citra_array[r + 1, c + 1])
        
    # Kalkulasi Koefisien Korelasi Pearson
    corr_hor = np.corrcoef(x_hor, y_hor)[0, 1]
    corr_ver = np.corrcoef(x_ver, y_ver)[0, 1]
    corr_diag = np.corrcoef(x_diag, y_diag)[0, 1]
    
    return corr_hor, corr_ver, corr_diag

def plot_histogram_perbandingan(asli_array, sandi_array):
    """Menampilkan dan membandingkan grafik histogram citra asli vs citra sandi."""
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.hist(asli_array.flatten(), bins=256, range=[0, 256], color='blue', alpha=0.7)
    plt.title('Histogram Citra Asli (Plain-image)')
    plt.xlabel('Nilai Piksel (0-255)')
    plt.ylabel('Frekuensi')
    
    plt.subplot(1, 2, 2)
    plt.hist(sandi_array.flatten(), bins=256, range=[0, 256], color='red', alpha=0.7)
    plt.title('Histogram Citra Sandi (Cipher-image)')
    plt.xlabel('Nilai Piksel (0-255)')
    plt.ylabel('Frekuensi')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # SESUAIKAN NAMA FILE GAMBAR ANDA DI SINI
    PATH_ASLI = "Pepper.png"
    PATH_SANDI = "hasil_enkripsi_pepper.png"
    
    print("Memproses analisis citra...")
    citra_asli = muat_citra_grayscale(PATH_ASLI)
    citra_sandi = muat_citra_grayscale(PATH_SANDI)
    
    print("\n==============================================")
    print("       HASIL ANALISIS KEUANGAN / METRIK       ")
    print("==============================================")
    
    # 1. Kalkulasi Entropi
    ent_asli = hitung_entropi(citra_asli)
    ent_sandi = hitung_entropi(citra_sandi)
    print(f"1. Entropi Informasi:")
    print(f"   - Citra Asli  : {ent_asli:.5f}")
    print(f"   - Citra Sandi : {ent_sandi:.5f}  (Target ideal: ~7.999)")
    
    # 2. Kalkulasi Korelasi Piksel Bertetangga
    hor_a, ver_a, diag_a = hitung_korelasi(citra_asli)
    hor_s, ver_s, diag_s = hitung_korelasi(citra_sandi)
    print(f"\n2. Koefisien Korelasi Piksel Bertetangga:")
    print(f"   [Horizontal]")
    print(f"     * Asli  : {hor_a:.5f}")
    print(f"     * Sandi : {hor_s:.5f}  (Mendekati 0.0)")
    print(f"   [Vertikal]")
    print(f"     * Asli  : {ver_a:.5f}")
    print(f"     * Sandi : {ver_s:.5f}  (Mendekati 0.0)")
    print(f"   [Diagonal]")
    print(f"     * Asli  : {diag_a:.5f}")
    print(f"     * Sandi : {diag_s:.5f}  (Mendekati 0.0)")
    
    print("\n==============================================")
    print("Membuka jendela visualisasi histogram...")
    plot_histogram_perbandingan(citra_asli, citra_sandi)