# 🔋 EV Plate Detector: Count Unique Electric Vehicles from Videos & Live Feed

This project is a Flask web application that uses a YOLOv8 object detection model to **detect and count unique Electric Vehicles (EVs)** from uploaded videos or a live webcam feed. It annotates only **new unique EV license plates**, avoiding duplicates using a proximity-based comparison.

The app provides both:
- 🎥 Annotated video output with bounding boxes and unique EV count
- 📷 Real-time webcam EV detection with live updates via SSE (Server-Sent Events)

---

## 📁 Features

- Upload a video and process it to count **unique EV license plates**  
- Detect EVs from live webcam feed in real-time  
- Bounding box annotations only for **new** EVs (avoids duplicates)  
- Final output includes:
  - Annotated video for download
  - Cropped EV license plate images
  - Unique EV count shown on screen  
- Built using **YOLOv8**, **OpenCV**, and **Flask**

---

## 🧠 Model Info

- Model: `best2.pt`  
- Framework: [Ultralytics YOLOv8](https://docs.ultralytics.com/)  
- Object Classes: Should include at least one class named `EV`

---

## 🚀 Installation

```bash
# Clone this repo
git clone https://github.com/your-username/ev-plate-detector.git
cd ev-plate-detector

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