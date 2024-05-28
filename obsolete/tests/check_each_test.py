import os
import ROOT
import numpy as np

class Checking():
    file_name1 = "first_half.root"
    file_name2 = "second_half.root"
    tree_name = "mytree"

    # default constants
    n_train_batch = 2
    n_val_batch = 1
    val_remainder = 1

    # Helpers
    def define_rdf(self, num_of_entries=10):
        df = ROOT.RDataFrame(num_of_entries)\
            .Define("b1", "(int) rdfentry_")\
            .Define("b2", "(double) b1*b1")
        
        return df

    def create_file(self, num_of_entries=10):
        self.define_rdf(num_of_entries).Snapshot(self.tree_name, self.file_name1)
    
    def create_5_entries_file(self):
        df1 = ROOT.RDataFrame(5)\
            .Define("b1", "(int) rdfentry_ + 10")\
            .Define("b2", "(double) b1 * b1")\
            .Snapshot(self.tree_name, self.file_name2)

    def teardown_file(self, file):
        os.remove(file)

    def test01_each_element_is_generated_unshuffled(self):
        self.create_file()

        try:
            df = ROOT.RDataFrame(self.tree_name, self.file_name1)
            
            gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
                df,
                batch_size=3,
                chunk_size=5,
                target="b2",
                validation_split=0.4,
                shuffle=True,
                drop_remainder=False
            )
            
            both_epochs_collected_x_train = []
            both_epochs_collected_x_val = []
            both_epochs_collected_y_train = []
            both_epochs_collected_y_val = []

            for i in range(2):
                print(f"Epoch number {i}")
                collected_x_train = []
                collected_x_val = []
                collected_y_train = []
                collected_y_val = []

                iter_train = iter(gen_train)
                iter_val = iter(gen_validation)

                print("Training")
                for _ in range(self.n_train_batch):
                    x, y = next(iter_train)
                    print(x)
                    print(y)
                    collected_x_train.append(x.tolist())
                    collected_y_train.append(y.tolist())
                
                print("Validation")
                for _ in range(self.n_val_batch):
                    x, y = next(iter_val)
                    print(x)
                    print(y)
                    collected_x_val.append(x.tolist())
                    collected_y_val.append(y.tolist())
                
                x, y = next(iter_val)
                collected_x_val.append(x.tolist())
                collected_y_val.append(y.tolist())

                flat_x_train = {x for xl in collected_x_train for xs in xl for x in xs}
                flat_x_val = {x for xl in collected_x_val for xs in xl for x in xs}
                flat_y_train = {y for yl in collected_y_train for ys in yl for y in ys}
                flat_y_val = {y for yl in collected_y_val for ys in yl for y in ys}

                both_epochs_collected_x_train.append(collected_x_train)
                both_epochs_collected_x_val.append(collected_x_val)
                both_epochs_collected_y_train.append(collected_y_train)
                both_epochs_collected_y_val.append(collected_y_val)

            self.teardown_file(self.file_name1)

        except:
            self.teardown_file(self.file_name1)
            raise


testing = Checking()

testing.test01_each_element_is_generated_unshuffled()
