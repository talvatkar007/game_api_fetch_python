import requests
import os
import shutil

# API Endpoint
API_URL = "https://partner-auth.dev-lab.uk/api/providers/1/games"

# Fetch game records from the API
response = requests.get(API_URL)
response.raise_for_status()  # Raise an error for bad responses
games = response.json()

# Process each game record
for game in games:
    name = game['name'].replace(" ", "_")  # Replace spaces with underscores
    game_code = game['game_code']
    category = game['category']
    
    # Prepare filenames and folders
    square_filename = f"{name}_{game_code}.jpg"
    round_filename = f"{name}_{game_code}.jpg"  # Assuming the same naming convention
    square_folder = os.path.join(category, "square")
    round_folder = os.path.join(category, "round")
    
    # Create folders if they don't exist
    os.makedirs(square_folder, exist_ok=True)
    os.makedirs(round_folder, exist_ok=True)
    
    # Download square image
    square_image_url = game['image_square']
    square_image_response = requests.get(square_image_url, stream=True)
    square_image_response.raise_for_status()
    
    # Save square image
    out_file_square = open(os.path.join(square_folder, square_filename), 'wb')  # Open file for writing
    shutil.copyfileobj(square_image_response.raw, out_file_square)  # Copy the image data
    out_file_square.close()  # Close the file

    # Download round image if available
    if 'image_round' in game:
        round_image_url = game['image_round']
        round_image_response = requests.get(round_image_url, stream=True)
        round_image_response.raise_for_status()
        
        # Save round image
        out_file_round = open(os.path.join(round_folder, round_filename), 'wb')  # Open file for writing
        shutil.copyfileobj(round_image_response.raw, out_file_round)  # Copy the image data
        out_file_round.close()  # Close the file

print("Images downloaded successfully.")
