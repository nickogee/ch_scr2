from flask import Flask, send_from_directory
from constants import UPLOAD_FOLDER


 # папка для сохранения загруженных файлов
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/uploads/<path:name>")
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], f'{name}.xml', as_attachment=True)


if __name__ == "__main__":
    app.run()
    