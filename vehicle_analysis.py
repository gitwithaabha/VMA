# import os
# import pandas as pd
# from dataset_load import load_metadata, display_sample_image
# from edge_ai_model import load_model, analyze_image, generate_insights
# import logging

# def main(data_dir):
#     # Load metadata
#     metadata = load_metadata(data_dir)
#     if metadata.empty:
#         logging.error("No metadata found.")
#         return

#     # Load AI model
#     model = load_model()

#     # Analyze images and generate insights
#     results = []
#     for index, row in metadata.iterrows():
#         image_path = row['vehicle_image_path']
#         result = analyze_image(model, image_path)
#         if result is not None:
#             results.append(result)

#     if results:
#         insights = generate_insights(results)
#         logging.info("Generated insights from analysis.")
#         print(insights)
#     else:
#         logging.info("No results to analyze.")

# if __name__ == "__main__":
#     data_dir = "data/vehicle_images"
#     main(data_dir)
