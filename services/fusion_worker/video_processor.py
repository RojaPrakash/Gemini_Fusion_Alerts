import cv2
import tempfile
from fusion_worker import process_image

def analyze_video(video_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_bytes)
        video_path = tmp.name

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 10

    results = []
    frame_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process only 1 frame per second
        if frame_index % fps == 0:
            _, jpeg = cv2.imencode(".jpg", frame)
            frame_bytes = jpeg.tobytes()

            detection = process_image(frame_bytes)
            results.append({
                "frame": frame_index,
                "result": detection
            })

            # Alert immediately when danger detected
            if detection.get("detected"):
                break

        frame_index += 1

    cap.release()

    return {
        "frames_processed": len(results),
        "summary": results
    }
