import os
import warnings
import csv
from moviepy.editor import VideoFileClip

# Suppress warnings related to FFMPEG_AudioReader
warnings.filterwarnings("ignore", category=UserWarning, module="moviepy.audio.io.ffmpeg_audioreader")

def get_video_duration(video_path):
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration / 60.0  # Convert duration to minutes
        clip.close()  # Explicitly close the VideoFileClip object
        return duration
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        return None

def process_folder(folder_path, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Relative Video Path', 'Duration (minutes)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):  # Add more extensions if needed
                    video_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(video_path, folder_path)
                    duration = get_video_duration(video_path)
                    
                    if duration is not None:
                        writer.writerow({'Relative Video Path': relative_path, 'Duration (minutes)': f"{duration:.2f}"})
                        print(f"Processed: {relative_path} - Duration: {duration:.2f} minutes")

if __name__ == "__main__":
    
    input_folder = "folder_path"
    output_file = "output_file_path.csv"


    process_folder(input_folder, output_file)
