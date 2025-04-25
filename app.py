
from flask import Flask, render_template, request
import os
import joblib
import uuid
import cv2
from import_cv2 import preprocess_image, extract_hog_feature
import numpy as np

app = Flask(__name__)
model = joblib.load("CEDER.pkl")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = str(uuid.uuid4()) + ".png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                img = preprocess_image(filepath)
                features = extract_hog_feature(img).reshape(1, -1)
                prediction = model.predict(features)[0]
                result = "امضا معتبر است ✅" if prediction == 1 else "امضا جعلی است ❌"
            except Exception as e:
                result = "خطا در پردازش تصویر"

            os.remove(filepath)
    return render_template("index.html", result=result)
