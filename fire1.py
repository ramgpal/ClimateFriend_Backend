from ultralytics import YOLO
import cv2
import math

# Initialize the YOLO model
model = YOLO('new.pt')

# Define class names
classnames = ['fire', 'other', 'smoke']

def detect_objects(input_path):
    detections = []

    def process_frame(frame):
        frame_detections = []
        results = model(frame)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence_percent = math.ceil(confidence * 100)
                Class = int(box.cls[0])

                if confidence_percent > 30 and 0 <= Class < len(classnames):
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    label = classnames[Class]

                    if label != 'Fireman':  # Just in case
                        # Prepare label text
                        text = f"{label} {confidence_percent}%"

                        # Get text size
                        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)

                        # Draw bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)

                        # Draw text background
                        cv2.rectangle(frame, (x1, y1 - text_height - 12), (x1 + text_width + 4, y1), (0, 0, 255), -1)

                        # Draw text
                        cv2.putText(frame, text, (x1 + 2, y1 - 4),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                        frame_detections.append({
                            "label": label,
                            "confidence": confidence_percent,
                            "bbox": [x1, y1, x2, y2]
                        })
        return frame_detections, frame

    if input_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        image = cv2.imread(input_path)
        detections, image_with_boxes = process_frame(image)
        cv2.imshow("Detection Result", image_with_boxes)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif input_path.lower().endswith(('.mp4', '.avi', '.mov')):
        cap = cv2.VideoCapture(input_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_detections, frame_with_boxes = process_frame(frame)
            detections.extend(frame_detections)

            cv2.imshow("Detection Result", frame_with_boxes)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        raise ValueError("Unsupported file format!")

    return detections
