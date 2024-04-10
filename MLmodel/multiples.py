import matplotlib.pyplot as plt
import ROOT
import random
import pandas as pd
import tensorflow as tf
import torch
from torch.utils.data import Dataset, DataLoader

torch.manual_seed(42)
random.seed(42)

csv_name = "testfile"
tree_name = "myTree"
file_name = "multiples_py.root"

class CheckEquality:
    def __init__(self, gen_train, gen_validation, train_loader, validation_loader, what_type="torch"):

        if what_type == "torch":
            print("Checking torch")
            self.batch_gen_train_x, self.batch_gen_train_y = self.fill_list(gen_train)
            self.batch_gen_validation_x, self.batch_gen_validation_y = self.fill_list(gen_validation)
        elif what_type == "numpy":
            print("Checking numpy")
            self.batch_gen_train_x, self.batch_gen_train_y = self.fill_list_numpy(gen_train)
            self.batch_gen_validation_x, self.batch_gen_validation_y = self.fill_list_numpy(gen_validation)
        elif what_type == "tf":
            print("Checking tf")
            self.batch_gen_train_x, self.batch_gen_train_y = self.fill_list_tf(gen_train)
            self.batch_gen_validation_x, self.batch_gen_validation_y = self.fill_list_tf(gen_validation)
        else:
            raise "Given type does not exist"


        self.train_loader_x, self.train_loader_y = self.fill_list(train_loader)
        self.validation_loader_x, self.validation_loader_y = self.fill_list(validation_loader)
    
    def fill_list(self, generator):
        list_x = []
        list_y = []

        for x, y in generator:
            list_x.append(x)
            list_y.append(y)
        
        return list_x, list_y
    
    def fill_list_numpy(self, generator):
        list_x = []
        list_y = []

        for x, y in generator:
            list_x.append(torch.from_numpy(x))
            list_y.append(torch.from_numpy(y))
        
        return list_x, list_y
    
    def fill_list_tf(self, generator):
        list_x = []
        list_y = []

        for x, y in generator:
            list_x.append(torch.from_numpy(x.numpy()))
            list_y.append(torch.from_numpy(y.numpy()))
        
        return list_x, list_y

    def check_if_equal(self, list_one, list_two):
        length_one = len(list_one)
        if length_one != len(list_two):
            print("Lenghts do not mach")
            return False
        
        for i in range(length_one):
            if not torch.equal(list_one[i], list_two[i]):
                print("Elements do not match")
                return False
        
        return True
    
    def check_it(self):
        print("Checking if train x batches are equal")
        print(self.check_if_equal(self.batch_gen_train_x, self.train_loader_x))

        print("Checking if train y batches are equal")
        print(self.check_if_equal(self.batch_gen_train_y, self.train_loader_y))

        print("Checking if validation x batches are equal")
        print(self.check_if_equal(self.batch_gen_validation_x, self.validation_loader_x))

        print("Checking if validation y batches are equal")
        print(self.check_if_equal(self.batch_gen_validation_y, self.validation_loader_y))


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
        df.to_csv(csv_name,index=False)

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


class DataIterator(Dataset):
    def __init__(self, data):
        self.x, self.y = data
        self.len = self.x.shape[0]
    
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
    
    def __len__(self):
        return self.len


# Creating a custom Multiple Linear Regression Model
class MultipleLinearRegression(torch.nn.Module):
    # Constructor
    def __init__(self, input_dim, output_dim):
        super(MultipleLinearRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)
    # Prediction
    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred


def check_numpy(train_loader, validation_loader):
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
    tree_name=tree_name,
    file_name=file_name,
    batch_size=400,
    chunk_size=4000,
    target=["2","3"],
    validation_split=0.3,
    shuffle=False
    )

    a = CheckEquality(gen_train, gen_validation, train_loader, validation_loader, "numpy")
    a.check_it()


def check_tf(train_loader, validation_loader):
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreateTFDatasets(
    tree_name=tree_name,
    file_name=file_name,
    batch_size=400,
    chunk_size=4000,
    target=["2","3"],
    validation_split=0.3,
    shuffle=False
    )

    a = CheckEquality(gen_train, gen_validation, train_loader, validation_loader, "tf")
    a.check_it()


def csv_to_root():
    ROOT.RDF.FromCSV(csv_name, True).Snapshot(tree_name, file_name)


def root_missing_data():
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
    tree_name=tree_name,
    file_name=file_name,
    batch_size=400,
    chunk_size=2000,
    target=["2","3"],
    validation_split=0.3,
    )
    print("Training")
    for x, y in gen_train:
        print(f"x: {x.shape}, y: {y.shape}")
    print("Validation")
    for x, y in gen_validation:
        print(f"x: {x.shape}, y: {y.shape}")


def training_and_validating_data(gen_train, gen_validation):   
    losses = []
    val_losses = []
    epochs = 10

    for epoch in range(epochs):
        train_l = []
        val_l = []

        # train model
        for x,y in gen_train:
            y_pred = MLR_model(x)
            loss = criterion(y_pred, y)
            train_l.append(loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


        # validate model
        print("Validating")
        for x,y in gen_validation:
            y_pred = MLR_model(x)
            v_loss = criterion(y_pred,y)
            val_l.append(v_loss.item())

        epoch_train_loss = sum(train_l)/len(train_l)
        epoch_val_loss = sum(val_l)/len(val_l)

        print(f"epoch = {epoch}, loss = {epoch_train_loss}, validation loss = {epoch_val_loss}")

        losses.append(epoch_train_loss)
        val_losses.append(epoch_val_loss)
    
    print("Done training!")

    # Plot the losses
    plt.plot(val_losses)
    plt.plot(losses)
    plt.xlabel("no. of epochs")
    plt.ylabel("total loss")
    plt.show()


if __name__ == "__main__":
    # model object
    MLR_model = MultipleLinearRegression(2,2)
    # model optimizer
    optimizer = torch.optim.SGD(MLR_model.parameters(), lr=0.1)
    # loss criterion
    criterion = torch.nn.MSELoss()


    # pytorch data generators
    data_generator = Data()
    train_data = DataIterator(data_generator.get_train_data())
    validation_data = DataIterator(data_generator.get_validation_data())

    train_loader = DataLoader(dataset=train_data, batch_size=400)
    validation_loader = DataLoader(dataset=validation_data, batch_size=400)


    # R_batch_generator
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
    tree_name=tree_name,
    file_name=file_name,
    batch_size=400,
    chunk_size=4000,
    target=["2","3"],
    validation_split=0.3,
    shuffle=False
    )


    """save data to folder, must for the first time"""
    #data_generator.torch_to_csv()
    #csv_to_root()

    """train and validate model with RBatchGenerator"""
    training_and_validating_data(gen_train, gen_validation)

    """train and validate model with pytorch generator"""
    #training_and_validating_data(train_loader, validation_loader)

    """check if created PYTORCH batches by rbatchgenerator are equal, must: shuffle=False"""
    #a = CheckEquality(gen_train, gen_validation, train_loader, validation_loader)
    #a.check_it()

    """check if created NUMPY batches by rbatchgenerator are equal, must: shuffle=False"""
    #check_numpy(train_loader, validation_loader)

    """check if created TF batches are by rbatchgenerator equal, must: shuffle=False"""
    #check_tf(train_loader, validation_loader)