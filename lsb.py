from PIL import Image


def to_str(binary_data):
    """Convert complete 8-bit binary groups into a UTF-8 string."""
    raw = bytearray()
    for index in range(0, len(binary_data) - 7, 8):
        value = int(binary_data[index:index + 8], 2)
        if value == 0:
            break
        raw.append(value)
    return raw.decode('utf-8', errors='replace')


def extract_lsb(image_path):
    """Extract a null-delimited UTF-8 message from RGB image LSBs."""
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    binary_data = []

    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]
            binary_data.extend(str(pixel[channel] & 1) for channel in range(3))

    return to_str(''.join(binary_data))
