import matplotlib.pyplot as plt
import numpy as np
import json


def display_image(x_test, image_index):
    plt.imshow(x_test[image_index].reshape(28, 28), cmap="binary")
    plt.show()


with np.load("training_data/mnist.npz", allow_pickle=True) as f:
    x_test = f["x_test"] / 255.0

image_index = 1005

display_image(x_test, image_index)
tf_serving_req = {"instances": x_test[image_index : image_index + 1].tolist()}

with open("input.json", "w") as json_file:
    json.dump(tf_serving_req, json_file)
