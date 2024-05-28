"""
import numpy as np

a = np.arange(20).reshape(4, 5)

print(a)


target_indices = [2,4]
weight_index = 3
#print(np.delete(a, (1,3), 1))

# Splice target column(s) from the data if target is given
def splitting_array(return_data, target_indices, weights_index):
    if True:
        target_data = return_data[:, target_indices]

        #Splice weight column from the data if weight is given
        if True:
            weights_data = return_data[:, weights_index]
            train_data = np.delete(return_data, target_indices + [weights_index], 1)

            return train_data, target_data, weights_data

        train_data = np.delete(return_data, target_indices, 1)

        return train_data, target_data

    return return_data

#print(type(target_indices[0]),type(target_indices[1]))



def print_results():
    train_data, target_data, weights_data = splitting_array(a, target_indices, weight_index)

    print(train_data)
    print(target_data)
    print(weights_data)

print_results()

#print(type(target_indices + [weight_index]))
"""

"""
import tensorflow as tf

t1 = tf.constant([[0,1,2,3],
                 [4,5,6,7],
                [8,9,10,11],
                [12,13,14,15]])

print(t1[:,1:3])                
"""


"""
import torch

t2 = torch.tensor([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9,10,11,12]])

#print(t2.gather(t2, 1, torch.tensor([1,2])))
print(t2[:,[1,3]])
"""

def pog(target = list()):
    print(len(target)>0)

pog()