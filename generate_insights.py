# # Module: generate_insights.py
# import pandas as pd

# def generate_insights(metadata):
#     # Example insights
#     vehicle_entry_exit_times = metadata[['vehicle_image_path', 'vehicle_timestamp']]
#     avg_parking_occupancy = metadata['vehicle_timestamp'].dt.hour.value_counts().mean()
    
#     insights = {
#         "Vehicle Entry and Exit Times": vehicle_entry_exit_times,
#         "Average Parking Occupancy": avg_parking_occupancy
#     }
    
#     return insights

# if __name__ == "_main_":
#     from dataset_load import load_metadata
    
#     # Load metadata
#     #data_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\vehicle_images"
#     data_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Result"
#     metadata = load_metadata(data_dir)
    
#     if not metadata.empty:
#         insights = generate_insights(metadata)
        
#         # Print insights
#         for key, value in insights.items():
#             print(f"{key}:\n{value}\n")
#     else:
#         print("No metadata found.")

import pandas as pd

def generate_insights(metadata):
    # Convert the 'vehicle_timestamp' column to datetime format
    metadata['vehicle_timestamp'] = pd.to_datetime(metadata['vehicle_timestamp'], format='%Y%m%d_%H%M%S', errors='coerce')

    # Example insights
    vehicle_entry_exit_times = metadata[['vehicle_image_path', 'vehicle_timestamp']]
    avg_parking_occupancy = metadata['vehicle_timestamp'].dt.hour.value_counts().mean()

    insights = {
        "Vehicle Entry and Exit Times": vehicle_entry_exit_times,
        "Average Parking Occupancy": avg_parking_occupancy
    }

    return insights

if __name__ == "__main__":
    from dataset_load import load_metadata

    # Load metadata
    data_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Result"
    metadata = load_metadata(data_dir)

    if not metadata.empty:
        insights = generate_insights(metadata)

        # Print insights
        for key, value in insights.items():
            print(f"{key}:\n{value}\n")
    else:
        print("No metadata found.")