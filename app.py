from flask import Flask, render_template, request, redirect, url_for
import os
import base64
import cv2
import numpy as np
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"

# Define the class names
class_names = [
    "produk",
    "Biskuit Selamat",
    "Chiki Twist",
    "Chitato Lite",
    "Chitato Sapi",
    "Fitbar",
    "Nissin Crackers",
    "Pocari",
    "Pop Mie",
    "Roma Kelapa",
    "Teh Botol",
]

# Register metadata
MetadataCatalog.get("custom_dataset").thing_classes = class_names

# Set up the Detectron2 configuration
cfg = get_cfg()
cfg.merge_from_file("saved_model/config.yaml")  # Configuration model
cfg.MODEL.WEIGHTS = "saved_model/model.pth"  # Model weights
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Threshold confidence score
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 11  # Number of classes
cfg.MODEL.DEVICE = "cpu"  # Use CPU for inference

# Create predictor object for prediction
predictor = DefaultPredictor(cfg)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        processed_image_path, detected_items = detect_objects(filepath)
        return render_template(
            "result.html", filename=processed_image_path, detected_items=detected_items
        )


@app.route("/capture", methods=["POST"])
def capture():
    image_data = request.form["image"]
    image_data = base64.b64decode(image_data.split(",")[1])
    raw_image_path = os.path.join(app.config["UPLOAD_FOLDER"], "captured_image.png")
    with open(raw_image_path, "wb") as f:
        f.write(image_data)
    processed_image_path, item_name, item_count = detect_objects(raw_image_path)
    print(processed_image_path)
    return render_template(
        "result.html",
        filename=processed_image_path,
        item_name=item_name,
        item_count=item_count,
    )


def detect_objects(image_path):
    im = cv2.imread(image_path)
    outputs = predictor(im)

    # Get the predicted class IDs and counts
    instances = outputs["instances"].to("cpu")
    class_ids = instances.pred_classes.numpy()
    unique, counts = np.unique(class_ids, return_counts=True)

    # Map class IDs to class names
    class_names = MetadataCatalog.get("custom_dataset").thing_classes
    detected_items = [
        [class_names[int(cls_id)], count] for cls_id, count in zip(unique, counts)
    ]

    # Create a visualizer and draw the predictions on the image
    v = Visualizer(
        im[:, :, ::-1], metadata=MetadataCatalog.get("custom_dataset"), scale=2.0
    )
    out = v.draw_instance_predictions(instances)

    processed_image_path = os.path.join(
        app.config["UPLOAD_FOLDER"], "processed_" + os.path.basename(image_path)
    )
    cv2.imwrite(
        processed_image_path, out.get_image()[:, :, ::-1]
    )  # Save the image with detections

    return processed_image_path, detected_items


if __name__ == "__main__":
    app.run(debug=True)
