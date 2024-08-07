# Image Processing API

This is a FastAPI application that processes images by extracting metadata using a specified script. The image path is provided in the request, and the script is executed to process the image.

## Features

- Accepts a JSON request with an image path.
- Verifies the existence of the image path.
- Executes a specified script to process the image.
- Returns a success message if the image is processed successfully.
- Logs relevant information and errors.

## Setup

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- dotenv
- PIL (Pillow)
- exifread
- iptcinfo3

### Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root directory and set the following environment variables:
    ```
    OUTPUT_DIR=path_to_output_directory
    SCRIPT_PATH=path_to_metadata_extraction_script
    ```

5. Update the paths in the `.env` file to match your environment.

### Running the Application

1. Start the FastAPI application using Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```

2. The application will be available at `http://127.0.0.1:8000`.

## Usage

### Endpoint

- **POST** `/process_image/`

### Request

The request body should be in JSON format and include the `image_path`:

```json
{
    "image_path": "path/to/your/image.jpg"
}
