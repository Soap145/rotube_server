
import cv2
import os
import numpy as np

def get_frame_count(video_path):
    """
    Returns the total number of frames in a video file.
    :param video_path: Path to the video file.
    :return: Total number of frames as an integer.
    """
    # Open video file
    vidcap = cv2.VideoCapture(video_path)
    
    if not vidcap.isOpened():
        print("Error: Could not open video.")
        return None
    
    # Get the total number of frames in the video
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Release the video capture object
    vidcap.release()
    
    return frame_count


def extract_frames_and_pixel_data(video_path, output_lua_file):
    """
    Extracts the first frame from a video file and writes scaled pixel data to a Lua file for Roblox.
    :param video_path: Path to the video file.
    :param output_lua_file: Lua file to write pixel data.
    """
    vidcap = cv2.VideoCapture(video_path)
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

        # Write to Lua file
        with open(output_lua_file, 'w') as file:
      #      file.write("local framesData = {\n")
            # Formatting data to trim unnecessary trailing zeros
            data_string = ",".join(f"{x:.4f}".rstrip('0').rstrip('.') if x != int(x) else str(int(x)) for x in pixel_data)
            #file.write(f"    [1] = {{{data_string}}},\n")
            file.write(data_string)
        #    file.write("}\n")
       #     file.write("return framesData")
    else:
        print("Failed to read the first frame.")
    vidcap.release()
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