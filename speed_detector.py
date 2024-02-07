import cv2


def match_digit(screenshot, templates):
    """
    Matches a screenshot against a set of digit templates by detecting edges.

    :param screenshot: The image where the digit is displayed.
    :param templates: A dictionary with digit templates. Keys are the digits (0-9), values are the images.
    :return: The detected digit.
    """
    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Apply Canny edge detector
    edges = cv2.Canny(screenshot_gray, threshold1=30, threshold2=150)

    found = None

    # Loop over the templates
    for digit, template in templates.items():
        # Convert template to grayscale and apply Canny edge detector
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template_edges = cv2.Canny(template_gray, threshold1=30, threshold2=150)

        # Match the edges of the template with the edges of the screenshot
        result = cv2.matchTemplate(edges, template_edges, cv2.TM_CCOEFF_NORMED)

        # Get the maximum match value for the current template
        (_, maxVal, _, _) = cv2.minMaxLoc(result)

        # If the match for this template is more significant than previous matches, then update the found variable
        if found is None or maxVal > found[0]:
            found = (maxVal, digit)

    # Return the detected digit
    return found[1] if found else None

# Load your screenshot and templates before calling the function
screenshot = cv2.imread('path_to_screenshot.png')
templates = {
    '0': cv2.imread('path_to_template_0.png'),
    '1': cv2.imread('path_to_template_1.png'),
    # ... Load all digit templates ...
}

detected_digit = match_digit(screenshot, templates)
print(f"Detected digit: {detected_digit}")
