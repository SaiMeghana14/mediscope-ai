from PIL import Image
import io

def load_image(image_file):
    return Image.open(image_file)

def save_upload_file(uploaded_file, destination):
    with open(destination, "wb") as buffer:
        buffer.write(uploaded_file.file.read())
