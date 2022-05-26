import argparse
import subprocess

import ffmpeg
import replicate
import requests
from dotenv import load_dotenv

# load API key from .env file
load_dotenv()

# get args from the command line
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--prompt', type=str, required=True)
args = parser.parse_args()
print(args.__dict__)

# make a temporary directory to store the files
import tempfile
temp_dir = tempfile.mkdtemp()
print("temp_dir: ", temp_dir)

# start the prediction
prediction_generator = replicate.models.get(args.model).predict(prompt=args.prompt, steps=100)
print("prediction_generator: ", prediction_generator)
print("waiting for output from the model. This can take a bit if the model is cold...")

# iterate over prediction responses
for index, url in enumerate(prediction_generator):

    # construct filename
    prefix = str(index).zfill(4) # 0001, 0002, etc.
    uuid = url.split('/')[-2]
    extension = url.split('.')[-1] # jpg, png, etc
    filename = f"{temp_dir}/{prefix}_{uuid}.{extension}"
    
    # download and save the file
    data = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(data.content)

# create video from series of images and append a reversed copy of the video
# so it will play ping-pong style: start-to-finish-to-start
in1 = ffmpeg.input(f"{temp_dir}/*.{extension}", pattern_type="glob", framerate=20)
v1 = in1.video
v2 = in1.video.filter('reverse')
joined = ffmpeg.concat(v1, v2, v=1).node

# create video
video_path = f"{temp_dir}/output.mp4"
ffmpeg.output(joined[0], video_path).run()

# create gif
gif_path = f"{temp_dir}/output.gif"
ffmpeg.output(joined[0], gif_path).run()

print(video_path)
subprocess.run(['open', video_path], check=True)

print(gif_path)
subprocess.run(['open', gif_path], check=True)

subprocess.run(['open', temp_dir], check=True)

print("done!")
