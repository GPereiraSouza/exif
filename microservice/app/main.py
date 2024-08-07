from fastapi import FastAPI, HTTPException, Request
from pathlib import Path
import subprocess
import logging
import sys
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from the .env file
load_dotenv()

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/process_image/")
async def process_image(request: Request):
    try:
        # Get the image path from the request body
        request_data = await request.json()
        image_path = request_data.get("image_path")

        if not image_path:
            raise HTTPException(status_code=400, detail="Image path not provided")

        image_path = Path(image_path).resolve()

        if not image_path.exists():
            raise HTTPException(status_code=400, detail="Image path does not exist")

        # Get the output directory and script path from environment variables
        output_dir = Path(os.getenv("OUTPUT_DIR")).resolve()
        script_path = Path(os.getenv("SCRIPT_PATH")).resolve()

        logger.info(f"Image path: {image_path}")
        logger.info(f"Output directory path: {output_dir}")

        # Path to the Python executable of the virtual environment
        venv_python = Path(sys.executable).resolve()
        
        # Command to run the script
        command = [
            str(venv_python),  
            str(script_path),
            str(image_path),
            str(output_dir)
        ]
        logger.info(f"Running command: {' '.join(command)}")

        # Run the script using subprocess
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"Error running script: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"Error processing the image: {result.stderr}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error processing the image")

    return {"message": "Image processed successfully"}
