from flask import send_from_directory

from droidapi.app import app

@app.route("/updates/<path:path>")
def media(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)