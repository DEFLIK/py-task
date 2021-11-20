from PIL import Image
import numpy as np


def apply_grey_filter(image_name: str, chunk_size: int, gradation: int):
    img = Image.open(image_name)
    arr = np.array(img)
    width = len(arr)
    height = len(arr[1])

    for x in range(0, width, chunk_size):
        for y in range(0, height, chunk_size):
            pixels_sum = get_chunk_pixel_sum(arr, x, y, chunk_size)
            apply_grey_filter_over_chunk(arr, x, y, chunk_size, pixels_sum, gradation)

    res = Image.fromarray(arr)
    res.save('res.jpg')


def get_chunk_pixel_sum(arr: bytearray, x: int, y: int, mosaic_size: int):
    chunk = arr[x: x + mosaic_size, y: y + mosaic_size]
    return np.sum(chunk) // (mosaic_size * 10)


def apply_grey_filter_over_chunk(
        arr: bytearray, x: int,
        y: int, mosaic_size: int,
        res_pixel_rgb_sum: int,
        gradation: int):
    arr[x: x + mosaic_size, y: y + mosaic_size] = \
        [int(res_pixel_rgb_sum // (mosaic_size * 10 / 2)) * gradation / 3] * 3


print('Image file name:')
file = input()
print('Chunk size:')
chunk_s = int(input())
print('Grey gradation:')
grad = int(input())
print('Result saved as "res.jpg"')

apply_grey_filter(file, chunk_s, grad)
