"""
Barcode generation utilities for device labels.
"""
import io
import base64
from barcode import Code128
from barcode.writer import ImageWriter


def generate_barcode_base64(device_id: str) -> str:
    """
    Generate a Code128 barcode for the given device ID and return as base64 image.

    Args:
        device_id: The device ID to encode (e.g., "2025-0042")

    Returns:
        Base64 encoded PNG image string suitable for <img src="data:image/png;base64,...">
    """
    # Create barcode object (Code128 supports alphanumeric characters)
    barcode_class = Code128(device_id, writer=ImageWriter())

    # Generate barcode image in memory
    buffer = io.BytesIO()
    barcode_class.write(buffer, options={
        'module_width': 0.3,  # Width of individual bars
        'module_height': 10.0,  # Height of bars in mm
        'quiet_zone': 2.0,  # Margin around barcode
        'font_size': 10,  # Size of text below barcode
        'text_distance': 3.0,  # Distance between bars and text
        'write_text': True,  # Show device ID below barcode
    })

    # Get the image data and encode as base64
    buffer.seek(0)
    image_data = buffer.getvalue()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    return f"data:image/png;base64,{base64_image}"
