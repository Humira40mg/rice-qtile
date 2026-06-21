import sys
import requests

from pathlib import Path
from os import path, environ

from modules.status_reader import Status

_status = Status()

HOME = Path.home()
LOCAL_FILE_NAME = f"{HOME}/.config/qtile/assets/images/discord_logo.png"

class DiscordAPI:
    BASE_API_URL = "https://discord.com/api/v10/users/@me"
    CDN_URL = "https://cdn.discordapp.com"

    def __init__(self, token: str):
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }


    def download_image(self, url: str, local_filename: str):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  

            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        
        except Exception:
            if not path.exists(local_filename) : return None
        
        return local_filename


    def get_username_and_avatar_url(self, size: int = 256) -> str:
        response = requests.get(self.BASE_API_URL, headers=self.headers)
        response.raise_for_status()

        user_data = response.json()
        user_id = user_data["id"]
        avatar_index = user_data["avatar"]
        avatar_url =  f"{self.CDN_URL}/avatars/{user_id}/{avatar_index}?size={size}"
        global_name = user_data["global_name"]

        if global_name and global_name != "" and global_name != _status.username: 
            _status.username = global_name
            _status.save()
        else: 
            global_name = _status.username

        return global_name, self.download_image(avatar_url, LOCAL_FILE_NAME)


def get_discord_info(token):
    try:
        api = DiscordAPI(token=token)
        return api.get_username_and_avatar_url(size=256)
    except Exception:
        if not path.exists(LOCAL_FILE_NAME): return _status.username, None
        return _status.username, LOCAL_FILE_NAME
