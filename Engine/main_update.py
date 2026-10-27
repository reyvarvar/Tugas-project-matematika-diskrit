from flask import Flask, request, send_file
from flask_cors import CORS
import io
from PIL import Image
import logic_update as logic

app = Flask(__name__)
CORS(app)

def ambil_parameter():
    m1 = int(request.form.get('m1', 256))
    m2 = int(request.form.get('m2', 257))
    m3 = int(request.form.get('m3', 259))
    x_val = float(request.form.get('x', 0.35))
    r_val = float(request.form.get('r', 3.99))
    return m1, m2, m3, x_val, r_val

def modulus_valid(m1, m2, m3):
    return logic.cek_relatif_prima(m1, m2, m3) and m1 * m2 * m3 >= 2**24

def kirim_png(img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/api/enkripsi', methods=['POST'])
def enkripsi():
    if 'gambar' not in request.files:
        return "Gambarnya mana", 400
    try:
        m1, m2, m3, x_val, r_val = ambil_parameter()
    except ValueError:
        return "Parameter harus berupa angka", 400
    if not modulus_valid(m1, m2, m3):
        return "Modulus harus saling prima dan m1*m2*m3 >= 2^24", 400

    img = Image.open(request.files['gambar'].stream)
    lebar, tinggi = img.size

    deret_piksel = logic.bongkar_gambar_rgb(img)
    deret_chaotic = logic.generate_logistic_map(x_val, r_val, len(deret_piksel))
    deret_acak = logic.acak_indeks(deret_piksel, deret_chaotic)
    deret_sandi = logic.proses_difusi(deret_acak, x_val, r_val, m1, m2, m3)
    img_hasil = logic.susun_gambar(deret_sandi, lebar, tinggi, simpan_alpha=True)
    return kirim_png(img_hasil)

@app.route('/api/dekripsi', methods=['POST'])
def dekripsi():
    if 'gambar' not in request.files:
        return "Gambarnya mana", 400
    try:
        m1, m2, m3, x_val, r_val = ambil_parameter()
    except ValueError:
        return "Parameter harus berupa angka", 400
    if not modulus_valid(m1, m2, m3):
        return "Modulus harus saling prima dan m1*m2*m3 >= 2^24", 400

    img = Image.open(request.files['gambar'].stream)
    lebar, tinggi = img.size

    deret_sandi = logic.bongkar_gambar(img)
    deret_chaotic = logic.generate_logistic_map(x_val, r_val, len(deret_sandi))
    deret_acak = logic.proses_difusi_balik(deret_sandi, x_val, r_val, m1, m2, m3)
    deret_asli = logic.permutasi_balik(deret_acak, deret_chaotic)
    img_hasil = logic.susun_gambar(deret_asli, lebar, tinggi, simpan_alpha=False)
    return kirim_png(img_hasil)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
