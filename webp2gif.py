#! /usr/bin/env python3

import sys
import os
import imageio
import webp
import requests
import time

def download_file(url: str, save_dir: str = "."):
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.webp"
        save_path = os.path.join(save_dir, filename)
        
        # send GET request
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()  # ensure success

        # write file in binary
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"done: {save_path}")
        return save_path
    
    except Exception as e:
        print(f"wrong: {e}")
        return None
    
def convert_webp2gif(src_webp):
    try:
        with open(src_webp, 'rb') as src_f:
            webp_data = webp.WebPData.from_buffer(src_f.read())
            dec = webp.WebPAnimDecoder.new(webp_data)
            
            list_frame=[]
            list_dur=[]
            prev_timestamp=0

            for frame, timestamp_ms in dec.frames():
                list_frame.append(frame)
                list_dur.append(timestamp_ms/1000.0 - prev_timestamp)
                prev_timestamp = timestamp_ms/1000.0

        with imageio.get_writer(src_webp.replace('.webp', '.gif'), mode='I', duration=list_dur) as dst_writer:
            for frame, duration_ms in zip(list_frame, list_dur):
                dst_writer.append_data(frame)
    except Exception as e:
        print(f"{ERR_RED}error while processing {src_webp}: {e}", file=sys.stderr)
        return -1
    return 0

if sys.stderr.isatty():
    ERR_RED = '\033[0;31m'
else:
    ERR_RED = '\033[0m'
    
if __name__ == '__main__':
    url = "https://p26-im-emoticon-sign.byteimg.com/tos-cn-o-0812/oEymDfucyEcDQJf1QAogFCp0IGxnAAb2EAzAX9~tplv-0wx4r9yasq-awebp-resize:0:0.awebp?biz_tag=aweme_im&lk3s=91c5b7cb&s=im_123&sc=emotion&x-expires=1787626185&x-signature=nwmYEpZ9b23LeOa4EawoIvlXhbs%3D"
    source_path = "" # source webp file path
    source_path = download_file(url)
    convert_webp2gif(source_path)