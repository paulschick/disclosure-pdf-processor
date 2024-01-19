# Disclosure CLI OCR Extractor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Companion project, [disclosureupdater](https://github.com/paulschick/disclosureupdater)

Very slow to process. Plan for around 5 hours to process 17,000 images.
Looking into using Golang with similar options to produce CSV output.

editing phase

## Code To Do

- [ ] Add tesseract best to configuration options
- [ ] Plan: how to integrate with Go CLI project

## Outline

- Overview
- Usage with Go CLI program
  - Using the Go CLI to generate the initial image data set
- Installation
  - Prerequisites
    - OpenCV
    - Tesseract
    - Download Tesseract Best Data
      - Provide recommended (default) location for the training data
- Usage
  - Configuration
    - Creating initial data set with Go CLI
    - Initialization
    - Setting image folder from Go generated data
  - OCR process
  - Failed Files
    - Future intent
      - Rotating images and re-trying OCR
