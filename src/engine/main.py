from flask import Flask, request, send_file
from flask_cors import CORS
import io
from PIL import Image
import logic

app = Flask(__name__)
CORS(app)

@app.route('/api/enkripsi', methods=['POST'])
def enkripsi():
    if 'gambar' not in request.files:
        return "Gambarnya mana", 400
    
    file = request.files['gambar']
    m1 = int(request.form.get('m1', 255))
    m2 = int(request.form.get('m2', 256))
    m3 = int(request.form.get('m3', 257))
    x_val = float(request.form.get('x', 0.35))
    r_val = float(request.form.get('r', 3.99))

    img = Image.open(file.stream)
    lebar, tinggi = img.size
    
    deret_piksel = logic.bongkar_gambar(img)
    deret_chaotic = logic.generate_logistic_map(x_val, r_val, len(deret_piksel))
    deret_acak = logic.skibiditoilet(deret_piksel, deret_chaotic)
    deret_sandi = logic.proses_difusi(deret_acak, x_val, r_val, m1, m2, m3)
    img_hasil = logic.susun_gambar(deret_sandi, lebar, tinggi)

    img_byte_arr = io.BytesIO()
    img_hasil.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(port=8080, debug=True)