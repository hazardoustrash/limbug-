import time
import pytesseract
from PIL import Image
import subprocess


def take_screenshot_with_screencapture(filename, region):
    """
    Takes a screenshot using the macOS screencapture utility.

    :param filename: The path to save the screenshot.
    :param region: A tuple of (x, y, width, height) defining the screenshot region.
    """
    # Format the region for the screencapture command
    region_str = ",".join(map(str, region))
    command = ["screencapture", "-x", "-R" + region_str, filename]
    subprocess.run(command, check=True)


def screenshot_and_detect(points=None, filename='../name_screenshot.png'):
    """

    :param points: the four points bounding the capturing area
    :param filename: where to save the image
    :return: text detected
    """
    # Calculate the bounding box from the points
    if points is None:
        points = [(88, 50),
                  (309, 50),
                  (88, 83),
                  [309, 83]]
    x_coords, y_coords = zip(*points)
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    # Take a screenshot with screencapture
    region = (x_min, y_min, x_max - x_min, y_max - y_min)
    take_screenshot_with_screencapture(filename, region)

    # Open the screenshot
    screenshot = Image.open(filename)
    text = pytesseract.image_to_string(screenshot)
    return text


name = [(88, 50),
        (309, 50),
        (88, 83),
        [309, 83]]
speed = [(465, 845),
         (482, 845),
         (465, 873),
         (482, 873)]
time.sleep(3)
