import tensorflow as tf

# Placeholder to hold the input data
N_STEPS = 500000

N_INPUT_NODES = 8
N_OUTPUT_NODES = 8
N_HIDDEN_NODES = 8

X = tf.placeholder(tf.float32, shape=[None, N_INPUT_NODES], name="X_input")
Y = tf.placeholder(tf.float32, shape=[None, N_OUTPUT_NODES], name="Y_input")


def get_data():
    x = []
    y = []
    for i in range(256):
        plaintext = str(bin(i))[2:].zfill(8)
        ms_nibble = plaintext[:4]
        ls_nibble = plaintext[4:]
        encrypted = ls_nibble+ms_nibble
        x.append(list(plaintext))
        y.append(list(encrypted))
    return x, y


def train(feed_dict, name=None):
    # Setup the parameters for the network.
    theta1 = tf.Variable(tf.random_uniform([N_INPUT_NODES, N_HIDDEN_NODES]), name="Theta_1")
    theta2 = tf.Variable(tf.random_uniform([N_HIDDEN_NODES, N_OUTPUT_NODES]), name="Theta_2")

    bias1 = tf.Variable(tf.random_normal([N_HIDDEN_NODES], 0, 1), name="Bias1")
    bias2 = tf.Variable(tf.random_normal([N_OUTPUT_NODES], 0, 1), name="Bias2")

    layer1 = tf.sigmoid(tf.matmul(X, theta1) + bias1)
    output = tf.sigmoid(tf.matmul(layer1, theta2) + bias2, name='Output')

    cost = tf.reduce_mean(tf.square(Y-output))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        for i in range(N_STEPS):
            sess.run(optimizer, feed_dict=feed_dict)
        if name:
            saver = tf.train.Saver()
            saver.save(sess, name, global_step=N_STEPS)


if __name__ == '__main__':
    training_input, training_output = get_data()
    print("training")
    train({X: training_input, Y: training_output}, name="checkpoint/encryptor_model")