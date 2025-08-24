import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Directory containing audio files
DIR = "/home/abdelrahman-khaled/Projects/Data/All/Seqoon_DS/wav"  # Change this to your directory

# Check if directory is provided
if not DIR:
    print("Usage: script requires a directory.")
    exit(1)

# Function to get audio duration using soxi
def get_audio_duration(file_path):
    try:
        result = subprocess.run(['soxi', '-D', file_path], capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return (file_path, duration)
    except subprocess.CalledProcessError:
        print(f"Failed to get duration for {file_path}")
        return (file_path, 0)

# Collect all valid audio files
audio_files = [os.path.join(DIR, file) for file in os.listdir(DIR)
               if os.path.isfile(os.path.join(DIR, file)) and file.lower().endswith(('.wav', '.mp3', '.flac', '.ogg'))]

# Initialize variables
total_duration = 0
max_duration = 0
min_duration = None
num_files = 0

# Use ThreadPoolExecutor to process files in parallel
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_audio_duration, file): file for file in audio_files}

    for future in as_completed(futures):
        file_path, duration = future.result()
        if duration > 0:
            # Increment the number of files
            num_files += 1
            # Add to the total duration
            total_duration += duration
            # Check for max duration
            if duration > max_duration:
                max_duration = duration
            # Check for min duration
            if min_duration is None or duration < min_duration:
                min_duration = duration

# Calculate the average duration
if num_files > 0:
    avg_duration = total_duration / num_files
else:
    avg_duration = 0
    min_duration = 0

# Display the results
print(f"Number of audio files: {num_files}")
print(f"Total duration: {(total_duration/ 3600)} hrs")
print(f"Maximum duration: {max_duration:.2f} seconds")
print(f"Minimum duration: {min_duration:.2f} seconds")
print(f"Average duration: {avg_duration:.2f} seconds")