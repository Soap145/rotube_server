import cv2
import os
import numpy as np

def extract_frames_and_pixel_data(video_path, output_lua_file, every_n_frames=60):
    """
    Extracts frames from a video file and writes scaled pixel data to a Lua file for Roblox.
    :param video_path: Path to the video file.
    :param output_lua_file: Lua file to write pixel data.
    :param every_n_frames: Interval of frames to capture (60 captures every 60th frame).
    """
    vidcap = cv2.VideoCapture(video_path)
    count = 0
    success = True
    frames_data = []

    while success:
        success, image = vidcap.read()
        if success:
            # Convert the image from BGR to RGBA
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            # Normalize pixel values to 0-1 range
            normalized_image = image / 255.0
            # Flatten the image array to 1D
            flattened = normalized_image.flatten()
            # Convert numpy array to list for easier handling
            pixel_data = list(flattened)
            frames_data.append((count, pixel_data))
        count += 1
    vidcap.release()

    # Write to Lua file
    with open(output_lua_file, 'w') as file:
        file.write("local framesData = {\n")
        for frame_number, data in frames_data:
            # Formatting data with higher precision
            data_string = ",".join(f"{x:.4f}" for x in data)
            file.write(f"    [{frame_number}] = {{{data_string}}},\n")
        file.write("}\n")
        file.write("return framesData")
    print("Pixel data extracted and written to " + output_lua_file)

if __name__ == "__main__":
    output_lua_file = './output.lua'
    if os.path.exists(output_lua_file):
        print("You currently have an output.lua file. If you continue it will be deleted completely and you won't be able to recover its contents.")
        inputOutput = input("Do you want to continue? [Y/N] ").lower()
        if inputOutput == "y":
            os.remove(output_lua_file)
            video_path = './path_to_your_video.mp4'
            extract_frames_and_pixel_data(video_path, output_lua_file)
        elif inputOutput == "n":
            exit()
        else:
            exit('That is not a valid answer! Please pick between "Y" (Yes) and "N" (No).')
    else:
        print("No output.lua was detected. A new file will be created.")
        inputOutput = input("Do you want to continue? [Y/N] ").lower()
        if inputOutput == "y":
            video_path = './path_to_your_video.mp4'
            extract_frames_and_pixel_data(video_path, output_lua_file)
        elif inputOutput == "n":
            exit()
        else:
            exit('That is not a valid answer! Please pick between "Y" (Yes) and "N" (No).')
