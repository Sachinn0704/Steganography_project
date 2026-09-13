import tempfile
import unittest
from pathlib import Path

from PIL import Image

from enc import embed_lsb, extract_lsb


class TestSteganography(unittest.TestCase):
    def create_cover(self, path, size=(16, 16)):
        Image.new("RGB", size, (120, 160, 200)).save(path)

    def test_utf8_message_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            cover = Path(tmp) / "cover.png"
            stego = Path(tmp) / "stego.png"
            self.create_cover(cover)

            message = "Hello, 世界 🌍"
            embed_lsb(cover, message, stego)

            self.assertEqual(extract_lsb(stego), message)

    def test_oversized_message_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            cover = Path(tmp) / "cover.png"
            stego = Path(tmp) / "stego.png"
            self.create_cover(cover, size=(2, 2))

            with self.assertRaises(ValueError):
                embed_lsb(cover, "this message cannot fit", stego)

    def test_extraction_from_unmodified_image_returns_no_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            cover = Path(tmp) / "cover.png"
            self.create_cover(cover)

            self.assertIsNone(extract_lsb(cover))


if __name__ == "__main__":
    unittest.main()
