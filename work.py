import cv2
import numpy as np
import pyautogui
import time


# Load the templates and their labels
templates = {
    "up": cv2.imread("up.png", cv2.IMREAD_GRAYSCALE),
    "down": cv2.imread("down.png", cv2.IMREAD_GRAYSCALE),
    "left": cv2.imread("left.png", cv2.IMREAD_GRAYSCALE),
    "right": cv2.imread("right.png", cv2.IMREAD_GRAYSCALE),
}

# Load the templates and their labels
templates = {
    "up": cv2.imread("up.png", cv2.IMREAD_GRAYSCALE),
    "down": cv2.imread("down.png", cv2.IMREAD_GRAYSCALE),
    "left": cv2.imread("left.png", cv2.IMREAD_GRAYSCALE),
    "right": cv2.imread("right.png", cv2.IMREAD_GRAYSCALE),
}

time.sleep(5)

# Threshold for match filtering
threshold = 0.9

while True:
    # Take screenshot (returns PIL Image)
    screenshot = pyautogui.screenshot()
    # Convert PIL image to NumPy array
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    # Make a working copy of the screenshot to blackout matches
    screenshot_gray_working = screenshot_gray.copy()

    # Detected patterns with x-coordinates
    detected = []

    for direction, template in templates.items():
        h, w = template.shape[:2]
        
        while True:
            res = cv2.matchTemplate(screenshot_gray_working, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val < threshold:
                break  # No strong match left

            top_left = max_loc
            x, y = top_left

            # Record the match
            detected.append((x, direction))

            # Blackout the matched region in working image
            screenshot_gray_working[y:y+h, x:x+w] = 0  # fill with black (0 intensity)

    # Sort detected patterns by x-coordinate (left to right)
    detected.sort(key=lambda x: x[0])

    # Final ordered pattern
    pattern = [direction for _, direction in detected]

    
    for key in pattern:
        pyautogui.press(f"{key}")
        time.sleep(0.1)
        print(key)