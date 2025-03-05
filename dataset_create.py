

# import cv2
# import os
# import datetime
# import pytesseract
# import pandas as pd

# # Set up Tesseract OCR (Update the path if necessary)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Load the pre-trained Haar cascade for license plate detection
# plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# def load_metadata(data_dir):
#     records = []
#     for filename in os.listdir(data_dir):
#         if filename.endswith("_metadata.txt"):
#             with open(os.path.join(data_dir, filename), 'r') as f:
#                 metadata = {}
#                 for line in f:
#                     try:
#                         key, value = line.strip().split(": ")
#                         metadata[key.strip()] = value.strip()
#                     except ValueError:
#                         continue
#                 records.append(metadata)
#     return pd.DataFrame(records)

# def save_metadata(metadata_path, image_path, timestamp, license_plate, status):
#     with open(metadata_path, 'a') as f:
#         f.write(f"vehicle_image_path: {image_path}\n")
#         f.write(f"vehicle_timestamp: {timestamp}\n")
#         f.write(f"license_plate: {license_plate}\n")
#         f.write(f"status: {status}\n")

# def capture_images(output_dir, num_images=1):
#     cap = cv2.VideoCapture(0)  # Default camera = 0

#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return

#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     # Load existing metadata
#     metadata_df = load_metadata(output_dir)

#     # Initialize occupancy count
#     occupancy_count = len(metadata_df)

#     for i in range(num_images):
#         print(f"Capturing image {i+1}... Please hold the camera steady.")
#         ret, frame = cap.read()
#         if not ret:
#             print(f"Error: Failed to capture image {i+1}")
#             continue
        
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         image_path = os.path.join(output_dir, f"vehicle_{timestamp}.jpg")
#         cv2.imwrite(image_path, frame)

#         # License plate detection
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 30))

#         license_plate_text = "Unknown"
#         if len(plates) > 0:
#             for (x, y, w, h) in plates:
#                 plate_img = gray[y:y + h, x:x + w]  # Crop detected license plate
#                 plate_img = cv2.resize(plate_img, (300, 100))  # Resize for better OCR accuracy
#                 _, plate_img = cv2.threshold(plate_img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#                 # Perform OCR
#                 license_plate_text = pytesseract.image_to_string(plate_img, config='--psm 7')
#                 license_plate_text = ''.join(filter(str.isalnum, license_plate_text))  # Clean the text

#         # Check authorization status
#         if license_plate_text != "Unknown":
#             if any(metadata_df['license_plate'].str.contains(license_plate_text)):
#                 status = "Authorized"
#             else:
#                 status = "Unauthorized"
#                 # Add unauthorized plate to metadata
#                 save_metadata(os.path.join(output_dir, f"unauthorized_metadata.txt"), image_path, timestamp, license_plate_text, status)
#         else:
#             status = "Failed to detect license plate"

#         # Save metadata
#         metadata_path = os.path.join(output_dir, f"vehicle_{timestamp}_metadata.txt")
#         save_metadata(metadata_path, image_path, timestamp, license_plate_text, status)

#         print(f"Saved: {image_path} (Plate: {license_plate_text}, Status: {status})")

#         # Update occupancy count
#         if status == "Authorized":
#             occupancy_count += 1

#     cap.release()
#     cv2.destroyAllWindows()

#     # Calculate and display parking occupancy
#     total_spots = 50  # Example total parking spots
#     occupancy_rate = (occupancy_count / total_spots) * 100
#     print(f"Parking Occupancy: {occupancy_count}/{total_spots} ({occupancy_rate:.2f}%)")

# # Usage
# output_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Result"
# capture_images(output_dir, num_images=1)  # Capture 1 image


import cv2
import os
import datetime
import pytesseract
import pandas as pd

# Set up Tesseract OCR (Update the path if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the pre-trained Haar cascade for license plate detection
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

def load_metadata(data_dir):
    """Load metadata from the specified directory."""
    records = []
    for filename in os.listdir(data_dir):
        if filename.endswith("_metadata.txt"):
            with open(os.path.join(data_dir, filename), 'r') as f:
                metadata = {}
                for line in f:
                    try:
                        key, value = line.strip().split(": ")
                        metadata[key.strip()] = value.strip()
                    except ValueError:
                        continue
                records.append(metadata)
    return pd.DataFrame(records)

def save_metadata(metadata_path, image_path, timestamp, license_plate, status):
    """Save metadata to a file."""
    with open(metadata_path, 'a') as f:
        f.write(f"vehicle_image_path: {image_path}\n")
        f.write(f"vehicle_timestamp: {timestamp}\n")
        f.write(f"license_plate: {license_plate}\n")
        f.write(f"status: {status}\n")

def preprocess_image(plate_img):
    """Preprocess the license plate image for better OCR accuracy."""
    # Convert to grayscale
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    return thresh

def extract_license_plate_text(image):
    """Extract license plate text from the given image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 30))
    
    license_plate_texts = []
    for (x, y, w, h) in plates:
        plate_img = image[y:y + h, x:x + w]  # Crop detected license plate
        plate_img = cv2.resize(plate_img, (300, 100))  # Resize for better OCR accuracy
        processed_plate_img = preprocess_image(plate_img)  # Preprocess the image

        # Perform OCR
        license_plate_text = pytesseract.image_to_string(processed_plate_img, config='--psm 8')
        license_plate_text = ''.join(filter(str.isalnum, license_plate_text))  # Clean the text
        if license_plate_text:  # Only add if text is not empty
            license_plate_texts.append(license_plate_text)

    return license_plate_texts

def extract_existing_license_plates(existing_images_dir):
    """Extract license plate texts from existing images in the specified directory."""
    existing_license_plates = []
    for filename in os.listdir(existing_images_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            existing_image_path = os.path.join(existing_images_dir, filename)
            existing_image = cv2.imread(existing_image_path)
            license_plate_texts = extract_license_plate_text(existing_image)
            existing_license_plates.extend(license_plate_texts)  # Add all detected plates
    return existing_license_plates

def capture_images(output_dir, num_images=1):
    """Capture images from the camera and process them."""
    cap = cv2.VideoCapture(0)  # Default camera = 0

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Directory containing existing vehicle images for comparison
    existing_images_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\vehicle_images"
    existing_license_plates = extract_existing_license_plates(existing_images_dir)

    for i in range(num_images):
        print(f"Capturing image {i+1}... Please hold the camera steady.")
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Failed to capture image {i+1}")
            continue
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(output_dir, f"vehicle_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)

        # Extract license plate texts from the captured image
        captured_license_plate_texts = extract_license_plate_text(frame)

        # Check authorization status by comparing license plate text
        status = "Unauthorized"
        for captured_license_plate_text in captured_license_plate_texts:
            if captured_license_plate_text in existing_license_plates:
                status = "Authorized"
                break  # No need to check further if one match is found

        # Save metadata
        metadata_path = os.path.join(output_dir, f"vehicle_{timestamp}_metadata.txt")
        save_metadata(metadata_path, image_path, timestamp, ', '.join(captured_license_plate_texts), status)

        print(f"Saved: {image_path} (Plates: {', '.join(captured_license_plate_texts)}, Status: {status})")

    cap.release()
    cv2.destroyAllWindows()

# Usage
output_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Result"
capture_images(output_dir, num_images=1)  # Capture 1 image