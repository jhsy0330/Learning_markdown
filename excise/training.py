# %%
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np

# %%
class PdData(Dataset):
    def __init__(self, DataFrame, feature_cols, label_col):
        self.data = DataFrame
        self.feature_cols = feature_cols
        self.label_col = label_col
        gender_map = {
            'male':0,
            'female':1
        }
        self.data['Sex'] = self.data['Sex'].map(gender_map)

    def __len__(self):
        return len(self.data)

    def __getitem__(self,idx):
        feature = torch.tensor(self.data.iloc[idx, 2:],dtype = torch.float32)
        label = torch.tensor(self.data.iloc[idx, 1], dtype = torch.float32)
        return feature, label

    def all_labels(self):
        return torch.tensor(self.data.iloc[:,1].values, dtype = torch.float32)
    
    def all_feature(self):
        return torch.tensor(
            self.data.iloc[:,2:].values,
            dtype = torch.float32
        )
    
    def showdata(self):
        print(self.data)


# %%
DataFrame = pd.read_csv('./dataset/titanic/train.csv')
DataFrame = DataFrame.drop(['Cabin','Embarked','Name','Ticket'],axis = 1)
DataFrame.dropna(axis = 0, how = 'any', inplace=True)
DataFrame.columns


# %%
csv_file = './dataset/titanic/train.csv'
label_col = 1
feature_cols = [2,3,4,5,6,7,8]

dataset = PdData(DataFrame, feature_cols=feature_cols, label_col= label_col)
features = dataset.all_feature()
labels = dataset.all_labels()

# %%
batch_size = 100
lr = 0.0001
epoch = 500

net = torch.nn.Sequential(torch.nn.Linear(6,4),torch.nn.Linear(4,2),torch.nn.Linear(2,1))
loss = torch.nn.BCEWithLogitsLoss()
optim = torch.optim.SGD(net.parameters(),lr)
iter = DataLoader(dataset, batch_size, shuffle=True)


for i in range(epoch):
    for x, y in iter:
        optim.zero_grad()
        y_hat = net(x)
        l = loss(y_hat, y.reshape(y_hat.shape))
        l.backward()
        optim.step()

    with torch.no_grad():
        out = net(features)
        l = loss(out, labels.reshape(out.shape))
        print(f'epoch:{i + 1}, loss:{float(l)}')


# %%
torch.save(net, "./titanic.pth")


