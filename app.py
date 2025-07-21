from flask import Flask, request, render_template, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        username = secure_filename(request.form["name"])
        files = request.files.getlist("photo")
        user_dir = os.path.join(UPLOAD_FOLDER, username)
        os.makedirs(user_dir, exist_ok=True)
        for f in files:
            if f.filename:
                f.save(os.path.join(user_dir, secure_filename(f.filename)))
        return "Upload complete!"
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
