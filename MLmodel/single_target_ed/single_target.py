import matplotlib.pyplot as plt
import pandas as pd
import ROOT
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split, default_collate
from sklearn.preprocessing import LabelEncoder
import numpy as np


class SonarDataset(Dataset):
    def __init__(self, X, y):
        # convert into PyTorch tensors and remember them
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        # this should return the size of the dataset
        return len(self.X)

    def __getitem__(self, idx):
        # this should return one sample from the dataset
        features = self.X[idx]
        target = self.y[idx]
        return features, target


def csv_to_root(csv_name, tree_name, file_name):
    ROOT.RDF.FromCSV(csv_name, False).Snapshot(tree_name, file_name)


def converted_data_to_csv(X, y, file_name):
    print(X.shape)
    print(y.shape)
    data_to = np.hstack((X,y))
    print(data_to.shape)

    DF = pd.DataFrame(data_to) 
    
    # save the dataframe as a csv file 
    DF.to_csv(file_name, index=True, header=False)


def model_training(if_dataloader=True):
    # set up DataLoader for data set
    if if_dataloader:
        dataset = SonarDataset(X, y)
        trainset, testset = random_split(dataset, [0.7, 0.3])
        train_loader = DataLoader(trainset, shuffle=True, batch_size=16)
        test_loader = DataLoader(testset, shuffle=False, batch_size=16)
    else:
        train_loader, test_loader = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
        tree_name="myTree",
        file_names="sonar.root",
        #file_names=["sonar_first_half.root","sonar_second_half.root"],
        batch_size=16,
        chunk_size=208,
        target="Col60",
        validation_split=0.3
        )

    # create model
    model = nn.Sequential(
        nn.Linear(60, 60),
        nn.ReLU(),
        nn.Linear(60, 30),
        nn.ReLU(),
        nn.Linear(30,1),
        nn.Sigmoid()
    )

    # Train the model
    n_epochs = 200
    loss_fn = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)
    model.train()

    losses = []
    val_losses = []


    for epoch in range(n_epochs):
        train_l = []
        val_l = []
        print("Training")
        for X_batch, y_batch in train_loader:
            y_pred = model(X_batch)
            #loss = loss_fn(y_pred, y_batch)
            loss = loss_fn(y_pred, torch.reshape(y_batch, (y_batch.shape[0], 1)))
            train_l.append(loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print("Validation")
        for X_batch, y_batch in test_loader:
            y_pred = model(X_batch)
            #loss = loss_fn(y_pred, y_batch)
            loss = loss_fn(y_pred, torch.reshape(y_batch, (y_batch.shape[0], 1)))
            val_l.append(loss.item())
        
        epoch_train_loss = sum(train_l)/len(train_l)
        epoch_val_loss = sum(val_l)/len(val_l)

        print(f"epoch = {epoch}, loss = {epoch_train_loss}, validation loss = {epoch_val_loss}")

        losses.append(epoch_train_loss)
        val_losses.append(epoch_val_loss)


    # Plot the losses
    plt.plot(val_losses,label="validation_loss")
    plt.plot(losses,label="loss")
    plt.xlabel("no. of epochs")
    plt.ylabel("total loss")
    plt.show()


def check_numbered(if_dataloader=True):
    # set up DataLoader for data set
    if if_dataloader:
        dataset = SonarDataset(X, y)
        trainset, testset = random_split(dataset, [0.7, 0.3])
        train_loader = DataLoader(trainset, shuffle=True, batch_size=16)
        test_loader = DataLoader(testset, shuffle=False, batch_size=16)
    else:
        train_loader, test_loader = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
        tree_name="myTree",
        file_name="sonar_first_half_numbered.root",
        #file_names=["sonar_first_half_numbered.root","sonar_second_half_numbered.root"],
        batch_size=16,
        chunk_size=208,
        target="Col61",
        validation_split=0.3,
        shuffle=False
        )

    print("Training")
    for X_batch, y_batch in train_loader:
        print("Train X_batch")
        print(X_batch.shape)
        print(X_batch[:,0])
        #print("Train y_batch")
        #print(y_batch[0].shape)

    print("========================================================")

    print("Validation")
    for X_batch, y_batch in test_loader:
        print("Train X_batch")
        print(X_batch.shape)
        print(X_batch[:,0])
        #print("Train y_batch")
        #print(y_batch.shape)


def two_halfs_of_data():
    data = pd.read_csv("sonar_converted")

    X_first = data.iloc[:100, 0:60].values
    y_first = data.iloc[:100, 60].values

    X_second = data.iloc[100:, 0:60].values
    y_second = data.iloc[100:, 60].values

    print(X_first.shape)
    print(np.reshape(y_first,(y_first.shape[0],1)).shape)
    print(X_second.shape)
    print(np.reshape(y_second,(y_second.shape[0],1)).shape)
    
    converted_data_to_csv(X_first, np.reshape(y_first,(y_first.shape[0],1)),"sonar_first_half_numbered")
    converted_data_to_csv(X_second, np.reshape(y_second,(y_second.shape[0],1)),"sonar_second_half_numbered")

    csv_to_root("sonar_first_half_numbered","myTree","sonar_first_half_numbered.root")
    csv_to_root("sonar_second_half_numbered","myTree","sonar_second_half_numbered.root")


if __name__ == "__main__":
    # Read data, convert to NumPy arrays
    # data = pd.read_csv("sonar")
    # X = data.iloc[:, 0:60].values
    # y = data.iloc[:, 60].values

    # # encode class values as integers
    # encoder = LabelEncoder()
    # encoder.fit(y)
    # y = encoder.transform(y).reshape(-1, 1)

    # converted_data_to_csv(X,y,"sonar_converted")

    #csv_to_root("sonar_converted","myTree","sonar.root")

    # df = ROOT.RDataFrame("myTree", "sonar.root")
    # print(df.Describe())

    #model_training()
    check_numbered(False)
    #two_halfs_of_data()