from flask import Flask, render_template, request, jsonify
import os
import joblib
import uuid
import cv2
from import_cv2 import preprocess_image, extract_hog_feature
import numpy as np

app = Flask(__name__)

# بارگذاری مدل، اسکیلر و PCA
model, scaler, pca = joblib.load("CEDER.pkl")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # دریافت فایل تصویر
        file = request.files.get("file")
        if not file:
            return jsonify({"result": "فایلی ارسال نشده"}), 400

        # ذخیره موقت تصویر
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # پیش‌پردازش و پیش‌بینی
        try:
            img = preprocess_image(filepath)
            features = extract_hog_feature(img).reshape(1, -1)
            features = scaler.transform(features)
            features = pca.transform(features)
            pred = model.predict(features)[0]
            result = "امضا معتبر است ✅" if pred == 0 else "امضا جعلی است ❌"
        except Exception as e:
            result = f"خطا در پردازش تصویر: {e}"

        # پاک کردن فایل موقت
        os.remove(filepath)

        # برگرداندن نتیجه به صورت JSON
        return jsonify({"result": result})

    # برای درخواست GET، صفحه HTML را رندر کن
    return render_template("index.html")
