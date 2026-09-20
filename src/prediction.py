"""
Model loading and prediction pipeline for infrastructure issue classification.

This module provides:
1. Safe loading of the fine-tuned MobileNetV2 Keras model.
2. Loading of class name taxonomy.
3. Inference on preprocessed image batches with confidence extraction.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import tensorflow as tf

DEFAULT_CLASS_NAMES = [
    "garbage",
    "normal",
    "pothole",
    "road_crack"
]


def load_class_names(class_names_path: Optional[Path] = None) -> List[str]:
    """
    Loads class names from a text file or returns the default taxonomy.

    Args:
        class_names_path: Optional Path to class_names.txt

    Returns:
        List[str]: Ordered list of class label strings.
    """
    if class_names_path and Path(class_names_path).exists():
        with open(class_names_path, "r", encoding="utf-8") as f:
            classes = [line.strip() for line in f if line.strip()]
            if classes:
                return classes
    return DEFAULT_CLASS_NAMES.copy()


def load_classification_model(model_path: Path) -> tf.keras.Model:
    """
    Loads the trained Keras model from disk.

    Args:
        model_path: Absolute or relative Path to the saved .keras model file.

    Returns:
        tf.keras.Model: Loaded TensorFlow/Keras model.

    Raises:
        FileNotFoundError: If the model file is not found.
        Exception: If loading fails.
    """
    resolved_path = Path(model_path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Model file not found at: {resolved_path}")

    model = tf.keras.models.load_model(str(resolved_path))
    return model


class PredictionResult(dict):
    """
    Structured prediction container that supports both dictionary access
    and 3-element tuple unpacking: (predicted_class, confidence_score, all_probabilities).
    """
    def __iter__(self):
        yield self["predicted_class"]
        yield self["confidence_score"]
        yield self["all_probabilities"]


def predict_infrastructure_issue(
    model: tf.keras.Model,
    preprocessed_array: Optional[np.ndarray] = None,
    class_names: Optional[List[str]] = None,
    image: Optional[Any] = None
) -> PredictionResult:
    """
    Performs inference on an image or preprocessed array and returns structured prediction results.

    Supports both:
    1. Direct PIL Image: predict_infrastructure_issue(model, image=image)
    2. Preprocessed Array: predict_infrastructure_issue(model, preprocessed_array=arr)
    3. Both tuple unpacking: (predicted_class, confidence_score, all_probabilities) = predict_...
       and dictionary access: res['predicted_class'], res['confidence'], etc.

    Args:
        model: Trained Keras model.
        preprocessed_array: Optional batch array of shape (1, 224, 224, 3) normalized in [0, 1].
        class_names: List of class names corresponding to output neuron indices.
        image: Optional PIL Image to preprocess automatically.

    Returns:
        PredictionResult: Dictionary supporting tuple unpacking of:
            (predicted_class: str, confidence_score: float [0-1], all_probabilities: Dict[str, float [0-1]])
    """
    if class_names is None:
        class_names = DEFAULT_CLASS_NAMES

    if preprocessed_array is None:
        if image is not None:
            from .preprocessing import preprocess_image
            preprocessed_array, _ = preprocess_image(image)
        else:
            raise ValueError("Either 'preprocessed_array' or 'image' must be provided.")

    # Run inference
    raw_predictions = model.predict(preprocessed_array, verbose=0)[0]

    predicted_index = int(np.argmax(raw_predictions))
    predicted_class = class_names[predicted_index]
    confidence_ratio = float(raw_predictions[predicted_index])  # 0.0 to 1.0
    confidence_percent = float(confidence_ratio * 100.0)       # 0.0 to 100.0

    all_probabilities_ratio = {
        cls_name: float(prob)
        for cls_name, prob in zip(class_names, raw_predictions)
    }

    class_probabilities_percent = {
        cls_name: float(prob * 100.0)
        for cls_name, prob in zip(class_names, raw_predictions)
    }

    return PredictionResult({
        "predicted_class": predicted_class,
        "predicted_index": predicted_index,
        "confidence_score": confidence_ratio,
        "confidence": confidence_percent,
        "all_probabilities": all_probabilities_ratio,
        "class_probabilities": class_probabilities_percent,
        "raw_probabilities": [float(p) for p in raw_predictions]
    })

