from enc import embed_lsb, extract_lsb
from PIL import Image
import os


def check_image_capacity(image_path, message):
    """Check whether an image can hold the UTF-8 message plus its delimiter."""
    try:
        with Image.open(image_path) as image:
            capacity_bits = image.width * image.height * 3
            required_bits = (len(message.encode("utf-8")) + 1) * 8
            if required_bits > capacity_bits:
                max_bytes = max(0, capacity_bits // 8 - 1)
                raise ValueError(
                    f"Message is too large. The image can hold about {max_bytes} UTF-8 bytes."
                )
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def run():
    print("🔐 Steganography Tool")

    cover_image = input("Enter the path to the cover image (e.g., cover.png): ")

    if not os.path.exists(cover_image):
        print(f"Error: {cover_image} not found!")
        return

    message = input("Enter your secret message: ")

    if not check_image_capacity(cover_image, message):
        return

    try:
        print("✅ Embedding message into image...")
        embed_lsb(cover_image, message, "stego.png")
        print("✅ Message embedded and saved to stego.png")

        print("🔍 Extracting message from image...")
        recovered_message = extract_lsb("stego.png")
        print(f"🔍 Recovered message: {recovered_message}")

        if recovered_message != message:
            raise ValueError("Integrity check failed: recovered message does not match the original")

        print("✅ Integrity check passed: recovered message matches the original")
    except Exception as e:
        print(f"Error during embedding or extraction: {str(e)}")


if __name__ == "__main__":
    run()
