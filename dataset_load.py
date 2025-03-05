# import os
# import pandas as pd
# import cv2
# import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def load_metadata(data_dir):
#     records = []
#     for filename in os.listdir(data_dir):
#         if filename.endswith("_metadata.txt"):
#             with open(os.path.join(data_dir, filename), 'r') as f:
#                 metadata = {}
#                 for line in f:
#                     try:
#                         key, value = line.strip().split(": ", 1)
#                         metadata[key.strip()] = value.strip()
                        
#                     except ValueError:
#                         logging.warning(f"Skipping line in {filename}: {line.strip()}")

#                 if 'vehicle_timestamp' in metadata:
#                     try:
#                         # Convert timestamp to datetime format explicitly
#                         metadata['vehicle_timestamp'] = pd.to_datetime(metadata['vehicle_timestamp'], format="%Y%m%d_%H%M%S")
#                     except ValueError:
#                         print(f"Error: Parsing timestamp in file {filename}")
#                 else:
#                     print(f"Warning: 'vehicle_timestamp' not found in file: {filename}")

#                 # Ensure the 'vehicle_image_path' is in metadata and valid
#                 if 'vehicle_image_path' not in metadata:
#                     print(f"Warning: 'vehicle_image_path' not found in file: {filename}")
#                 else:
#                     image_path = os.path.join(data_dir, metadata['vehicle_image_path'])
#                     if not os.path.exists(image_path):
#                         print(f"Warning: Image path {image_path} does not exist.")
#                     else:
#                         records.append(metadata)

#     return pd.DataFrame(records)

# def display_sample_image(image_path):
#     if not os.path.exists(image_path):
#         print(f"Error: The file {image_path} does not exist.")
#         return
    
#     image = cv2.imread(image_path)
#     if image is None:
#         print(f"Error: Failed to load image {image_path}.")
#         return
    
#     cv2.imshow('Sample Image', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # Usage
# if __name__ == "__main__":
#     data_dir = "data/vehicle_images"
#     metadata = load_metadata(data_dir)
    
#     if not metadata.empty:
#         print(metadata.head())
#         first_image_path = os.path.join(data_dir, metadata.iloc[0]['vehicle_image_path'])
#         display_sample_image(first_image_path)
#     else:
       
#       print("No metadata found.")


import os
import pandas as pd
import cv2

def load_metadata(data_dir):
    records = []
    timestamp_formats = ["%Y-%m-%d %H:%M:%S", "%Y%m%d_%H%M%S", "%Y%m%d_%H%M", "%Y-%m-%d %H:%M", "%Y%m%d_%H%M%S"]  # Add more formats if needed

    for filename in os.listdir(data_dir):
        if filename.endswith("_metadata.txt"):
            with open(os.path.join(data_dir, filename), 'r') as f:
                metadata = {}
                for line in f:
                    try:
                        key, value = line.strip().split(": ")
                        metadata[key.strip()] = value.strip()
                    except ValueError:
                        continue  # Handle lines that don't split correctly

                if 'vehicle_timestamp' in metadata:
                    timestamp_str = metadata['vehicle_timestamp']
                    parsed = False
                    for fmt in timestamp_formats:
                        try:
                            metadata['vehicle_timestamp'] = pd.to_datetime(timestamp_str, format=fmt)
                            parsed = True
                            break
                        except ValueError:
                            continue
                    if not parsed:
                        print(f"Error parsing timestamp in file {filename} with value {timestamp_str}")
                        metadata['vehicle_timestamp'] = pd.NaT  # Set to NaT if parsing fails
                    
                if 'vehicle_image_path' in metadata:
                    image_path = metadata['vehicle_image_path']
                    if not os.path.exists(image_path):
                        print(f"Warning: Image path {image_path} does not exist.")
                        metadata['vehicle_image_path'] = None  # Set to None if the image does not exist

                records.append(metadata)

    return pd.DataFrame(records)
