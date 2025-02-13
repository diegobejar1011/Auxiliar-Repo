import tensorflow as tf
import random

class Model:
    def __init__(self, input_dim, lr):
        self.W = tf.Variable(tf.random.normal(shape=(input_dim, 1), stddev=0.1), dtype=tf.float32)
        self.b = tf.Variable(tf.zeros(shape=(1,)), dtype=tf.float32)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=lr)

    def train(self, X_train, y_train, epochs=100):
        loss_history = []
        initial_weights = (self.W.numpy(), self.b.numpy())  
        for epoch in range(epochs):
            with tf.GradientTape() as tape:
                y_pred = tf.matmul(X_train, self.W) + self.b
                loss = tf.reduce_mean(tf.square(y_train - y_pred))
            gradients = tape.gradient(loss, [self.W, self.b])
            self.optimizer.apply_gradients(zip(gradients, [self.W, self.b]))
            loss_history.append(loss.numpy())

        final_weights = (self.W.numpy(), self.b.numpy()) 
        error = abs(loss_history[-1]) 
        return loss_history, initial_weights, final_weights, error, epochs
