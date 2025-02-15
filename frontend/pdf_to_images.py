from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(os.path.join(output_folder, f"page_{i + 1}.png"), "PNG")