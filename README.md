# Windows Auto-Screenshot

Windows Python program to make full-screen screenshots every 10 seconds for accountability purposes.

## Use the executable
Go to https://github.com/SimonBaars/auto-screenshot-windows/releases/tag/1.0 and download the `auto_screenshot.exe` executable. Execute it and you can find the screenshots at `Pictures/Screenshots`.

For autostart:

- Press `Win + R`, enter:
  ```
  shell:startup
  ```
- Place a shortcut to `auto_screenshot.exe` here.

## Notes

- All screenshots are saved in `Pictures/Screenshots/YYYY/MM/DD/HH_MM_SS[_monitorX].png`
- Duplicate consecutive screenshots (unchanged displays) are deleted automatically.
- Errors are logged to file; script resumes automatically.

## Other versions
- XFCE (Linux): https://github.com/SimonBaars/xfce-auto-screenshot
- Android (Magisk): https://github.com/SimonBaars/magisk-auto-screenshot
- Android (APK): https://github.com/SimonBaars/Android-AutoScreenshot

## Development instructions

### Prerequisites

- Windows 10 or later (though it prob works on earlier Windows versions)
- Python 3.7+
- Install required packages:
  ```
  pip install pillow imagehash mss psutil
  ```

### Installation

1. **Save Script**
   - Save the provided Python script as `auto-screenshot.py` in any folder.

2. **Test Run**
   - Execute the script:
     ```
     python auto-screenshot.py
     ```
   - Screenshots will appear under `Pictures/Screenshots` in a structured date/time format.

3. **Convert to Executable (Optional)**
   - For a standalone `.exe` (no Python install required):
     ```
     pip install pyinstaller
     pyinstaller --onefile --noconsole auto-screenshot.py
     ```
   - Resulting `.exe` will be in the `dist` folder.

### Autostart Setup

**Either method works:**

### 1. Using Startup Folder

- Press `Win + R`, enter:
  ```
  shell:startup
  ```
- Place a shortcut to `auto-screenshot.py` or the packaged `.exe` here.

### 2. Task Scheduler

- Open Windows Task Scheduler.
- Create Basic Task:
  - Trigger: At logon
  - Action: Start Program  
    - **Program/script:** Path to `python.exe` or your compiled `.exe`
    - **Add arguments:** `auto-screenshot.py` (if using `.py`)
    - **Start in:** Directory of your script
