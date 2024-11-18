## Fields_detector
Detects the fields that need to be filled in the form.

## Form OCR Extractor

A Python-based project that extracts and identifies form fields (labels and values) from scanned forms or images using EasyOCR and OpenCV. This tool can recognize text in multiple languages and associate labels with their corresponding values.

## Features

Supports multiple languages (e.g., English, Hindi, Tamil).
Uses advanced image preprocessing techniques for improved OCR accuracy.
Identifies and matches form labels with their respective values.
Easily extendable and customizable.
## Installation

Prerequisites
Python 3.7 or later
pip (Python package installer)
## Install the project dependencies by running: pip install -r requirements.txt

This will install the necessary packages:
pip install -r Requirements.txt


easyocr for Optical Character Recognition (OCR)
opencv-python-headless for image processing
numpy for numerical operations
scikit-learn for calculating Euclidean distances
To verify that EasyOCR is installed correctly, you can check the supported languages with the following command: python -c "import easyocr; print(easyocr.Reader.list_supported_languages())"

## Usage
Place your image file in the project folder.

Update the image_path variable in main.py with the path to your image.

## Run the script:
python main.py

The extracted fields will be printed in the terminal.

