"""
Image preprocessing utilities for MobileNetV2 infrastructure classification.

This module handles:
1. Input validation for uploaded images.
2. Conversion to RGB color space.
3. Resizing to 224x224 using high-quality Lanczos resampling.
4. Normalization to [0, 1] range matching model training configuration.
5. Batch dimension expansion for tensor inference.
"""

from typing import Tuple
import numpy as np
from PIL import Image


TARGET_IMAGE_SIZE: Tuple[int, int] = (224, 224)
ALLOWED_FORMATS = {"JPEG", "JPG", "PNG"}


def validate_image(image: Image.Image) -> bool:
    """
    Validates that the provided object is a valid PIL Image.

    Args:
        image: PIL Image instance.

    Returns:
        bool: True if image is valid, False otherwise.
    """
    if image is None:
        return False
    return isinstance(image, Image.Image)


def preprocess_image(
    image: Image.Image,
    target_size: Tuple[int, int] = TARGET_IMAGE_SIZE
) -> Tuple[np.ndarray, Image.Image]:
    """
    Preprocesses a PIL Image for MobileNetV2 inference.

    Pipeline:
        1. Convert image to RGB format.
        2. Resize image to target_size (default: 224x224) using LANCZOS.
        3. Convert pixel values to float32 NumPy array.
        4. Normalize pixel values to [0, 1] by dividing by 255.0.
        5. Expand dimensions to shape (1, height, width, 3).

    Args:
        image: Input PIL Image.
        target_size: Tuple (height, width) expected by the neural network.

    Returns:
        Tuple[np.ndarray, Image.Image]:
            - Preprocessed batch array of shape (1, 224, 224, 3) ready for model.predict()
            - Resized RGB PIL Image for display or inspection
    """
    # 1. Convert to RGB color space (ensures 3 channels, handles RGBA/grayscale)
    rgb_image = image.convert("RGB")

    # 2. Resize to 224 x 224
    resized_image = rgb_image.resize(target_size, Image.Resampling.LANCZOS)

    # 3. Convert to float32 numpy array
    img_array = np.array(resized_image, dtype=np.float32)

    # 4. Normalize pixel values to [0, 1]
    img_array = img_array / 255.0

    # 5. Expand batch dimension to (1, 224, 224, 3)
    batch_array = np.expand_dims(img_array, axis=0)

    return batch_array, resized_image
