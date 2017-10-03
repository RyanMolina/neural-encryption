from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import base64
import restore_model
import argparse
import os

app = Flask(__name__)


@app.route('/')
def homepage():
    print("Homepage")
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    file, key = get_data(request, 'input_image', 'encryption_key')
    return enc_dec_process(file, "encrypt", key)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    file, key = get_data(request, 'input_image', 'encryption_key')
    return enc_dec_process(file, "decrypt", key)

def get_data(request, filename, fieldname):
    file = request.files[filename]
    key = request.form[fieldname]
    return file, key


def enc_dec_process(file, process, key):
    file.save(secure_filename(file.filename))
    processed = restore_model.process(file, frozen_model, process, key)
    os.remove(file.filename)
    return jsonify({"output_image": "data:image/" 
                   + (os.path.splitext(file.filename)[1])[1:]
                   + ";base64," 
                   + str(base64.b64encode(processed))[2:-1], 
                   "output_filename": file.filename})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frozen_model_filename', 
                        default="./frozen_model.pb", 
                        type=str, 
                        help="Frozen model filename")
    args = parser.parse_args()
    frozen_model = args.frozen_model_filename
    app.run(debug=True, use_reloader=True)
