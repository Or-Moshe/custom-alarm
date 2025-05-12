import random
import webbrowser

YOUTUBE_LINKS = [
    "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=3tmd-ClpJxA"
]

def open_random_youtube():
    link = random.choice(YOUTUBE_LINKS)
    webbrowser.open(link)

