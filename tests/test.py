import unittest

import ROOT

class RBatchGeneratorMultipleFiles(unittest.TestCase):

    file_name1 = "first_half.root"
    file_name2 = "second_half.root"
    tree_name = "mytree"

    # Helpers
    def create_two_files(self):
        df1 = ROOT.RDataFrame(20)\
            .Define("b1", "(int) rdfentry_")\
            .Define("b2", "(double) rdfentry_ * rdfentry_")\
            .Snapshot(self.tree_name, self.file_name1)

        df2 = ROOT.RDataFrame(10)\
            .Define("b1", "(int) rdfentry_ + 20")\
            .Define("b2", "(double) b1*b1")\
            .Snapshot(self.tree_name, self.file_name2)
        
        #print(df1.Describe())
        #print(df2.Describe())

        #df2.Display("",).Print()

    def foo(self):
        ROOT.TMVA.Experimental.CreatePyTorchGenerators(
        tree_name=self.tree_name,
        file_names=[self.file_name1, self.file_name2],
        batch_size=10,
        chunk_size=30,
        target="b2",
        validation_split=0.3
        )

if __name__ == 'main':
    unittest.main()

#a = RBatchGeneratorMultipleFiles()
#a.create_two_files()