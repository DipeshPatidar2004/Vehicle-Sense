from flask import Flask, render_template, request
from ultralytics import YOLO
import os

app = Flask(__name__)

model = YOLO("yolov8n.pt")

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# allowed vehicle classes
vehicle_classes = ["bicycle", "car", "motorcycle", "bus", "truck"]

@app.route("/", methods=["GET", "POST"])
def index():

    detected_names = []

    if request.method == "POST":

        file = request.files["image"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            results = model(filepath)

            for box in results[0].boxes.cls:
                class_id = int(box)
                name = model.names[class_id]

                # filter only vehicles
                if name in vehicle_classes:
                    detected_names.append(name)

    return render_template("index.html", names=detected_names)


if __name__ == "__main__":
    app.run(debug=True)