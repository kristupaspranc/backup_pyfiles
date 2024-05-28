from math import ceil

import keras
from keras import layers
from keras import models
import tensorflow as tf
import numpy as np

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


n_features = 20

# Generate a synthetic dataset
X, y = make_classification(n_samples=2000, n_features=n_features, n_classes=2, random_state=42)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build the Keras model
model = models.Sequential([
    layers.Input(shape=(X_train.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

batch_size = 32

def gen_func(X, y):
    def gen():
        i = 0
        n = len(X)
        while i < n:
            j = i + batch_size
            if j > n:
                yield np.pad(X[i:n], ((0,j-n),(0,0)), 'constant', constant_values=0), np.pad(y[i:n], ((0,j-n)), 'constant', constant_values=0)
                i = i + batch_size
                break
            yield X[i:j], y[i:j]
            i = i + batch_size
    
    return gen

train_steps = 1600//batch_size
print(f"Training steps: {train_steps}")
val_steps = ceil(400//batch_size)
print(f"Validation steps: {val_steps}")

# dataset_mem = tf.data.Dataset.from_tensors((X_train, y_train)).repeat(10)

dataset_gen = tf.data.Dataset.from_generator(gen_func(X_train, y_train),
     output_signature=(
         tf.TensorSpec(shape=tf.TensorShape((batch_size, n_features)), dtype=tf.float64),
         tf.TensorSpec(shape=tf.TensorShape((batch_size)), dtype=tf.int64))).repeat(2)

val_gen = tf.data.Dataset.from_generator(gen_func(X_test, y_test),
     output_signature=(
         tf.TensorSpec(shape=(batch_size, n_features), dtype=tf.float64),
         tf.TensorSpec(shape=(batch_size), dtype=tf.int64))).repeat(2)



# Train the model
# model.fit(dataset_mem, epochs=10, batch_size=32, validation_data=(X_test, y_test))
model.fit(dataset_gen, epochs=2, steps_per_epoch=train_steps, validation_data=val_gen, validation_steps=val_steps)

# # Evaluate the model on the test set
# loss, accuracy = model.evaluate(X_test, y_test)
# print(f'Test accuracy: {accuracy}')
