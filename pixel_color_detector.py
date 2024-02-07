import numpy as np
from PIL import ImageGrab
from color_lightener import adjust_image_parameters
import cv2


def define_color_names():
    return {
        'red': np.array([190, 45, 34]),
        'green': np.array([153, 199, 72]),
        'yellow': np.array([236, 186, 88]),
        'purple': np.array([84, 12, 131]),
        'cyan': np.array([62, 130, 152]),
        'dark blue': np.array([41, 80, 132]),
        'orange': np.array([216, 112, 59]),
    }


def define_dark_color_names():
    return {
        'red': np.array([228, 0, 0]),
        'green': np.array([189, 210, 63]), #
        'yellow': np.array([255, 195, 18]),
        'purple': np.array([84, 0, 111]),
        'cyan': np.array([42, 183, 210]),
        'dark blue': np.array([30, 108, 198]), #
        'orange': np.array([210, 90, 9]),
    }


def get_nearest_color_name(color, color_names):
    color = color[:3]
    colors = list(color_names.values())
    color_diffs = np.linalg.norm(colors - np.array(color), axis=1)
    return list(color_names.keys())[np.argmin(color_diffs)]


def get_pixel_color(pixel_coordinates=(597, 92)):
    """

    :param pixel_coordinates: coordinate of the pixel
    :return: color of the pixel, out of the seven preset colors
    """
    # Take a screenshot at the specified pixel
    screenshot = ImageGrab.grab(bbox=(pixel_coordinates[0], pixel_coordinates[1],
                                      pixel_coordinates[0]+1, pixel_coordinates[1]+1))
    # No need to convert to RGB as ImageGrab.grab() already returns an RGB image
    pixel_color = np.array(screenshot)[0, 0]

    # Get the nearest named color
    color_names = define_color_names()
    color_name = get_nearest_color_name(pixel_color, color_names)
    return color_name, pixel_color[:3].tolist()


def get_darkened_pixel_color(pixel_coordinates):
    screenshot = ImageGrab.grab(bbox=(pixel_coordinates[0], pixel_coordinates[1],
                                      pixel_coordinates[0]+1, pixel_coordinates[1]+1))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    lightened = adjust_image_parameters(screenshot)
    # No need to convert to RGB as ImageGrab.grab() already returns an RGB image
    lightened = cv2.cvtColor(lightened, cv2.COLOR_BGR2RGB)
    pixel_color = np.array(lightened)[0, 0]

    # Get the nearest named color
    color_names = define_dark_color_names()
    color_name = get_nearest_color_name(pixel_color, color_names)
    return color_name, pixel_color[:3].tolist()
