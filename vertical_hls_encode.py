import click
import subprocess
import os

@click.command()
@click.option("--folder", help="Name of the folder containing the video files")
def convert_videos_to_hls(folder):
    try:
        files = os.listdir(folder)
        print("Files in the folder:", files)
        for file_name in files:
            print("Current file:", file_name)
            if file_name.endswith(".mp4"):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    print("Processing file:", file_name)
                    print("File path:", file_path)
                    formatted_file_name = file_name.replace(".mp4", "")
                    output_directory_name = f"{formatted_file_name}_output"
                    full_output_directory_name = f"{folder}/{output_directory_name}"
                    os.mkdir(full_output_directory_name)
                    os.chdir(full_output_directory_name)
                    convert_to_hls(f"../{file_name}")
                    os.chdir("../../")
                    pwd_output = subprocess.run("pwd", shell=True, check=True, capture_output=True, text=True)
                    print("Current working directory:", pwd_output.stdout)

                else:
                    print("File not found:", file_path)
            else:
                print("Skipping non-video file:", file_name)
    except FileNotFoundError:
        print(f"Error: Folder '{folder}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def convert_to_hls(video_name):
    try:
        first_vertical_hls_command = f"ffmpeg -i {video_name} -c:v libx264 -preset slow -profile:v baseline -level 3.0 -s 360x640 -start_number 0 -hls_time 5 -hls_list_size 0 -f hls 640_out.m3u8"

        second_vertical_hls_command = f"ffmpeg -i {video_name} -c:v libx264 -preset slow -profile:v baseline -level 3.0 -s 480x800 -start_number 0 -hls_time 5 -hls_list_size 0 -f hls 800_out.m3u8"

        third_vertical_hls_command = f"ffmpeg -i {video_name} -c:v libx264 -preset slow -profile:v baseline -level 3.0 -s 720x1280 -start_number 0 -hls_time 5 -hls_list_size 0 -f hls 1280_out.m3u8"

        fourth_vertical_hls_command = f"ffmpeg -i {video_name} -c:v libx264 -preset slow -profile:v baseline -level 3.0 -s 1080x1920 -start_number 0 -hls_time 5 -hls_list_size 0 -f hls 1920_out.m3u8"

        hls_parent_file_content = ("#EXTM3U\n"
                                   "#EXT-X-STREAM-INF:BANDWIDTH=375000,RESOLUTION=360x640\n640_out.m3u8\n"
                                   "#EXT-X-STREAM-INF:BANDWIDTH=750000,RESOLUTION=480x854\n854_out.m3u8\n"
                                   "#EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=720x1280\n1280_out.m3u8\n"
                                   "#EXT-X-STREAM-INF:BANDWIDTH=3500000,RESOLUTION=1080x1920\n1920_out.m3u8")

        first_command_result = subprocess.run(first_vertical_hls_command, shell=True, check=True, capture_output=True, text=True)
        click.echo("1st command executed successfully.")

        second_command_result = subprocess.run(second_vertical_hls_command, shell=True, check=True, capture_output=True, text=True)
        click.echo("2nd command executed successfully.")

        third_command_result = subprocess.run(third_vertical_hls_command, shell=True, check=True, capture_output=True, text=True)
        click.echo("3rd command executed successfully.")

        fourth_command_result = subprocess.run(fourth_vertical_hls_command, shell=True, check=True, capture_output=True, text=True)
        click.echo("4th command executed successfully.")

        main_file_name = video_name.replace(".mp4", "")

        create_hls_parent_file = open(f"{main_file_name}.m3u8", "w")
        create_hls_parent_file.write(hls_parent_file_content)
        create_hls_parent_file.close()

        click.echo("All commands executed successfully.")

        return


    except subprocess.CalledProcessError as e:
        click.echo(f"Error executing command: {e}")
        click.echo(e.stderr)
        return

if __name__ == "__main__":
    convert_videos_to_hls()