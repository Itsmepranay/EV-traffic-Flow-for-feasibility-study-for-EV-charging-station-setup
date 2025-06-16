from werkzeug.utils import secure_filename
import os
import cv2
import math
import numpy as np
import base64
import json
from flask import Flask, render_template, request, send_from_directory, Response, redirect, url_for
from ultralytics import YOLO
import time

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
CROPS_FOLDER = 'cropped_ev_plates'
MODEL_PATH = 'best2.pt'
CONF_THRESH = 0.35
GLOBAL_PROX_THRESH = 100

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(CROPS_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

# Create placeholder image
if not os.path.exists('static/placeholder.jpg'):
    img = np.zeros((300, 400, 3), np.uint8)
    cv2.putText(img, "Webcam Feed", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite('static/placeholder.jpg', img)

model = YOLO(MODEL_PATH)

def is_close(box1, box2, thresh):
    x1a, y1a, x2a, y2a = box1
    x1b, y1b, x2b, y2b = box2
    cxa, cya = (x1a + x2a) // 2, (y1a + y2a) // 2
    cxb, cyb = (x1b + x2b) // 2, (y1b + y2b) // 2
    return math.hypot(cxa - cxb, cya - cyb) < thresh

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'video' not in request.files:
            return redirect(request.url)

        file = request.files['video']
        if file.filename == '':
            return redirect(request.url)

        if file and file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                cap = cv2.VideoCapture(filepath)
                if not cap.isOpened():
                    return render_template('index.html', error="Error opening video file")

                fps = cap.get(cv2.CAP_PROP_FPS)
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                processed_filename = f"annotated_{int(time.time())}_{filename}"
                out_path = os.path.join(PROCESSED_FOLDER, processed_filename)
                out_vid = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

                seen_ev_boxes = []
                unique_ev_count = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    result = model.predict(source=frame, conf=CONF_THRESH, verbose=False, save=False)[0]
                    annotated = frame.copy()

                    for i, (box, cls_id) in enumerate(zip(result.boxes.xyxy.cpu().numpy().astype(int),
                                                          result.boxes.cls.cpu().numpy().astype(int))):
                        x1, y1, x2, y2 = box
                        x1, y1 = max(0, x1), max(0, y1)
                        x2, y2 = min(w, x2), min(h, y2)
                        label = model.names[cls_id].upper()

                        if label == 'EV':
                            curr_box = (x1, y1, x2, y2)
                            if not any(is_close(curr_box, prev, GLOBAL_PROX_THRESH) for prev in seen_ev_boxes):
                                seen_ev_boxes.append(curr_box)
                                unique_ev_count += 1
                                crop = frame[y1:y2, x1:x2]
                                crop_filename = os.path.join(CROPS_FOLDER, f"EV_{int(time.time())}_{i}.jpg")
                                cv2.imwrite(crop_filename, crop)

                                # Only annotate new unique EVs
                                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(annotated, label, (x1, y1 - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Draw only the unique EV count
                    cv2.putText(annotated, f"Unique EVs: {unique_ev_count}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    out_vid.write(annotated)

                cap.release()
                out_vid.release()

                return render_template('index.html', count=unique_ev_count, filename=processed_filename)

            except Exception as e:
                return render_template('index.html', error=f"Error processing video: {str(e)}")

    return render_template('index.html', count=None)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/webcam_stream')
def webcam_stream():
    def generate():
        cap = cv2.VideoCapture(0)
        seen_ev_boxes = []
        unique_ev_count = 0

        while True:
            success, frame = cap.read()
            if not success:
                break

            result = model.predict(source=frame, conf=CONF_THRESH, verbose=False, save=False)[0]
            annotated = frame.copy()
            h, w = frame.shape[:2]

            for i, (box, cls_id) in enumerate(zip(result.boxes.xyxy.cpu().numpy().astype(int),
                                                  result.boxes.cls.cpu().numpy().astype(int))):
                x1, y1, x2, y2 = box
                label = model.names[cls_id].upper()

                if label == 'EV':
                    curr_box = (x1, y1, x2, y2)
                    if not any(is_close(curr_box, prev, GLOBAL_PROX_THRESH) for prev in seen_ev_boxes):
                        seen_ev_boxes.append(curr_box)
                        unique_ev_count += 1

                        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(annotated, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.putText(annotated, f"Unique EVs: {unique_ev_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', annotated)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            data = {
                "image": frame_base64,
                "unique_evs": unique_ev_count
            }

            yield f"data: {json.dumps(data)}\n\n"

        cap.release()
        cv2.destroyAllWindows()

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
