"""
Author: Danijel Slavulj
"""

import os
import glob
import numpy as np
from PIL import Image, ImageStat

class ImageStandardizer:
    def __init__(self, input_dir):
        if not os.path.isdir(input_dir):
            raise ValueError("'input_dir' must be an existing directory")

        #Scan this input directory recursively for files ending in .jpg.
        image_files = glob.glob(os.path.join(input_dir, "**", "*.jpg"), recursive=True)

        #Raise a ValueError if there are no .jpg file
        if len(image_files) == 0:
            raise ValueError("No .jpg files found")

        #Transform all paths to absolute paths and sort them alphabetically in ascending order.
        for i in range(len(image_files)):
            image_files[i] = os.path.abspath(image_files[i])
        image_files = sorted(image_files)

        #Store the sorted absolute file paths in an attribute self.files
        self.files = image_files

        #Create an attribute self.mean with value None.
        self.mean = None

        #Create an attribute self.std with value None.
        self.std = None

    def analyze_images(self):
        mean_sum = np.array([0., 0., 0.], dtype=np.float64)
        std_sum = np.array([0., 0., 0.], dtype=np.float64)

        #Compute the means and standard deviations for each color channel of all images in the list self.files
        for file in self.files:
            with Image.open(file) as image:
                mean_sum = np.add(mean_sum, np.array(ImageStat.Stat(image).mean, dtype=np.float64))
                std_sum = np.add(std_sum, np.array(ImageStat.Stat(image).stddev, dtype=np.float64))

        #Store the average over these RGB means of all images in the attribute self.mean
        self.mean = (mean_sum / len(self.files))

        #Store the average over these RGB standard deviations of all images in the attribute self.std
        self.std = (std_sum / len(self.files))

        return (self.mean, self.std)

    def get_standardized_images(self):
        #Raise a ValueError if self.mean or self.std is None.
        if self.mean is None or self.std is None:
            raise ValueError("self.mean or self.std is None")
        
        #Yield the pixel data of each image (generator function), i.e., the raw numpy data with shape (H, W, 3), in the order that the image files appear in self.files.
        for file in self.files:
            with Image.open(file) as image:
                #Load the image and store the image data (pixels) in a 3D numpy array of datatype np.float32.
                image = np.array(image).astype(np.float64)

                #Standardize the image data using the global RGB mean and standard deviation
                st_image = (image - self.mean) / self.std

                #Yield the standardized image data as 3D numpy array of datatype np.float32.
                yield st_image.astype(np.float32)
