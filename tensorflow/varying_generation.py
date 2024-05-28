import tensorflow as tf
import numpy as np

# max_data_size = 4

# # Define a simple model
# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(10, activation='relu', input_shape=(max_data_size,)),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# def data_generator():
#     for i in range(100):
#         # Generate data with varying sizes
#         size = np.random.randint(1, 5)  # Random size between 1 and 4
#         data = np.random.rand(size)
#         label = np.random.randint(0, 2)  # Random label 0 or 1

#         padded_data = np.pad(data, (0, max_data_size - size), 'constant', constant_values=0).reshape(-1,1).transpose()

#         yield padded_data, label

# Define output signature based on the actual data

# Create a dataset
# dataset = tf.data.Dataset.from_generator(data_generator, output_signature=(
#         tf.TensorSpec(shape=(None, max_data_size), dtype=tf.float32), tf.TensorSpec(shape=(None, 1), dtype=tf.int32)))

# dataset_gen = tf.data.Dataset.from_generator(gen_func(X_train, y_train),
#      output_signature=(
#          tf.TensorSpec(shape=tf.TensorShape((None, n_features)), dtype=tf.float64),
#          tf.TensorSpec(shape=tf.TensorShape((None)), dtype=tf.int64))).repeat(10)

# for i in dataset:
#     print(i[0].shape)
#     print(i[1])

# model.fit(dataset, epochs=10)

# a = np.array(((1,2),(3,4),(5,6)))
# print(a)
# b = np.pad(a, ((0,3),(0,0)), 'constant', constant_values=0)
# print(b)

a = tf.constant([[1,2],[3,4]])
print(a)

b = tf.pad(a, tf.constant([[0,2],[0,0]]))
print(b)
