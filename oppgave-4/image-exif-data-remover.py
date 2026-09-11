from PIL import Image
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}

script_dir = Path(__file__).resolve().parent

input_dir = script_dir / "input"
output_dir = script_dir / "output"

# Removes EXIF data from a specified image and saves the stripped version.
def remove_image_exif_data(image_path, output_path):
    with Image.open(image_path) as img:
        exif_data = img.getexif()
        exif_data.clear()
        
        img.save(output_path, quality="keep")

# Gets all the images in the input directory and returns them as a list of image file objects
def get_image_files(input_dir):
    images = []
    
    # Loops over every file found in the input directory and appends it to images[] if it's of one of the filetypes stated in IMAGE_EXTENSIONS.
    for file in input_dir.iterdir():
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS:
            images.append({"stem": file.stem, "suffix": file.suffix, "full": file.name})
    
    return images

# Modifies the name of the input file and returns the full output path
def get_image_output_path(image_file_obj, output_dir):
    return output_dir / f"{image_file_obj["stem"]}-exif-removed{image_file_obj["suffix"]}"

def strip_all_images(input_dir, output_dir):
    image_files = get_image_files(input_dir)

    # Loops over every image file found in the input directory and removes their EXIF data, then saves the stripped image into the output directory
    for image_file_obj in image_files:
        image_path = input_dir / image_file_obj["full"]
        output_path = get_image_output_path(image_file_obj, output_dir)
        
        print("Removing EXIF data from image:", image_file_obj["full"])
        remove_image_exif_data(image_path, output_path)

strip_all_images(input_dir, output_dir)