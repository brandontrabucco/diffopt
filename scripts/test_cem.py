"""Author: Brandon Trabucco, Copyright 2019, MIT License"""


from controls import cem
from controls import shooting
import tensorflow as tf


if __name__ == "__main__":

    A = tf.constant([[[-0.313, 56.7, 0.0],
                      [-0.0139, -0.426, 0.0],
                      [0.0, 56.7, 0.0]]])

    B = tf.constant([[[0.232],
                      [0.0203],
                      [0.0]]])

    Q = tf.constant([[[0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0]]])

    R = tf.constant([[[1.0]]])

    def controls_model(x):
        return tf.zeros([tf.shape(x[0])[0], 1, 1])

    def dynamics_model(x):
        return A @ x[0] + B @ x[1]

    def cost_model(x):
        return 0.5 * tf.matmul(
            tf.matmul(x[0], Q, transpose_a=True), x[0]) + 0.5 * tf.matmul(
            tf.matmul(x[1], R, transpose_a=True), x[1])

    initial_states = tf.random.normal([1, 3, 1])

    controls_model = cem(
        initial_states,
        controls_model,
        dynamics_model,
        cost_model,
        horizon=20,
        num_candidates=1000,
        num_iterations=100,
        top_k=100,
        exploration_noise_std=1.0)

    shooting_states, shooting_controls, shooting_costs = shooting(
        initial_states, controls_model, dynamics_model, cost_model, 20)

    for i in range(20):

        costs = shooting_costs[i, ...]

        print("Cost: {}".format(costs.numpy().sum()))
