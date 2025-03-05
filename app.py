
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
from dataset_create import capture_images

class VehicleAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Movement Analysis")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")

        # Frame for buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.button_frame.pack(pady=15)

        # Capture Image Button
        self.capture_button = tk.Button(self.button_frame, text="📸 Capture Image", command=self.capture_image)
        self.capture_button.pack(side='left', padx=10)

        # Output Frame
        self.output_frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.output_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Metadata Text Box
        self.metadata_text = tk.Text(self.output_frame, height=10, font=("Arial", 10))
        self.metadata_text.pack(pady=5, fill='both', expand=True, padx=10)

        # Occupancy Label
        self.occupancy_label = tk.Label(self.output_frame, text="", font=("Arial", 12))
        self.occupancy_label.pack(pady=5)

    def capture_image(self):
        output_dir = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Vehicle-Movement-Analysis-main\\Result"
        capture_images(output_dir, num_images=1)  # Capture 1 image
        self.display_metadata(output_dir)

    def display_metadata(self, output_dir):
        # Display the latest metadata
        metadata_files = sorted([f for f in os.listdir(output_dir) if f.endswith("_metadata.txt")], reverse=True)
        if metadata_files:
            with open(os.path.join(output_dir, metadata_files[0]), 'r') as f:
                metadata = f.read()
            self.metadata_text.delete('1.0', tk.END)
            self.metadata_text.insert(tk.END, metadata)

            # Extract occupancy information
            if "status: Authorized" in metadata:
                self.occupancy_label.config(text="Status: Authorized")
            elif "status: Unauthorized" in metadata:
                self.occupancy_label.config(text="Status: Unauthorized")
            else:
                self.occupancy_label.config(text="Status: License Plate Detection Failed")

if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleAnalysisApp(root)
    root.mainloop()