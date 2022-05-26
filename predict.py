from dotenv import load_dotenv
load_dotenv()
import replicate
from urllib import request
import argparse


# Get args from the command line
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
prediction_generator = replicate.models.get(args.model).predict(prompt=args.prompt, steps=20)
print("prediction_generator: ", prediction_generator)

# iterate over prediction reponses
for url in prediction_generator:
    print("url: ", url)
    
    # get extension from url
    extension = url.split('.')[-1]
    uuid = url.split('/')[-2]
    filename =  f"{uuid}.{extension}"
    
    filepath = temp_dir + '/' + filename

    print("extension: ", extension)
    print("uuid: ", uuid)
    print("filename: ", filename)
    print("filepath: ", filepath)

    response = request.urlretrieve(url, filename)    
    print("response: ", response)

# convert images from temp_dir to video using ffmpeg
import subprocess
subprocess.call(["ffmpeg", "-framerate", "10", "-pattern_type", "glob", "-i", temp_dir + "/*.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", temp_dir + "/output.mp4"])

print(temp_dir + "/output.mp4")
    
print("done!")

