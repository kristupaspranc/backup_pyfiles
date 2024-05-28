import pandas as pd
import random
import ROOT
import torch

random.seed(42)
csv_name = "ints_and_strings"
tree_name = "myTree"
file_name = "ints_and_strings.root"

class Data():
    def __init__(self, if_shuffle = False):
        self.x = torch.zeros(4000, 2)
        self.x[:, 0] = torch.arange(-2, 2, 0.001)
        self.x[:, 1] = torch.arange(-2, 2, 0.001)
        w = torch.tensor([[1.0, 2.0], [2.0, 4.0]])
        b = 1
        func = torch.mm(self.x, w) + b    
        self.y = func + 0.2 * torch.randn((self.x.shape[0],1))
        self.len = self.x.shape[0]
        self.validation_split = 0.3
        self.shuffle = if_shuffle
        self.train_indices, self.validation_indices = self.indices_to_split()

    def torch_to_csv(self):
        df = pd.DataFrame(torch.cat((self.x,self.y),1).numpy())
        #df = pd.DataFrame(self.x.numpy())
        df.to_csv(csv_name,index=False,header=["a1","a2","a3","a4"])

    def indices_to_split(self):
        self.indices = [x for x in range(self.len)]
        if self.shuffle:
            random.shuffle(self.indices)
        self.split_index = round(self.validation_split * self.len)
        
        return self.indices[self.split_index:], self.indices[:self.split_index]
    
    def get_train_data(self):
        return torch.index_select(self.x, 0, torch.LongTensor(self.train_indices)), torch.index_select(self.y, 0, torch.LongTensor(self.train_indices))
    
    def get_validation_data(self):
        return torch.index_select(self.x, 0, torch.LongTensor(self.validation_indices)), torch.index_select(self.y, 0, torch.LongTensor(self.validation_indices))
    
    def get_type(self):
        print(type(self.x[0][0][0]))


def csv_to_root():
    ROOT.RDF.FromCSV(csv_name, True).Snapshot(tree_name, file_name)

def create_pandas_csv():
    d = {'col1': [1, 2], 'col2': ["string1", "string2"]}

    df = pd.DataFrame(data=d)

    df.to_csv("ints_and_strings", index=False, header=["b1","b2"])


if __name__ == "__main__":
    a = Data()
    a.get_type()
    # a.torch_to_csv()
    # csv_to_root()
    # create_pandas_csv()