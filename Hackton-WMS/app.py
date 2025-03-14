from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
from PIL import Image

app = Flask(__name__)

# Dataset Path (Replace with actual path)
DATASET_PATH = "dataset/"

# Waste category recommendations
RECOMMENDATIONS = {
    "plastic": "♻️ Recyclable! Dispose in the recycling bin.",
    "paper": "♻️ Recyclable! Keep dry and place in the paper recycling bin.",
    "glass": "♻️ Recyclable! Place in a glass recycling bin.",
    "metal": "♻️ Recyclable! Send to a metal recycling facility.",
    "cardboard": "♻️ Recyclable! Flatten before recycling.",
    "trash": "🚮 General waste. Dispose in the regular trash bin.",
    "Unknown": "⚠️ Unclassified! Check waste type manually."
}

def load_sample_images():
    """Loads one sample image per waste type from TrashNet."""
    categories = ["plastic", "paper", "glass", "metal", "cardboard", "trash"]
    sample_images = {}

    for category in categories:
        folder_path = os.path.join(DATASET_PATH, category)
        if os.path.exists(folder_path):
            sample_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
            if sample_files:
                sample_images[category] = os.path.join(folder_path, sample_files[0])

    return sample_images

# Load dataset
sample_images = load_sample_images()
def classify_waste(image_path):
    """Compares uploaded image with TrashNet samples using histogram similarity."""
    input_img = cv2.imread(image_path)
    
    if input_img is None:
        return "Unknown"  # If the image couldn't be read
    
    input_img_resized = cv2.resize(input_img, (256, 256))  # Resize to match sample size

    # Convert to HSV (Hue, Saturation, Value) for better color comparison
    input_hsv = cv2.cvtColor(input_img_resized, cv2.COLOR_BGR2HSV)
    input_hist = cv2.calcHist([input_hsv], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])

    best_match = None
    highest_score = 0

    for category, sample_path in sample_images.items():
        sample_img = cv2.imread(sample_path)
        if sample_img is None:
            continue  # Skip if sample image is not found
        
        sample_resized = cv2.resize(sample_img, (256, 256))  # Resize sample to match input image
        sample_hsv = cv2.cvtColor(sample_resized, cv2.COLOR_BGR2HSV)
        sample_hist = cv2.calcHist([sample_hsv], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
        
        # Compare histograms using correlation
        score = cv2.compareHist(input_hist, sample_hist, cv2.HISTCMP_CORREL)

        if score > highest_score:
            highest_score = score
            best_match = category

    # If no match is found or score is low, classify as "Unknown"
    return best_match if highest_score > 0.2 else "Unknown"  # Lowered threshold for better matching

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    # Save the uploaded file
    filepath = "static/uploads/" + file.filename
    file.save(filepath)

    # Classify the uploaded image
    category = classify_waste(filepath)
    recommendation = RECOMMENDATIONS.get(category, "⚠️ No recommendation available.")

    return jsonify({
        "category": category.upper(),
        "recommendation": recommendation,
        "image_url": filepath
    })

if __name__ == "__main__":
    app.run(debug=True)
