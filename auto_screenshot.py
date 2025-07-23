import os
import time
from datetime import datetime
from PIL import Image
import imagehash
import mss

base_dir = os.path.expanduser("~\\Pictures\\Screenshots")
previous_hashes = None

def take_screenshot():
    now = datetime.now()
    path = now.strftime("%Y/%m/%d/%H_%M_%S")
    full_dir = os.path.join(base_dir, os.path.dirname(path))
    os.makedirs(full_dir, exist_ok=True)
    filenames = []
    with mss.mss() as sct:
        # sct.monitors[1:] skips the pseudo-monitor [0]
        for i, monitor in enumerate(sct.monitors[1:], start=1):
            sct_img = sct.grab(monitor)
            img_filename = os.path.join(full_dir, f"{os.path.basename(path)}_monitor{i}.png")
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=img_filename)
            filenames.append(img_filename)
    return filenames

def compute_hash(filename):
    with Image.open(filename) as img:
        return imagehash.phash(img)

def main_loop():
    global previous_hashes
    while True:
        try:
            filenames = take_screenshot()
            current_hashes = [compute_hash(f) for f in filenames]
            if previous_hashes is not None and current_hashes == previous_hashes:
                # Screens unchanged; remove current files
                for f in filenames:
                    os.remove(f)
            else:
                previous_hashes = current_hashes
            time.sleep(10)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main_loop()
