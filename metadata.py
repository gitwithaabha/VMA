import os
from datetime import datetime

# Path to the directory containing the images
image_directory = r"C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\vehicle_images\\vehicle_images"

# Dictionary to manually set timestamps for each image
manual_timestamps = {
    "vehicle1.jpg": "2024-07-08 10:00:00",
    "vehicle2.jpg": "2024-07-08 10:05:00",
    "vehicle3.jpg": "2024-07-08 10:10:00",
    "vehicle4.jpg": "2024-07-08 10:15:00",
    "vehicle5.jpg": "2024-07-08 10:20:00",
    "vehicle6.jpg": "2024-07-08 10:25:00",
    "vehicle7.jpg": "2024-07-08 10:30:00",
    "vehicle8.jpg": "2024-07-08 10:35:00",
    "vehicle9.jpg": "2024-07-08 10:40:00",
    "vehicle10.jpg": "2024-07-08 10:45:00",
    "vehicle11.jpg": "2024-07-08 10:50:00",
    "vehicle12.jpg": "2024-07-08 10:55:00",
    "vehicle13.jpg": "2024-07-08 11:00:00",
    "vehicle14.jpg": "2024-07-08 11:05:00",
    "vehicle15.jpg": "2024-07-08 11:10:00",
    "vehicle16.jpg": "2024-07-08 11:15:00",
    "vehicle17.jpg": "2024-07-08 11:20:00",
}

# Function to add metadata file with timestamp
def add_metadata_to_images(directory, timestamps):
    for image_file in os.listdir(directory):
        # Check if the file is a JPEG image
        if image_file.endswith(".jpg"):
            # Use the manually set timestamp or default to current time
            timestamp = timestamps.get(image_file, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Create a metadata filename with "_metadata.txt"
            base_name = os.path.splitext(image_file)[0]
            metadata_filename = base_name + "_metadata.txt"
            metadata_path = os.path.join(directory, metadata_filename)
            
            # Write the timestamp to the metadata file
            with open(metadata_path, 'w') as metadata_file:
                metadata_file.write(f"vehicle_image_path: {os.path.join(directory, image_file)}\n")
                metadata_file.write(f"vehicle_timestamp: {timestamp}\n")
            
            print(f"Created {metadata_filename} with timestamp {timestamp}")

# Call the function to add metadata to all images in the directory
add_metadata_to_images(image_directory, manual_timestamps)

print("Metadata files with timestamps have been added for all images.")