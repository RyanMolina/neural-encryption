import tensorflow as tf
import numpy as np
import random
import cv2
import os

def color_post_process(pixel):
    p = []
    for colors in pixel:
        bits = [str(color) for color in colors]
        p.append(int(''.join(bits), 2))
    return p


def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name="encryption")
        return graph


def eval_model(name, img):
    graph = load_graph(name)
    with tf.Session(graph=graph) as sess:
        X = graph.get_tensor_by_name("encryption/X_input:0")
        op_to_restore = graph.get_tensor_by_name("encryption/Output:0")
        img = [[color_post_process(np.round(sess.run(op_to_restore, feed_dict={X: colors})).astype(int).tolist())
                for colors in pixel] for pixel in img]
    return img


def process(file, model, procedure, key):
    filename, file_ext = os.path.splitext(file.filename)
    img = cv2.imread(filename+file_ext, cv2.IMREAD_UNCHANGED)
    img = img.tolist()
    img = [[[list([int(n) for n in list(str(bin(color))[2:].zfill(8))])
              for color in colors] for colors in pixel] for pixel in img]
    img = eval_model(name=model, img=img)
    img = np.array(img)
    img = diffusion(img, key, True) if procedure == "encrypt" else diffusion(img, key, False)
    img = cv2.imencode(file_ext, img)[1]
    return img


def diffusion(image, seed, diffuse=True):
    h, w, c = image.shape
    flattened = image.reshape((h*w*c, 1))
    random.seed(seed)
    flattened = shuffle(flattened) if diffuse else unshuffle(flattened)
    reshaped = flattened.reshape((h, w, c))
    return reshaped


def shuffle(l):
    for i in range(len(l)):
        j = random.randrange(i, len(l))
        l[[i]], l[[j]] = l[[j]], l[[i]]
    return l


def unshuffle(l):
    swaps = []
    for i in range(len(l)):
        j = random.randrange(i, len(l))
        swaps.append((i, j))
    for i, j in reversed(swaps):
        l[[i]], l[[j]] = l[[j]], l[[i]]
    return l
