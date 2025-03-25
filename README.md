# Synchronized-Quad-Camera-Video-Stitching-
This repository contains a Rpi implementation of a synchronized quad-camera video stitching solution utilizing the Arducam CamArray HAT on a Raspberry Pi and four IMX708 camera modules.
Synchronized Quad-Camera Video Stitching

Overview

This project provides a Python-based implementation for synchronized video stitching using the Arducam CamArray HAT on a Raspberry Pi. Four IMX708 camera modules are utilized to create an expansive panoramic video feed, ideal for immersive viewing and real-time applications.

Hardware Requirements

Raspberry Pi (tested on Raspberry Pi 4)

Arducam 12MP IMX708 Quad-Camera Kit

CamArray HAT (Arducam)

Camera Specifications

Individual Camera Resolution: 2304×1296 pixels (quarter resolution)

Composite Frame Size: 4608×2592 pixels (2×2 mosaic layout)

Software Dependencies

Python 3.x

OpenCV

NumPy

v4l2

Arducam MIPI_Camera Python API

Installation

Clone the repository and install the required packages:

git clone <repository-url>
cd <repository-directory>
pip install opencv-python numpy
# Follow the Arducam official guide to install arducam_mipicamera

Usage

Start the quad-camera video stitching script:

python quad_cam_stitching.py

To terminate the video stream, press ESC.

Implementation Steps

1. Camera Initialization

Utilizes Arducam MIPI_Camera API.

Default Resolution: 2304×1296 pixels (28 FPS).

Higher Resolution Option: 4608×2592 pixels (7 FPS).

2. Frame Capture

Frames are captured in YUV (I420) format for efficiency.

3. Quadrant Processing

Each frame is split into four equal segments corresponding to each camera.

4. Image Stitching

Quadrants stitched horizontally with minimal processing.

Optimized for low latency and real-time performance.

5. Real-time Display

Output is displayed in a fullscreen window via OpenCV.

Python Script

Refer to quad_cam_stitching.py for detailed implementation.

Additional Recommendations

Camera Orientation: Adjust the stitching order based on actual camera setup.

Alignment: Implement minor cropping adjustments to correct misalignments.

Performance: Using YUV format enhances real-time processing capabilities.
