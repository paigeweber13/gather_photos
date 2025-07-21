from flask import Flask, request, render_template, redirect, abort, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load shared password from environment variable
SHARED_PASSWORD = os.environ.get("UPLOAD_PASSWORD", "changeme")

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password != SHARED_PASSWORD:
            return "Incorrect password", 403

        username = secure_filename(request.form["name"])
        files = request.files.getlist("photo")
        user_dir = os.path.join(UPLOAD_FOLDER, username)
        os.makedirs(user_dir, exist_ok=True)
        for f in files:
            if f.filename:
                f.save(os.path.join(user_dir, secure_filename(f.filename)))
        return """
  
          <!DOCTYPE html>
          <html>
          <head><title>Upload Complete!</title></head>
          <body>
            <h1> Upload complete! </h1>
            <br>
            <a href="/">Upload Again</a>
            <br>
            <a href="/gallery">View Uploaded Photos</a>
          </body>
          </html>
        """
    return render_template("upload.html")

@app.route("/gallery")
def gallery():
    images = []
    for user in os.listdir(UPLOAD_FOLDER):
        user_dir = os.path.join(UPLOAD_FOLDER, user)
        if os.path.isdir(user_dir):
            for fname in os.listdir(user_dir):
                images.append(f"/uploads/{user}/{fname}")
    return render_template("gallery.html", images=images)

@app.route("/uploads/<username>/<filename>")
def uploaded_file(username, filename):
    user_dir = os.path.join(UPLOAD_FOLDER, secure_filename(username))
    return send_from_directory(user_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
