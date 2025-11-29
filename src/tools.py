from urllib.parse import urlparse

from aiogram.types import FSInputFile

def get_poster(poster: str):
    if urlparse(poster).scheme:
        return poster
    else:
        return FSInputFile(poster)