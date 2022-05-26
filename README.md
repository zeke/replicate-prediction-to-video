![output](https://user-images.githubusercontent.com/2289/170425350-48b08e54-8eff-4a31-9062-a4b023b1ca07.gif)

This is a command-line tool that uses the [Replicate API](https://replicate.com/api) to create videos from the outputs of image generation models.

## How it works

1. Run the CLI with a model name and a text prompt.
1. The [replicate-python](https://github.com/replicate/replication) client runs a prediction on the given model using the [Replicate API](https://replicate.com/api).
1. The individual images output by the model are save to a temporary directory
1. FFmpeg is used to produce an MP4 and GIF from the output images.

## Usage

Install the dependencies

```
pip install -r requirements.txt
```

Get an API key from [replicate.com/api](https://replicate.com/api) and store it in a `.env` file:

```
echo "REPLICATE_API_KEY=XXXXXX" > .env
```

Create videos!

```sh
$ python prediction-to-video.py --model laion-ai/erlich --prompt "a logo of a white cat curled up into a ball, sleeping on a blue rug"
```

See [replicate.com/collections/text-to-image](https://replicate.com/collections/text-to-image) for a collection of models that generate images from text prompts.