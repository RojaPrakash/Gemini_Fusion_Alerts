# services/cctv_fetcher/cctv_fetcher.py

import os
import time
import requests
import cv2
import base64
from urllib.parse import urlparse
import numpy as np

# ENV variables
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "")
FUSION_URL = os.getenv("FUSION_URL", "http://fusion-worker:8000/upload-image")
SAMPLE_INTERVAL = float(os.getenv("SAMPLE_INTERVAL", "5.0"))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", "1280"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", "720"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))



def is_file_source(src: str):
    return src.startswith("file://")

def is_folder_source(src: str):
    return src.startswith("folder://")



def open_capture(source: str):
    if is_file_source(source):
        path = source[len("file://"):]
        return cv2.VideoCapture(path)
    return cv2.VideoCapture(source)


def send_frame(frame, index=0):
    try:
        ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ret:
            print("[CCTV] JPEG encode failed", flush=True)
            return

        data = jpeg.tobytes()
        files = {"file": (f"frame_{index}.jpg", data, "image/jpeg")}

        print(f"[CCTV] Sending frame {index} to Fusion Worker...", flush=True)
        resp = requests.post(FUSION_URL, files=files, timeout=REQUEST_TIMEOUT)
        print("[CCTV] Fusion response:", resp.status_code, resp.text, flush=True)

    except Exception as e:
        print("[CCTV] Error sending frame:", e, flush=True)


def capture_loop():
    if not CAMERA_SOURCE:
        print("[CCTV] CAMERA_SOURCE not set; exiting.", flush=True)
        return

    print(f"[CCTV] Starting. Source={CAMERA_SOURCE} sample_interval={SAMPLE_INTERVAL}s", flush=True)
    cap = open_capture(CAMERA_SOURCE)

    # If not a valid video capture, fallback to HTTP snapshot
    if cap is None or (hasattr(cap, "isOpened") and not cap.isOpened()):
        print("[CCTV] Could not open source with VideoCapture; trying HTTP snapshot if applicable.", flush=True)
        parsed = urlparse(CAMERA_SOURCE)
        if parsed.scheme in ("http", "https"):
            cap = None
        else:
            return

    last_send = 0.0
    frame_index = 0

    while True:
        start = time.time()


        if cap is not None:
            ret, frame = cap.read()
            if not ret:
                if is_file_source(CAMERA_SOURCE):
                    cap.release()
                    cap = open_capture(CAMERA_SOURCE)
                    time.sleep(1)
                    continue
                print("[CCTV] Frame read failed, retrying...", flush=True)
                time.sleep(1)
                continue

        else:
            try:
                r = requests.get(CAMERA_SOURCE, timeout=10)
                r.raise_for_status()
                np_arr = np.frombuffer(r.content, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is None:
                    print("[CCTV] Failed to decode snapshot", flush=True)
                    time.sleep(1)
                    continue

            except Exception as e:
                print("[CCTV] HTTP snapshot error:", e, flush=True)
                time.sleep(5)
                continue

        if FRAME_WIDTH and FRAME_HEIGHT:
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        now = time.time()
        if now - last_send >= SAMPLE_INTERVAL:
            last_send = now
            frame_index += 1
            send_frame(frame, frame_index)

        elapsed = time.time() - start
        time.sleep(max(0.01, min(SAMPLE_INTERVAL, 0.5 - elapsed)))


def folder_simulation_loop(folder_path):
    print(f"[CCTV] Starting folder frame simulation from: {folder_path}", flush=True)

    if not os.path.exists(folder_path):
        print("[CCTV] Folder does not exist!", flush=True)
        return

    processed = set()
    frame_index = 0

    while True:
        frames = sorted(os.listdir(folder_path))

        for frame in frames:
            full_path = os.path.join(folder_path, frame)

            if frame in processed:
                continue
            if not frame.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            try:
                print(f"[CCTV] Sending folder frame: {frame}", flush=True)

                with open(full_path, "rb") as f:
                    data = f.read()

                files = {"file": (frame, data, "image/jpeg")}
                resp = requests.post(FUSION_URL, files=files, timeout=REQUEST_TIMEOUT)

                print("[CCTV] Fusion response:", resp.status_code, resp.text, flush=True)

                processed.add(frame)
                frame_index += 1
                time.sleep(SAMPLE_INTERVAL)

            except Exception as e:
                print("[CCTV] Folder frame error:", e, flush=True)

        time.sleep(1)  # scan for new frames


if __name__ == "__main__":
    print("[CCTV] CAMERA_SOURCE =", CAMERA_SOURCE, flush=True)

    if is_folder_source(CAMERA_SOURCE):
        folder = CAMERA_SOURCE[len("folder://"):]
        folder_simulation_loop(folder)
    else:
        capture_loop()
