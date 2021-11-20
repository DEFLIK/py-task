from PIL import Image
import numpy as np
import cProfile


def apply_grey_filter(image_name: str, chunk_size: int, gradation: int):
    """
    Applying grey filter to initial image, result will be saved as res.jpg
    :param image_name: initial image path
    :param chunk_size: size of pixel chunks into which initial image will be divided
    :param gradation: gradation of grey color (less - darker, more - lighter)
    >>> initImage = Image.fromarray(\
            (np.array([[[255, 127, 39], [34, 177, 76]],[[63, 72, 204], [63, 72, 204]]])).astype(np.uint8))
    >>> initImage.save('_testImage.jpg')
    >>> apply_grey_filter('_testImage.jpg', 1, 50)
    >>> img = Image.open('res.jpg')
    >>> arr = np.array(img)
    >>> np.array_equal(arr, [[[142, 142, 142], [140, 140, 140]],[[91, 91, 91], [89, 89, 89]]])
    True
    """
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


def get_chunk_pixel_sum(arr: bytearray, x: int, y: int, chunk_size: int):
    """
    Counts sum of pixels in one chunk
    :param arr: array of pixels from initial image
    :param x: chunk left-top corner X coordinate relative to the array
    :param y: chunk left-top corner Y coordinate relative to the array
    :param chunk_size: initial chunk size
    :return: result sum
    >>> get_chunk_pixel_sum(np.array([[[255, 127, 39], [34, 177, 76]],[[63, 72, 204], [63, 72, 204]]]), 0, 0, 2)
    69
    """
    chunk = arr[x: x + chunk_size, y: y + chunk_size]
    return np.sum(chunk) // (chunk_size * 10)


def apply_grey_filter_over_chunk(
        arr: bytearray,
        x: int,
        y: int,
        chunk_size: int,
        res_pixel_rgb_sum: int,
        gradation: int):
    """
    Applying grey filter to one chunk
    :param arr: array of pixels from initial image
    :param x: chunk left-top corner X coordinate relative to the array
    :param y: chunk left-top corner Y coordinate relative to the array
    :param chunk_size: initial chunk size
    :param res_pixel_rgb_sum: sum of pixels inside current chunk
    :param gradation: gradation of gery color (less - darker, more - lighter)
    """
    arr[x: x + chunk_size, y: y + chunk_size] = \
        [int(res_pixel_rgb_sum // (chunk_size * 10 / 2)) * gradation / 3] * 3


if __name__ == '__main__':
    print('Image file name:')
    file = input()
    print('Chunk size:')
    chunk_s = int(input())
    print('Grey gradation:')
    grad = int(input())
    print('Result saved as "res.jpg"')

    pr = cProfile.Profile()
    pr.enable()
    apply_grey_filter(file, chunk_s, grad)
    pr.disable()
    pr.print_stats(sort=1)
