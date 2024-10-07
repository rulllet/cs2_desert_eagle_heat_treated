import csv
import cv2
import numpy as np
import os

from tqdm import tqdm

def calculate_color_percentages(image_path):
    
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError("Failed to upload image")
    
    # Conversion to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Defining ranges for shades of blue, black and white
    lower_blue = np.array([100, 150, 0]) 
    upper_blue = np.array([140, 255, 255]) 
    
    lower_black = np.array([0, 0, 0]) 
    upper_black = np.array([180, 255, 50]) 
    
    lower_white = np.array([255, 255, 255])  
    upper_white = np.array([232, 232, 232])  
    
    # Creating masks for shades of blue, black and white
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
    white_mask = cv2.inRange(hsv_image, lower_white, upper_white)
    
    # Counting the number of pixels
    blue_pixels = cv2.countNonZero(blue_mask)
    black_pixels = cv2.countNonZero(black_mask)
    total_non_white_pixels = image.shape[0] * image.shape[1] - cv2.countNonZero(white_mask)
    
    # Calculating percentages
    blue_percentage = (blue_pixels / total_non_white_pixels) * 100 if total_non_white_pixels > 0 else 0
    black_percentage = (black_pixels / total_non_white_pixels) * 100 if total_non_white_pixels > 0 else 0

    return image, blue_mask, black_mask, blue_percentage, black_percentage


def save_masks(image_path, original_image, blue_mask, black_mask, input_folder):
    filename = os.path.splitext(os.path.basename(image_path))[0]
        
    # Creating an image with blue pixels on a black background
    blue_image = cv2.bitwise_and(original_image, original_image, mask=blue_mask)
    cv2.imwrite(f"{input_folder}masks/{filename}_image_blue.webp", blue_image)
        
    # Creating an image with black pixels on a white background
    white_image = np.full_like(original_image, (255, 255, 255), dtype=np.uint8)
    black_image = cv2.bitwise_and(white_image, white_image, mask=black_mask)
    cv2.imwrite(f"{input_folder}/masks/{filename}_image_black.webp", black_image)

def image_analysis_and_save_csv(input_folder, file_csv, masks=False):
    # Creating a header for the CSV file
    fieldnames = ['filename', 'blue_percentage', 'black_percentage']

    # Opening the CSV file for recording
    with open(file_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
    
    # Bypass all files in the specified folder
        for filename in tqdm(os.listdir(input_folder)):
            if filename.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')):
                image_path = os.path.join(input_folder, filename)
                
                try:
                    image, blue_mask, black_mask, blue_percentage, black_percentage = calculate_color_percentages(image_path)
                    
                    if masks:
                        save_masks(image_path, image, blue_mask, black_mask, input_folder)
                    
                    # Записываем результаты в CSV-файл
                    writer.writerow({
                        'filename': filename,
                        'blue_percentage': f"{blue_percentage:.4f}",
                        'black_percentage': f"{black_percentage:.4f}"
                    })

                except ValueError as e:
                    print(f"Error processing the file {filename}: {str(e)}")

    print(f"\nThe analysis is completed. The results are saved in a file {file_csv}")