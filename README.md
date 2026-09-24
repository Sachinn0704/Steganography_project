# Image Steganography Project

A Python project demonstrating digital-image steganography: hiding secret information inside an image so that the embedded data is not obvious from normal visual inspection.

## Project Summary

The implementation hides a UTF-8 text message inside the least significant bits (LSBs) of an RGB image. Steganography focuses on concealing the existence of information rather than simply encrypting its contents.

## Core Workflow

1. Convert the secret message to UTF-8 bytes and binary bits.
2. Append a null-byte delimiter to mark the end of the payload.
3. Replace one least significant bit from each RGB channel with a payload bit.
4. Save the modified image as the stego-image.
5. Read the RGB LSBs back during extraction and decode the recovered bytes as UTF-8.
6. Compare the extracted message with the original to verify integrity.

## Capacity and Validation

Each RGB pixel provides three payload bits. The implementation reserves eight bits for the null delimiter, so the safe payload limit is approximately `floor(width × height × 3 / 8) - 1` UTF-8 bytes. Capacity is measured using encoded byte length rather than Python character count, which correctly handles non-ASCII text.

## Core Concept

The general workflow is:

1. Select a cover image.
2. Prepare the secret message or file.
3. Embed the secret information into image data.
4. Save the resulting stego-image.
5. Extract the hidden information when required.
6. Verify that the recovered information matches the original.

## Why Steganography?

Steganography can be useful for studying:

- Information hiding
- Digital media processing
- Data confidentiality concepts
- Image-based communication
- Secure-data handling techniques

## Repository

The implementation files in this repository contain the project code. Refer to the source files for the exact embedding algorithm, input format, and execution commands.

## Key Learning Outcomes

- Understanding the difference between encryption and information hiding
- Working with image data
- Embedding and extracting digital information
- Designing a simple data-hiding workflow

## Future Improvements

- Add detailed usage examples
- Document the exact embedding algorithm
- Add sample input/output images
- Measure image quality before and after embedding
- Add automated extraction and integrity tests
