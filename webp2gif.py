#! /usr/bin/env python3

import os
import requests
import time
from PIL import Image, ImageSequence

def download_file(url: str, save_dir: str = "."):
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.webp"
        save_path = os.path.join(save_dir, filename)
        gif_path = os.path.join(save_dir, f"{timestamp}.gif")
        
        # send GET request
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()  # ensure success

        # write file in binary
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"done: {save_path}")
        return save_path, gif_path
    
    except Exception as e:
        print(f"wrong: {e}")
        return None
    
def convert_webp2gif(src_webp, gif_path):
    try:

        im = Image.open(src_webp)

        frames = []
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert("RGBA") 
            bg = Image.new("RGBA", im.size, (255, 255, 255, 0))
            bg.paste(frame, (0, 0), frame)
            frames.append(bg.convert("P")) 

        # save GIF
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=im.info.get("duration", 100),  # Keep original FPS
            disposal=2  # Refresh every frame to avoid ghosting
        )
        print(f"已转换为 GIF: {gif_path}")

    except Exception as e:
        print(f"error while processing {src_webp}: {e}")
        return -1
    return 0

if __name__ == '__main__':
    url = input()
    source_path = "" # source webp file path
    source_path, gif_path = download_file(url)
    convert_webp2gif(source_path, gif_path)