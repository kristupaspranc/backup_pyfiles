import tensorflow as tf
import numpy as np

a = np.array((0,1,2,3,4,5,6,7,8,9))

def gen():

    for i in range(0,len(a),2):
        np.random.shuffle(a)
        yield a[i:i+2]

# for i in gen():
#     print(i)

df = tf.data.Dataset.from_generator(gen, output_signature=(tf.TensorSpec(shape=(2,), dtype=tf.int64))).cache().repeat(2)

for i in df:
    print(i)

print("Round two")

for i in df:
    print(i)
