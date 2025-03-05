import cv2
import os
import datetime

def capture_images(output_dir, num_images=1):
    cap = cv2.VideoCapture(0)  #default camera = 0

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(num_images):
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            continue
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(output_dir, f"vehicle_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        
        metadata_path = os.path.join(output_dir, f"vehicle_{timestamp}_metadata.txt")
        with open(metadata_path, 'w') as f:
            f.write(f"vehicle_image_path: {image_path}\n")
            f.write(f"vehicle_timestamp: {timestamp}\n")

        cv2.imshow('Captured Image', frame)
        cv2.waitKey(10)  # Capture image each second

    cap.release()
    cv2.destroyAllWindows()

# Usage
output_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Result"
capture_images(output_dir) 

