import requests
import os
from tqdm import tqdm

base_url = "https://img.cs2inspects.com/1_1054_{number}_front.webp"
total_images = 1000

def download_image(number, output_folder):
    url = base_url.format(number=number)
    filename = f"{number}.webp"
    filepath = os.path.join(output_folder, filename)

    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return True
    else:
        print(f"Error loading the image {number}: {response.status_code}")
        return False

def download_all_images(output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    successful_downloads = 0
    
    for number in tqdm(range(1, total_images + 1)):
        filename = f"{number}.webp"
        filepath = os.path.join(output_folder, filename)
        
        if not os.path.exists(filepath):
            if download_image(number, output_folder):
                successful_downloads += 1

    print(f"\nDownloaded successfully: {successful_downloads}/{total_images}")
