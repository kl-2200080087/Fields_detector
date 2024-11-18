import easyocr
import cv2
import os
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

reader = easyocr.Reader(['en', 'hi', 'ta'])  # English, Hindi, Tamil

def preprocess_image(image_path, adaptive=True):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file does not exist at {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image at {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if adaptive:
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    else:
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        return thresh

def extract_text_with_positions(image_path, confidence_threshold=0.5):
    processed_image = preprocess_image(image_path)
    results = reader.readtext(processed_image)
    return [{"bbox": bbox, "text": text.strip(), "conf": conf} for bbox, text, conf in results if conf > confidence_threshold]

def is_label(text):
    label_keywords = [
        "full name", "name", "sex", "address", "city", "pin code", "state",
        "std code", "phone", "mobile", "email", "district", "centre",
        "date of birth", "dob", "age", "place of birth", "nationality",
        "religion", "father", "husband", "category", "pwd", "training",
        "declaration", "sign", "date", "place"
    ]
    lower_text = text.lower()
    return lower_text.endswith(":") or any(keyword in lower_text for keyword in label_keywords)

def find_label_value_pairs(text_data, distance_threshold=50):
    field_pairs = {}
    labels = [item for item in text_data if is_label(item["text"])]
    values = [item for item in text_data if not is_label(item["text"])]
    for label in labels:
        label_center = np.array(label["bbox"]).mean(axis=0).reshape(1, -1)
        closest_value, min_distance = None, float("inf")
        for value in values:
            value_center = np.array(value["bbox"]).mean(axis=0).reshape(1, -1)
            distance = euclidean_distances(label_center, value_center)[0][0]
            if distance < distance_threshold and distance < min_distance:
                closest_value, min_distance = value["text"], distance
        if closest_value:
            field_pairs[label["text"]] = closest_value
    return field_pairs

def extract_all_fields(image_path):
    try:
        text_data = extract_text_with_positions(image_path)
        fields = find_label_value_pairs(text_data)
        for label, value in fields.items():
            print(f"{label}: {value}")
        return fields
    except Exception as e:
        print(f"Error: {e}")
        return None

image_path = "Your image path"
extracted_fields = extract_all_fields(image_path)
