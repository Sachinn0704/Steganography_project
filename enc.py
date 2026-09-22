from PIL import Image


def to_bin(text):
    """Convert text to an 8-bit UTF-8 binary representation."""
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))


def get_payload_capacity(image):
    """Return the maximum UTF-8 payload size in bytes for an RGB image.

    One byte of capacity is reserved for the null-byte delimiter used by
    extraction, so the returned value is the safe message limit.
    """
    return max(0, (image.width * image.height * 3) // 8 - 1)


def embed_lsb(cover_image, message, output_image):
    """Embed a UTF-8 message in the RGB least significant bits of an image."""
    image = Image.open(cover_image).convert('RGB')
    binary_message = to_bin(message) + '00000000'  # Null-byte delimiter
    capacity = image.width * image.height * 3

    if len(binary_message) > capacity:
        max_bytes = get_payload_capacity(image)
        raise ValueError(
            f"Message is too large for this image. Maximum payload is about {max_bytes} bytes."
        )

    pixels = image.load()
    data_index = 0

    for row in range(image.height):
        for col in range(image.width):
            pixel = list(pixels[col, row])
            for channel in range(3):
                if data_index >= len(binary_message):
                    break
                pixel[channel] = (pixel[channel] & 0xFE) | int(binary_message[data_index])
                data_index += 1
            pixels[col, row] = tuple(pixel)
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    image.save(output_image)


def extract_lsb(image_path):
    """Extract the first null-delimited UTF-8 message from an LSB stego image."""
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    binary_message = []

    for row in range(image.height):
        for col in range(image.width):
            pixel = pixels[col, row]
            binary_message.extend(str(pixel[channel] & 1) for channel in range(3))

    raw = bytearray()
    for index in range(0, len(binary_message) - 7, 8):
        value = int(''.join(binary_message[index:index + 8]), 2)
        if value == 0:
            break
        raw.append(value)

    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return None
