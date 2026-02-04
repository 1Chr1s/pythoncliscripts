import click
import subprocess
import os
import pandas as pd
import cv2
import pdb
import time
import random



@click.command()
@click.option("--file", help="Name of the csv file containing the links of the videos files")
# Csv file contains columns: "businessid", "name", "businessvideoid", "url", "video_type"
def take_screenshot_of_videos(file):
    try: 
        # Open the file with pandas:
        print("In the take_screenshot_of_videos:")
        business_video_dataframe = pd.read_csv(file)
        print(business_video_dataframe.head)
        print()
        pdb.set_trace()

        for index, business_video_row in business_video_dataframe.iterrows():
            print(f"Currently on index: {index}, businessId: {business_video_row['businessid']}, businessVideoId: {business_video_row['businessvideoid']}")
            video_url = business_video_row["url"]
            # pdb.set_trace()
            video_capture = cv2.VideoCapture(video_url)

            if not video_capture.isOpened():
                print('!!! Unable to open URL')
                return

            print('Stream opened successfully. Reading frames...')
            # pdb.set_trace()

            # Read a single frame
            ret, frame = video_capture.read()
            # pdb.set_trace()

            if ret:
                screenshot_name = f"{business_video_row['businessvideoid']}_{business_video_row['name']}"
                screenshot_name = screenshot_name.replace(" ", "_")
                screenshot_filename = f"{screenshot_name}.png"

                cv2.imwrite(screenshot_filename, frame)
                print(f"Screenshot saved as {screenshot_filename}")
            else:
                print("Failed to read a frame from the stream.")

            # Release the capture object
            video_capture.release()

            # Go to the video url for each business:
            
            # Take a screenshot at the x second:

            # Save the screenshot:
            if index % 2 > 0:
                should_wait = random.choice([True, False])
                if should_wait:
                    print("waiting for 1 second")
                    time.sleep(1)
                


           

    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    take_screenshot_of_videos()