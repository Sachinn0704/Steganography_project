from PIL import Image  # Import Image module

def to_str(binary_data):
    """Convert binary data back to string"""
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def extract_lsb(image_path):
    """Extract message from the least significant bit of the image"""
    # Open the image
    image = Image.open(image_path)
    pixels = image.load()

    # Extract binary data from image
    binary_data = ""
    for y in range(image.height):
        for x in range(image.width):
            pixel = list(pixels[x, y])  # Get the RGB values of the pixel
            for i in range(3):  # Loop over R, G, B channels
                binary_data += str(pixel[i] & 1)  # Extract the LSB

    # Convert binary data back to string
    message = to_str(binary_data)

    # Find the null byte (special delimiter) to know where the message ends
    return message.split("\x00")[0]  # Return the message before the null byte
