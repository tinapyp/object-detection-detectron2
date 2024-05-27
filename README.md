This is a Flask application that uses Detectron2 for object detection on uploaded images or images captured via a web interface. The application detects various items in the image and displays the results with bounding boxes and labels.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Credits](#credits)

## Features

- Upload an image for object detection.
- Capture an image using the web interface for object detection.
- Display detected objects with bounding boxes and labels.
- List detected items in a table.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/detectron2-flask-app.git
    cd detectron2-flask-app
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Ensure you have the Detectron2 dependencies installed:

    ```sh
    pip install torch torchvision
    pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html
    ```

## Usage

1. Run the Flask application:

    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Use the interface to upload an image or capture an image using your webcam.

## Configuration

### Model Configuration

- The model configuration is specified in the `saved_model/efficient-det.yaml` file.
- The model weights are stored in `saved_model/model.pth`.

### Class Names

- The class names for the objects are defined in the `class_names` list in `app.py`.

### Metadata Registration

- Metadata is registered for the custom dataset with class names in `app.py`.

## File Structure
```
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── saved_model # Directory containing model configuration and weights
│ ├── efficient-det.yaml
│ └── model.pth
├── static
│ ├── styles.css # CSS styles
│ └── uploads # Directory to store uploaded and processed images
├── templates
│ ├── index.html # Main page template
│ ├── result.html # Result page template
└── README.md # This file
```

