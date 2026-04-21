from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

vehicle_classes = ["bicycle", "car", "motorcycle", "bus", "truck"]

@app.route("/", methods=["GET", "POST"])
def index():

    detected_names = []

    if request.method == "POST":

        file = request.files.get("image")

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # 🔥 FAKE / DEMO detection (replace later with API)
            detected_names = ["car", "truck"]

    return render_template("index.html", names=detected_names)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
