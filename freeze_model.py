import os, argparse
import tensorflow as tf
from tensorflow.python.framework import graph_util


dir = os.path.dirname(os.path.realpath(__file__))

def freeze_graph(model_folder, frozen_model):
    checkpoint = tf.train.get_checkpoint_state(model_folder)
    input_checkpoint = checkpoint.model_checkpoint_path

    absolute_model_folder = "/".join(input_checkpoint.split('/')[:-1])
    output_graph = absolute_model_folder + frozen_model

    output_node_names = "Output"
    clear_devices = True

    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=clear_devices)

    graph = tf.get_default_graph()
    input_graph_def = graph.as_graph_def()

    with tf.Session() as sess:
        saver.restore(sess, input_checkpoint)
        output_graph_def = graph_util.convert_variables_to_constants(
            sess,
            input_graph_def,
            output_node_names.split(",")
        )
        with tf.gfile.GFile(output_graph, "wb") as f:
            f.write(output_graph_def.SerializeToString())

        print("{} ops in the final graph.".format(len(output_graph_def.node)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_folder", type=str, help="Model folder to export")
    parser.add_argument("--frozen_model", type=str, help="Frozen model filename")
    args = parser.parse_args()

    freeze_graph(args.model_folder, args.frozen_model)
