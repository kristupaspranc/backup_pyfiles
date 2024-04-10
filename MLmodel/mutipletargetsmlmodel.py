import torch
from torch import nn
from torch.nn import functional as F
import torch.utils.data as Data
from torch import optim
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm
     

housing = fetch_california_housing()

X, y = housing.data, housing.target

y = np.column_stack((y, X[:,1]))
X = np.delete(X,1,1)

n_samples, n_features = X.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)


class DataMaker(Data.Dataset):
    def __init__(self, X, y):
        self.targets = X.astype(np.float32)
        self.labels = y.astype(np.float32)

    def __getitem__(self, i):
        return self.targets[i, :], self.labels[i, :]

    def __len__(self):
        return len(self.targets)
    

class Model(nn.Module):
    def __init__(self, n_features, hiddenA, hiddenB):
        super(Model, self).__init__()
        self.linearA = nn.Linear(n_features, hiddenA)
        self.linearB = nn.Linear(hiddenA, hiddenB)
        self.linearC = nn.Linear(hiddenB, 2)

    def forward(self, x):
        yA = F.relu(self.linearA(x))
        yB = F.relu(self.linearB(yA))
        return self.linearC(yB)


torch.manual_seed(1)

train_set = DataMaker(X_train, y_train)
test_set = DataMaker(X_test, y_test)
     
bs = 25
train_loader = Data.DataLoader(train_set, batch_size=bs, shuffle=True)
test_loader = Data.DataLoader(test_set, batch_size=bs, shuffle=True)

net = Model(n_features, 100, 50)


print(net)


# criterion = nn.MSELoss(size_average=False)
# optimizer = optim.Adam(net.parameters(), lr=0.01)

# n_epochs = 50
# all_losses = []
# for epoch in range(n_epochs):
#     progress_bar = tqdm(train_loader, leave=False)
#     losses = []
#     total = 0
#     for inputs, target in progress_bar:
#         optimizer.zero_grad()
#         y_pred = net(inputs)
#         loss = criterion(y_pred, torch.unsqueeze(target,dim=1))

#         loss.backward()
        
#         optimizer.step()
        
#         progress_bar.set_description(f'Loss: {loss.item():.3f}')
        
#         losses.append(loss.item())
#         total += 1

#     epoch_loss = sum(losses) / total
#     all_losses.append(epoch_loss)
                
#     mess = f"Epoch #{epoch+1}\tLoss: {all_losses[-1]:.3f}"
#     #tqdm.tqdm.write(mess)
