import os
import json
import glob
from PIL import Image
import exifread
from iptcinfo3 import IPTCInfo

def extract_metadata(file_path):
    metadata = {
        'EXIF': {},
        'IPTC': {},
        'XMP': {},
        'Basic': {},
        'PNG': {},
        'TIFF': {},
        'GIF': {},
        'HEIF': {}
    }

    # Open the image using Pillow
    image = Image.open(file_path)

    # EXIF metadata using exifread
    try:
        with open(file_path, 'rb') as f:
            exif_data = exifread.process_file(f)
            metadata['EXIF'] = {tag: str(value) for tag, value in exif_data.items()}
    except Exception as e:
        metadata['EXIF'] = str(e)

    # PNG metadata
    if image.format == 'PNG':
        metadata['PNG'] = image.info

    # TIFF metadata using Pillow
    if image.format == 'TIFF':
        metadata['TIFF'] = {tag: image.tag_v2[tag] for tag in image.tag_v2}

    # GIF metadata using Pillow
    if image.format == 'GIF':
        metadata['GIF'] = image.info

    # HEIF metadata using pillow-heif
    if image.format == 'HEIF':
        heif_file = pillow_heif.open_heif(file_path)
        metadata['HEIF'] = heif_file.metadata

    return metadata

def save_metadata_as_json(metadata, json_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

def extract_metadata_from_file(image_path, output_dir):
    # Extract metadata
    metadata = extract_metadata(image_path)

    # Save metadata to JSON files
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    exif_json_path = os.path.join(output_dir, f"{base_filename}_metadata.json")

    save_metadata_as_json(metadata, exif_json_path)
    return exif_json_path

def extract_metadata_from_directory(directory_path, output_dir):
    # Supported image formats
    image_extensions = ['jpg', 'jpeg', 'png', 'tiff', 'gif', 'heif']
    files = []
    for ext in image_extensions:
        files.extend(glob.glob(os.path.join(directory_path, f'*.{ext}')))

    for file_path in files:
        print(f"Processing file: {file_path}")
        output_file = extract_metadata_from_file(file_path, output_dir)
        print(f"Metadata saved to: {output_file}")

# Example usage
directory_path = 'C:/Users/guibr/Desktop/microservices/exif/exif'  # Specify the directory path here
output_dir = 'C:/Users/guibr/Desktop/microservices/exif/output'     # Update to the correct output directory
extract_metadata_from_directory(directory_path, output_dir)
