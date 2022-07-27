"""
Author: Danijel Slavulj
"""
import os
import glob
import shutil
import numpy as np
import hashlib
from PIL import Image, ImageStat


def validate_images(input_dir, output_dir, log_file, formatter=None):
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    log_file = os.path.abspath(log_file)

    if not os.path.isdir(input_dir):
        raise ValueError("'input_dir' must be an existing directory")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(log_file, "w+") as f:
        f.write("")
    
    image_files = sorted(glob.glob(os.path.join(input_dir, "**", "*"), recursive=True))
    hashes=[]
    n = 0
    for i, image_file in enumerate(image_files):
        if os.path.isdir(image_file):
            continue
        file_name, file_extension = os.path.splitext(image_file)

        #1. The file name ends with .jpg, .JPG, .jpeg or .JPEG
        if file_extension not in [".jpg", ".JPG", ".jpeg", ".JPEG"]:
            filename = file_name.split('\\')[-1] + file_extension + ";1" + "\n"
            with open(log_file, "a") as f:
                    f.write(filename)
            continue

        #2. The file size does not exceed 250kB (=250 000 Bytes).
        if os.path.getsize(image_file) > 250000:
            filename = file_name.split('\\')[-1] + file_extension + ";2" + "\n"
            with open(log_file, "a") as f:
                    f.write(filename)
            continue

        #3. The file can be read as image (i.e., the PIL/pillow module does not raise an exception when reading the file).
        try:
            im = Image.open(image_file)
            im.verify()
        except:
            filename = file_name.split('\\')[-1] + file_extension + ";3" + "\n"
            with open(log_file, "a") as f:
                    f.write(filename)
            continue

        #4. The image data has a shape of (H, W, 3) with H (height) and W (width) larger than or equal to 96 pixels. The three channels must be in the order RGB (red, green, blue).
        with Image.open(image_file) as image:
            if image.width < 96 or image.height < 96 or image.mode != "RGB":
                filename = file_name.split('\\')[-1] + file_extension + ";4" + "\n"
                with open(log_file, "a") as f:
                        f.write(filename)
                continue

        #5. The image data has a variance larger than 0, i.e., there is not just one common RGB pixel in the image data.
            if np.mean(ImageStat.Stat(image).var) <= 0:
                filename = file_name.split('\\')[-1] + file_extension + ";5" + "\n"
                with open(log_file, "a") as f:
                        f.write(filename)
                continue

        #6. The same image has not been copied already
            hash = hashlib.md5(image.tobytes()).hexdigest()
            if hash in hashes:
                filename = file_name.split('\\')[-1] + file_extension + ";6" + "\n"
                with open(log_file, "a") as f:
                        f.write(filename)
                continue
            else:
                hashes.append(hash)

        if formatter != None:
            string = "{:" + formatter + "}.jpg"
            filename = string .format(n)
            shutil.copy(image_file, os.path.join(output_dir, filename))

        else:
            filename = str(n) + ".jpg"
            shutil.copy(image_file, os.path.join(output_dir, filename))
        n+=1
