import tkinter as tk
from pathlib import Path  # For easy path manipulation
import time
from tkinter import filedialog
import google.generativeai as genai

def generate_captions(video_path):
    """Generates captions for the given video file using Gemini Pro."""
    genai.configure(api_key="YOUR_API_KEY")  
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # Upload video file
    print(f"Uploading file...")
    video = genai.upload_file(video_path)
    print(f"Uploading Complete")

    # Check whether the file is ready to be used.
    while video.state.name == "PROCESSING":
        print(video.state.name)
        time.sleep(10)
        video = genai.get_file(video.name)

    if video.state.name == "FAILED":
        raise ValueError(video.state.name)

    # Generate captions (SRT format assumed)
    response = model.generate_content(
        ["Please generate SRT captions for this video. Please, make sure the timestamps are in this format 00:00:00,000", video]
    )# Generate captions (SRT format assumed)(response)
    # Access and extract the SRT content correctly
    if response.candidates and response.candidates[0].content:
        return response.candidates[0].content.parts[0].text 
    else:
        raise ValueError("No captions were generated.")  # Extract the SRT content from response

def save_srt(captions, video_path):
    """Saves the SRT captions to a file, replacing the original extension."""
    
    video_path = Path(video_path)  # Convert to Path object
    srt_path = video_path.with_suffix(".srt")  # Replace extension elegantly
    
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(captions)

def main():
    """Opens file picker, generates captions, and saves SRT file."""
    root = tk.Tk()
    root.withdraw()

    video_path = filedialog.askopenfilename(
        title="Select Video File", filetypes=[("Video files", "*.mp4 *.mov *.avi")]
    )

    if video_path:
        captions = generate_captions(video_path)
        save_srt(captions, video_path)
        print("SRT file generated successfully!")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
