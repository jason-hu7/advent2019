from typing import List, Tuple
import numpy as np
import sys
import matplotlib.pyplot as plt


def decode_image(image_encoded: str, image_dim: Tuple[int, int]) -> np.ndarray:
    layer_width = image_dim[1]
    layer_height = image_dim[0]
    layer_size = layer_width * layer_height
    layer_num = int(len(image_encoded) / layer_size)
    # print((layer_width, layer_height, layer_num))
    image_decoded = np.zeros(shape=(layer_height, layer_width, layer_num))
    for i in range(layer_num):
        layer_i = list(image_encoded[(i*layer_size) : ((i+1)*layer_size)])
        layer_i = list(map(int, layer_i))
        image_decoded[:, :, i] = np.array(layer_i).reshape(layer_height, layer_width)
    return image_decoded


def get_fewest0_layer(image_decoded: np.ndarray) -> int:
    zero_count = []
    for i in range(image_decoded.shape[-1]):
        zeros_num = np.count_nonzero(image_decoded[:, :, i] == 0)
        zero_count.append(zeros_num)
    return np.argmin(zero_count)


def part1(image_decoded: np.ndarray) -> int:
    target_layer_num = get_fewest0_layer(image_decoded)
    target_layer = image_decoded[:, :, target_layer_num]
    one_counts = np.count_nonzero(target_layer == 1)
    two_counts = np.count_nonzero(target_layer == 2)
    return one_counts * two_counts


def final_image(image_decoded: np.ndarray) -> np.ndarray:
    layer_height, layer_width, layer_channels = image_decoded.shape
    image_final = np.zeros(shape=(layer_height, layer_width))
    for i in range(layer_height):
        for j in range(layer_width):
            pixel_stack = image_decoded[i, j, :]
            # print("pixel stack is: ", pixel_stack)
            non2_pixels = np.where(pixel_stack != 2)
            top_non2 = np.min(non2_pixels[0])
            # print("non2 pixel for each channel is: ", non2_pixels)
            # print("top non2 is: ", top_non2)
            image_final[i,j] = image_decoded[i,j,top_non2]
    return image_final


if __name__ == "__main__":
    # read data
    with open("data/input_day8.txt") as f:
        image_encoded = f.read()
    image_encoded = image_encoded.strip()
    image_dim = (6, 25)
    image_decoded = decode_image(image_encoded, image_dim)

    # unit test
    test1 = "123456789012"
    test1_decoded = decode_image(test1, (2,3))
    assert part1(test1_decoded) == 1

    print("part 1 answer is: {}".format(part1(image_decoded)))

    print("-------------------------------------part 2 start here:")

    test2 = "0222112222120000"
    test2_decoded = decode_image(test2, (2, 2))
    print(final_image(test2_decoded))
    
    part2_image = final_image(image_decoded)
    print("part 2 answer is: {}".format(part2_image))
    plt.imshow(part2_image, interpolation='nearest')
    plt.show()