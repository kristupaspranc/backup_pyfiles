import unittest
import numpy as np
import os
import ROOT

def define_rdf(num_of_entries=10):
        df = ROOT.RDataFrame(num_of_entries)\
            .Define("b1", "(int) rdfentry_")\
            .Define("b2", "(double) b1*b1")
        
        return df

n_train_batch = 2
n_val_batch = 1
val_remainder = 1

def test01_each_element_is_generated_unshuffled():
        gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
        rdataframe = define_rdf(),
        batch_size=3,
        chunk_size=5,
        target="b2",
        validation_split=0.3,
        shuffle=False,
        drop_remainder=False
        )

        results_x_train = [2.0, 3.0, 4.0, 7.0, 8.0, 9.0]
        results_x_val = [0.0, 1.0, 5.0, 6.0]
        results_y_train = [4.0, 9.0, 16.0, 49.0, 64.0, 81.0]
        results_y_val = [0.0, 1.0, 25.0, 36.0]
        
        collected_x_train = []
        collected_x_val = []
        collected_y_train = []
        collected_y_val = []

        for _ in range(n_train_batch):
            x, y = next(gen_train)
            collected_x_train.append(x.tolist())
            collected_y_train.append(y.tolist())
        

        for _ in range(n_val_batch):
            x, y = next(gen_validation)
            collected_x_val.append(x.tolist())
            collected_y_val.append(y.tolist())
        
        x, y = next(gen_validation)
        collected_x_val.append(x.tolist())
        collected_y_val.append(y.tolist())

        flat_x_train = [x for xl in collected_x_train for xs in xl for x in xs]
        flat_x_val = [x for xl in collected_x_val for xs in xl for x in xs]
        flat_y_train = [y for yl in collected_y_train for ys in yl for y in ys]
        flat_y_val = [y for yl in collected_y_val for ys in yl for y in ys]
        
        print(flat_x_train)
        print(flat_x_val)
        print(flat_y_train)
        print(flat_y_val)

if __name__ == '__main__':
    # test01_each_element_is_generated_unshuffled()
    define_rdf().Snapshot("myTree","10entries.root")
