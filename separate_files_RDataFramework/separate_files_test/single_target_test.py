import matplotlib.pyplot as plt
import ROOT
import torch.nn as nn
import torch.optim as optim


def model_training_one_file():
    train_loader, test_loader = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
        tree_name="myTree",
        file_names="sonar.root",
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
            loss = loss_fn(y_pred, y_batch)
            train_l.append(loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print("Validation")
        for X_batch, y_batch in test_loader:
            y_pred = model(X_batch)
            loss = loss_fn(y_pred, y_batch)
            val_l.append(loss.item())
        
        epoch_train_loss = sum(train_l)/len(train_l)
        epoch_val_loss = sum(val_l)/len(val_l)

        print(f"epoch = {epoch}, loss = {epoch_train_loss}, validation loss = {epoch_val_loss}")

        losses.append(epoch_train_loss)
        val_losses.append(epoch_val_loss)


    # Plot the losses
    plt.plot(val_losses)
    plt.plot(losses)
    plt.xlabel("no. of epochs")
    plt.ylabel("total loss")
    plt.show()


def model_training_two_files():
    train_loader, test_loader = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
        tree_name="myTree",
        file_names=["sonar_first_half.root","sonar_second_half.root"],
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
            loss = loss_fn(y_pred, y_batch)
            train_l.append(loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print("Validation")
        for X_batch, y_batch in test_loader:
            y_pred = model(X_batch)
            loss = loss_fn(y_pred, y_batch)
            val_l.append(loss.item())
        
        epoch_train_loss = sum(train_l)/len(train_l)
        epoch_val_loss = sum(val_l)/len(val_l)

        print(f"epoch = {epoch}, loss = {epoch_train_loss}, validation loss = {epoch_val_loss}")

        losses.append(epoch_train_loss)
        val_losses.append(epoch_val_loss)


    # Plot the losses
    plt.plot(val_losses)
    plt.plot(losses)
    plt.xlabel("no. of epochs")
    plt.ylabel("total loss")
    plt.show()


def check_numbered():
    train_loader, test_loader = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
        tree_name="myTree",
        file_name = "sonar_first_half_numbered.root",
        #file_names=["sonar_first_half_numbered.root","sonar_second_half_numbered.root"],
        batch_size=16,
        chunk_size=208,
        target="Col61",
        validation_split=0.3,
        shuffle=True
        )
    for _ in range(2):
        print("Training")
        for X_batch, y_batch in train_loader:
            print("Train X_batch")
            print(X_batch.shape)
            print(X_batch[:,0])

        print("========================================================")

        print("Validation")
        for X_batch, y_batch in test_loader:
            print("Train X_batch")
            print(X_batch.shape)
            print(X_batch[:,0])


if __name__ == "__main__":
    """train model with data from one file"""
    # model_training_one_file()

    """train model with data from two files"""
    model_training_two_files()

    """check if all the values are transfered"""
    # check_numbered()