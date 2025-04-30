from flask import Flask, render_template, request, jsonify
import os, joblib, uuid
import cv2
import numpy as np
from import_cv2 import preprocess_image, extract_hog_feature  # ماژولی که ساختی
from pathlib import Path

app = Flask(__name__)
model, scaler, pca = joblib.load("CEDER.pkl")

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
                features = scaler.transform(features)
                features = pca.transform(features)
                prediction = model.predict(features)[0]
                result = "امضا معتبر است ✅" if prediction == 1 else "امضا جعلی است ❌"
            except Exception as e:
                result = f"خطا: {str(e)}"

            os.remove(filepath)

            # اگر انتظار JSON از سمت JS هست:
            if request.accept_mimetypes['application/json']:
                return jsonify({"result": result})
    
    return render_template("index.html", result=result)
