from PIL import Image

def to_bin(text):
    """Convert text to binary format."""
    binary = ''.join(format(ord(c), '08b') for c in text)
    return binary

def embed_lsb(cover_image, message, output_image):
    """Embed message in the cover image using LSB steganography."""
    try:
        image = Image.open(cover_image)
        binary_message = to_bin(message + "\x00")  # Add a special delimiter (null byte)

        data_index = 0
        width, height = image.size
        pixels = image.load()

        for row in range(height):
            for col in range(width):
                pixel = list(pixels[col, row])
                for i in range(3):  # Iterate through RGB channels
                    if data_index < len(binary_message):
                        pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1
                pixels[col, row] = tuple(pixel)

        image.save(output_image)
    except Exception as e:
        print(f"Error during embedding: {str(e)}")
        raise

def extract_lsb(image_path):
    """Extract message from the image using LSB steganography."""
    try:
        image = Image.open(image_path)
        width, height = image.size
        pixels = image.load()

        binary_message = ""
        for row in range(height):
            for col in range(width):
                pixel = list(pixels[col, row])
                for i in range(3):  # Iterate through RGB channels
                    binary_message += format(pixel[i], '08b')[-1]  # Extract LSB

        # Split by 8 bits to form characters
        decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        return decoded_message.split('\x00')[0]  # Return message before the null byte
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        return None
