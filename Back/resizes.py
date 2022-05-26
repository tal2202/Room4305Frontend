from PIL import Image
import os

path = r"old"
dirs = os.listdir(path)


def resize():
    count = 0
    for item in dirs:
        file_path = f"{path}/{item}"
        if os.path.isfile(file_path):
            im = Image.open(file_path)
            im_resize = im.resize((224, 224), Image.ANTIALIAS)
            im_resize.save(f'new/{count}.jpg', 'JPEG', quality=90)
            count += 1


resize()
