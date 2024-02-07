import cv2
import numpy as np


def adjust_image_parameters(image, gamma=0.8, value_scale=1.5, saturation_scale=1.5):
    # Read the image in BGR format
    if image is None:
        raise ValueError("Image not found")

    # Apply gamma correction
    gamma_corrected = np.power(image / 255.0, gamma)

    # Convert to HSV to adjust saturation and value (brightness)
    hsv = cv2.cvtColor((gamma_corrected * 255).astype('uint8'), cv2.COLOR_BGR2HSV)
    hsv[..., 1] = cv2.multiply(hsv[..., 1], saturation_scale)  # Saturation
    hsv[..., 2] = cv2.multiply(hsv[..., 2], value_scale)       # Value

    # Convert back to BGR format
    adjusted_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Ensure values are within the proper range
    adjusted_img = np.clip(adjusted_img, 0, 255).astype('uint8')

    # Apply contrast adjustment if needed
    alpha = 3  # Contrast control (1.0-3.0)
    beta = 0     # Brightness control (0-100)
    contrast_img = cv2.convertScaleAbs(adjusted_img, alpha=alpha, beta=beta)

    return contrast_img


def save_adjusted_image(image_path, output_path, gamma, value_scale, saturation_scale):
    # Adjust the image with the given parameters
    adjusted_image = adjust_image_parameters(image_path, gamma, value_scale, saturation_scale)
    # Save the adjusted image
    cv2.imwrite(output_path, adjusted_image)



