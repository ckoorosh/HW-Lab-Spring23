#!/bin/bash

# Get packages required for OpenCV
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev -y
sudo apt-get install libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev -y
sudo apt-get install libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev -y
sudo apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev -y
sudo apt-get install libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
pip install --default-timeout=100 opencv-python

# Get packages required for TensorFlow
pip install tflite-runtime