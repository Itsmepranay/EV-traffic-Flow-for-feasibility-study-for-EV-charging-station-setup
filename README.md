# 🔋 EV Plate Detector – Unique EV Counting for Smart Charging Insights

This project is a Flask web application that uses a YOLOv8 object detection model to **detect and count unique Electric Vehicles (EVs)** from uploaded videos or live webcam feeds. It focuses on identifying **unique EV license plates**, making it ideal for analyzing EV traffic flow in specific locations.

> 🎯 **Purpose:**  
> This tool serves as a **feasibility study platform for EV charging station companies and potential franchise owners**, helping them understand EV density and traffic in targeted regions.

---

## 📦 Features

- 🎥 Upload a video to automatically detect and **count unique EVs**  
- 📡 Real-time EV detection via webcam stream with live updates  
- ✅ Avoids duplicate counting using a **centroid proximity check**
- 🧠 Annotates only **new unique EV license plates**
- 💾 Output includes:
  - Processed video with bounding boxes
  - Cropped license plate images
  - Final count of unique EVs displayed on screen  

---

## 🧠 Model Info

- Model: `best2.pt`  
- Framework: [Ultralytics YOLOv8](https://docs.ultralytics.com/)  
- Object Classes: Should include at least one class named `EV`

---

## 🚀 Installation

```bash
# Clone this repo
git clone https://github.com/Itsmepranay/EV-traffic-Flow-for-feasibility-study-for-EV-charging-station-setup.git
cd EV-traffic-Flow-for-feasibility-study-for-EV-charging-station-setup

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📂 Project Structure

```
.
├── app.py                  # Main Flask app
├── best2.pt                # Trained YOLO model
├── uploads/                # Folder for uploaded videos
├── processed/              # Annotated output videos
├── cropped_ev_plates/      # Cropped EV license plates
├── static/
│   └── placeholder.jpg     # Placeholder image for webcam feed
├── templates/
│   └── index.html          # HTML front-end template
├── requirements.txt        # Required Python packages
└── README.md
```

---

## 📝 Requirements

Make sure the following Python libraries are installed:

```
Flask
opencv-python
ultralytics
numpy
```

You can install all with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Example Output

- EVs in the uploaded video are detected and annotated only **once**.
- Final frame displays: `Unique EVs: <count>`

---

## 📌 Notes

- Ensure your YOLO model detects a class named `"EV"` for this to work.
- Duplicates are filtered using centroid-based proximity comparison.

---

## 📃 License

This project is licensed under the MIT License.
