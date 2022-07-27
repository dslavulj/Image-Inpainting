"""
Author: Danijel Slavulj
"""

import os
import sys
import numpy as np

def ex4(image_array, offset, spacing):

    if not isinstance(image_array, np.ndarray):
            raise TypeError('image_array is not a numpy array')

    if image_array.ndim != 3 or image_array.shape[2] !=3:
        raise NotImplementedError('image_array is not 3D array or 3rd dimension is not equal to 3')

    try:
        int(offset[0])
        int(offset[1])
        int(spacing[0])
        int(spacing[1])
    except:
        raise ValueError('offset and spacing are not convertible to int objects')

    if offset[0] < 0 or offset[0] > 32 or offset[1] < 0 or offset[1] > 32:
        raise ValueError('values in offset are smaller than 0 or larger than 32')
        
    if spacing[0] < 2 or spacing[0] > 8 or spacing[1] < 2 or spacing[1] > 8:
        raise ValueError('values in spacing are smaller than 0 or larger than 32')

    input_array = image_array.copy()
    known_array = np.ones_like(image_array)
    target_array = [[],[],[]]

    i=0

    for m in range (input_array.shape[0]):
        for n in range (input_array.shape[1]):
            if n < offset[0] or m < offset[1] or n%spacing[0] != offset[0]%spacing[0]or m%spacing[1] != offset[1]%spacing[1]:
                target_array[0].append(input_array[m][n][0])
                target_array[1].append(input_array[m][n][1])
                target_array[2].append(input_array[m][n][2])

                input_array[m][n][0], input_array[m][n][1], input_array[m][n][2] = 0, 0, 0
                known_array[m][n][0], known_array[m][n][1], known_array[m][n][2] = 0, 0, 0
            else:
                i+=1

    target_array = np.array(target_array).flatten()
    input_array = np.transpose(input_array, (2, 0, 1))
    known_array = np.transpose(known_array, (2, 0, 1))


    if i < 144:
        raise ValueError("remaining known image pixels smaller than 144")

    return (input_array, known_array, target_array)
