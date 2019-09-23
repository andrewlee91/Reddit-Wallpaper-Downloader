import configparser
import io

import praw
import requests
from PIL import Image

config = configparser.ConfigParser()
config.read("config.ini")

SCORE_THRESHOLD = int(config["DEFAULT"]["score_threshold"])

MIN_WIDTH = int(config["DEFAULT"]["minimum_width"])
MIN_HEIGHT = int(config["DEFAULT"]["minimum_height"])
MAX_WIDTH = int(config["DEFAULT"]["maximum_width"])
MAX_HEIGHT = int(config["DEFAULT"]["maximum_height"])

reddit = praw.Reddit("auth", user_agent="Wallpaper Downloader (by /u/fulke)")

if __name__ == "__main__":
    for submission in reddit.subreddit("wallpapers").top("day"):
        if submission.score >= SCORE_THRESHOLD:
            req = requests.get(submission.url)
            stream = io.BytesIO(req.content)
            image = Image.open(stream)
            image_width, image_height = image.size

            if (image_width >= MIN_WIDTH and image_width <= MAX_WIDTH) and (
                image_height >= MIN_HEIGHT and image_height <= MAX_HEIGHT
            ):
                print(
                    f"Downloading {submission.title} (id: {submission.id}) from u/{submission.author.name}"
                )
                with open(f"{submission.id}.png", "wb") as f:
                    f.write(req.content)
