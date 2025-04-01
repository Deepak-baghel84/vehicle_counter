# Vehicle Counter using YOLO and SORT Tracker

## Description
This project is a real-time vehicle counting system using YOLO for object detection and SORT for object tracking. It captures frames from a video, processes them to detect and count vehicles, and displays the results.

## Features
- Uses YOLOv8 for vehicle detection.
- Using SORT for multi-object tracking which uses kalman filtering internally.
- Utilizes multithreading for efficient frame capture and processing(working).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vehicle-counter.git
   cd vehicle-counter

2. Clone the SORT repository:
   ```sh
   git clone https://github.com/abewley/sort.git

3. Install dependencies:
   pip install -r requirements.txt