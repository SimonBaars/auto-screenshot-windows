import os
import sys
import time
from datetime import datetime
from PIL import Image
import imagehash
import mss
import psutil

# --- Configuration ---
BASE_DIR = os.path.expanduser("~\\Pictures\\Screenshots")
LOCKFILE = os.path.expanduser("~\\AppData\\Local\\screenshotter.lock")
SLEEP_SECONDS = 10

previous_hashes = None


def kill_previous_instance():
    if os.path.exists(LOCKFILE):
        try:
            with open(LOCKFILE, 'r') as f:
                pid = int(f.read().strip())
            if psutil.pid_exists(pid):
                p = psutil.Process(pid)
                # Optional: check process cmdline to be sure it's your script
                cmdline = " ".join(p.cmdline()).lower()
                if ('python' in cmdline or p.name().lower() == 'python.exe' or p.name().lower() == 'pythonw.exe') and \
                        ('screenshotter.py' in cmdline or 'screenshotter.exe' in cmdline):
                    print(f"Killing previous instance with PID {pid}")
                    p.terminate()
                    try:
                        p.wait(timeout=5)
                    except psutil.TimeoutExpired:
                        print("Terminate timed out, killing now...")
                        p.kill()
                else:
                    print(f"Process with PID {pid} is not recognized as previous instance, skipping kill.")
            else:
                print("Previous PID not running.")
        except Exception as e:
            print(f"Failed to kill previous instance: {e}")
        # Clean up lock file regardless
        try:
            os.remove(LOCKFILE)
        except OSError:
            pass


def write_lockfile():
    with open(LOCKFILE, 'w') as f:
        f.write(str(os.getpid()))


def take_screenshot():
    now = datetime.now()
    path = now.strftime("%Y/%m/%d/%H_%M_%S")
    full_dir = os.path.join(BASE_DIR, os.path.dirname(path))
    os.makedirs(full_dir, exist_ok=True)
    filenames = []
    with mss.mss() as sct:
        monitors = sct.monitors[1:]  # skip the virtual monitor 0
        multiple = len(monitors) > 1
        for i, monitor in enumerate(monitors, start=1):
            sct_img = sct.grab(monitor)
            if multiple:
                img_filename = os.path.join(full_dir, f"{os.path.basename(path)}_monitor{i}.png")
            else:
                img_filename = os.path.join(full_dir, f"{os.path.basename(path)}.png")
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
                    try:
                        os.remove(f)
                    except Exception as delete_error:
                        print(f"Failed to delete duplicate {f}: {delete_error}")
            else:
                previous_hashes = current_hashes

            time.sleep(SLEEP_SECONDS)

        except Exception as e:
            # Log error and continue
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error occurred: {e}")
            time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    kill_previous_instance()
    write_lockfile()
    try:
        main_loop()
    finally:
        if os.path.exists(LOCKFILE):
            try:
                os.remove(LOCKFILE)
            except Exception:
                pass
