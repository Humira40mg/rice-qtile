import requests

def download_image(url: str, local_filename: str):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  

        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    
    except Exception:
        if not path.exists(local_filename) : return None
    
    return local_filename