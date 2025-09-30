from enc import embed_lsb, extract_lsb
from PIL import Image
import os

def check_image_capacity(image_path, message):
    """
    Check if the image can contain the given message.
    """
    try:
        image = Image.open(image_path)
        width, height = image.size
        capacity = (width * height * 3) // 8  # Calculate capacity (each pixel has 3 channels: RGB)
        if len(message) > capacity:
            raise ValueError(f"Message is too large. The image can only hold {capacity} characters.")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run():
    print("🔐 Steganography Tool")

    # Get the cover image file
    cover_image = input("Enter the path to the cover image (e.g., cover.png): ")

    # Check if the image exists
    if not os.path.exists(cover_image):
        print(f"Error: {cover_image} not found!")
        return

    # Get secret message
    message = input("Enter your secret message: ")

    # Check image capacity to hold the message
    if not check_image_capacity(cover_image, message):
        return

    # Embed message into image
    try:
        print("✅ Embedding message into image...")
        embed_lsb(cover_image, message, "stego.png")
        print("✅ Message embedded and saved to stego.png")

        # Extract the message from the stego image
        print("🔍 Extracting message from image...")
        recovered_message = extract_lsb("stego.png")
        print(f"🔍 Recovered message: {recovered_message}")
    except Exception as e:
        print(f"Error during embedding or extraction: {str(e)}")

if __name__ == "__main__":
    run()
