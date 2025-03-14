# WMS - Waste Management System

## Project Overview
**WMS - Waste Management System** is a python-based waste classification system that helps users identify waste types by uploading an image. The system processes the image, compares it with a dataset of known waste categories, and provides classification along with disposal recommendations.

## Features
- Upload an image of waste.
- Classifies waste into **plastic, paper, glass, metal, cardboard, or trash**.
- Uses **OpenCV histogram comparison** for classification.
- Provides **waste disposal recommendations**.
- Web-based UI built with **Flask**.

---

## Installation
### **1. Clone the repository**
```bash
git clone https://github.com/Vitsi/FTL-ML.git
cd Hackton-WMS
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the application**
```bash
python app.py
```

### **4. Open in browser**
Go to `http://127.0.0.1:5000` to use the application.

---

## 🔍 How It Works
### **1. Image Upload & Processing**
- The user uploads an image.
- The image is resized to **256x256 pixels**.
- It is converted to **HSV color space**.
- A **color histogram** is generated.

### **2. Classification via Histogram Matching**
- The uploaded image histogram is compared with sample images.
- The similarity score is computed using **cv2.compareHist()**.
- The category with the highest match is assigned.
- If no strong match is found, it is classified as **Unknown**.

### **3. Waste Disposal Recommendations**
Each waste type has a predefined recommendation, e.g.:
- **Plastic** → ♻️ Recycle in a plastic bin.
- **Glass** → ♻️ Place in a glass recycling bin.

---

## API Endpoints
### **1. Home Page**
`GET /`
- Loads the web interface for image upload.

### **2. Image Classification**
`POST /upload`
- Accepts an image file and returns the waste classification result.

---

## Technologies Used
- **Python** (Flask, OpenCV, NumPy, Pillow)
- **HTML, CSS, JavaScript** (Web UI)
- **Dataset**: Sample waste images from TrashNet.

---

## Future Improvements
- Improve classification accuracy with a **machine learning model**.
- Expand dataset for better recognition.
- Integrate a database for the uploaded images.
- Add Additonal Features.
- Add support for **Video Recognition**.

---

