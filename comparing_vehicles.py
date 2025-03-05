# import cv2
# import numpy as np
# import os

# def recognize_license_plate(image):
#     try:
#         # Convert the image to grayscale
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         # Apply Gaussian blur to reduce noise and improve edge detection
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
#         # Apply adaptive thresholding to handle different lighting conditions
#         adaptive_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                                 cv2.THRESH_BINARY_INV, 11, 2)
        
#         # Find contours in the thresholded image
#         contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
#         # Initialize variables to store the license plate region
#         license_plate_region = None
#         max_area = 0
        
#         # Iterate through the contours
#         for cnt in contours:
#             # Calculate the area of the contour
#             area = cv2.contourArea(cnt)
            
#             # Check if the area is within a reasonable range
#             if 1000 < area < 30000:
#                 # Get the bounding rectangle of the contour
#                 rect = cv2.minAreaRect(cnt)
#                 box = cv2.boxPoints(rect)
#                 box = np.int0(box)
                
#                 # Calculate the aspect ratio of the bounding rectangle
#                 width, height = rect[1]
#                 aspect_ratio = max(width, height) / min(width, height)
                
#                 # Check if the aspect ratio is within the range of a license plate
#                 if 2.2 < aspect_ratio < 5.5:
#                     # Update the license plate region if the area is larger
#                     if area > max_area:
#                         max_area = area
#                         license_plate_region = box
        
#         # If a license plate region was found, draw it on the image and extract the region
#         if license_plate_region is not None:
#             mask = np.zeros_like(gray)
#             cv2.drawContours(mask, [license_plate_region], -1, (255, 255, 255), thickness=cv2.FILLED)
#             result = cv2.bitwise_and(image, image, mask=mask)
            
#             x, y, w, h = cv2.boundingRect(license_plate_region)
#             license_plate_region = result[y:y+h, x:x+w]
#             return license_plate_region
#         else:
#             return None
    
#     except Exception as e:
#         print(f"Error detecting license plate: {e}")
#         return None

# def process_dataset(dataset_folder, output_folder):
#     # Ensure the output folder exists
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     # Process each image in the dataset folder
#     for filename in os.listdir(dataset_folder):
#         if filename.endswith(('.jpg', '.jpeg', '.png')):
#             image_path = os.path.join(dataset_folder, filename)
#             image = cv2.imread(image_path)
            
#             license_plate_region = detect_license_plate(image)
            
#             if license_plate_region is not None:
#                 output_path = os.path.join(output_folder, filename)
#                 cv2.imwrite(output_path, license_plate_region)
#                 print(f"License plate detected and saved: {output_path}")
#             else:
#                 print(f"License plate detection failed for: {filename}")

# # Define paths
# dataset_folder = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Result"
# output_folder = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Detected"

# # Process the dataset
# process_dataset(dataset_folder, output_folder)


# import cv2
# import easyocr

# def recognize_license_plate(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Failed to load image {image_path}.")
    
#     # Preprocess the image for OCR
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
#     # Perform OCR using EasyOCR
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(binary_image)
    
#     license_plates = []
#     for (bbox, text, prob) in results:
#         license_plates.append(text)
    
#     return license_plates

# def match_vehicle(captured_image_path, existing_metadata):
#     # Recognize license plate from the captured image
#     captured_license_plates = recognize_license_plate(captured_image_path)
    
#     for captured_plate in captured_license_plates:
#         for _, row in existing_metadata.iterrows():
#             existing_license_plate = row['License-plate']
#             if captured_plate == existing_license_plate:
#                 return {
#                     'match': True,
#                     'existing_data': row.to_dict()
#                 }
    
#     return {'match': False}

import cv2
import easyocr

def correct_license_plate(text):
    # Implement your logic here for text correction if required
    corrected_text = text.upper().replace(' ', '').replace('-', '')
    return corrected_text

def recognize_license_plate(image_path, approved_db):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image {image_path}.")
    
    # Preprocess the image for OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Perform OCR using EasyOCR
    reader = easyocr.Reader(['en'])
    results = reader.readtext(binary_image)
    
    license_plates = []
    for (bbox, text, prob) in results:
        corrected_text = correct_license_plate(text)  # Ensure the text is formatted correctly
        license_plates.append(corrected_text)
    
    # Check authorization status
    for plate in license_plates:
        if plate in approved_db:
            return plate, "Authorized"
    
    return license_plates[0] if license_plates else "Unknown", "Unauthorized"