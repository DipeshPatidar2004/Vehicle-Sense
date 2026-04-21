from flask import Flask, render_template, request
from ultralytics import YOLO
import os

app = Flask(__name__)

# Upload folder setup
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Lazy load model (IMPORTANT)
model = None

def get_model():
    global model
    if model is None:
        model = YOLO("yolov8n.pt")
    return model

# allowed vehicle classes
vehicle_classes = ["bicycle", "car", "motorcycle", "bus", "truck"]

@app.route("/", methods=["GET", "POST"])
def index():

    detected_names = []

    if request.method == "POST":

        file = request.files.get("image")

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            model = get_model()  # load here (not at startup)
            results = model(filepath)

            for box in results[0].boxes.cls:
                class_id = int(box)
                name = model.names[class_id]

                if name in vehicle_classes:
                    detected_names.append(name)

    return render_template("index.html", names=detected_names)


# IMPORTANT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
