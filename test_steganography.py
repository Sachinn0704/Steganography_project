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

    def test_payload_capacity_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            cover = Path(tmp) / "cover.png"
            stego = Path(tmp) / "stego.png"
            self.create_cover(cover)

            # A 16x16 RGB image has 768 LSBs. One byte is reserved for
            # the null delimiter, so 95 ASCII bytes is the largest payload.
            message = "A" * 95
            embed_lsb(cover, message, stego)

            self.assertEqual(extract_lsb(stego), message)

            with self.assertRaises(ValueError):
                embed_lsb(cover, "B" * 96, stego)

    def test_capacity_is_measured_in_utf8_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            cover = Path(tmp) / "cover.png"
            stego = Path(tmp) / "stego.png"
            self.create_cover(cover)

            # Each character below occupies three UTF-8 bytes. Forty-two
            # characters therefore fit (126 bytes + 1-byte delimiter), while
            # forty-three characters require 130 bytes and must be rejected.
            message = "界" * 42
            embed_lsb(cover, message, stego)
            self.assertEqual(extract_lsb(stego), message)

            with self.assertRaises(ValueError):
                embed_lsb(cover, "界" * 43, stego)

    def test_extraction_from_unmodified_image_returns_no_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            cover = Path(tmp) / "cover.png"
            self.create_cover(cover)

            self.assertIsNone(extract_lsb(cover))


if __name__ == "__main__":
    unittest.main()
