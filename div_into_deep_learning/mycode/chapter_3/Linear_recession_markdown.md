线性回归从零实现

```python
def synthetic_data(w, b, num):
    feature = torch.normal(0, 1, (num, len(w)))
    label = torch.matmul(feature, w) + b

    #添加噪声, 需要更小的学习率以抑制噪声导致的梯度震荡。 方差越大 学习率越小
    label += torch.normal(0, 0.01, label.shape)
    return feature, label

def data_iterator(batch_size, feature, label):
    num = len(feature)
    index = list(range(num))
    random.shuffle(index)

    for i in range(0, num, batch_size):
        j = torch.tensor(index[i:min(i + batch_size, num)])
        yield feature.index_select(0, j), label.index_select(0, j)

#真实值
true_w = torch.tensor([2, -3.4])
true_b = 4.2

#训练集
features, labels = synthetic_data(true_w, true_b, 1000)

#超参数
lr = 0.03
batch_size = 5
epoch = 5

#初始化参数  初始预测误差更大，需更小学习率避免参数更新步长过大。
w = torch.tensor(torch.normal(0, 0.01, true_w.shape), requires_grad = True)
b = torch.tensor(1, dtype = float, requires_grad = True)

for i in range(epoch):
    for x, y in data_iterator(batch_size, features, labels):
        y_hat = torch.matmul(x, w) + b
        loss = (y_hat - y) ** 2 / 2
        loss.sum().backward()

    		#更新参数 小批量梯度下降
    		# 每次更新参数在Batch后更新, 而不是在epoch后更新参数
        with torch.no_grad():
            w -= lr * w.grad / batch_size
            w.grad.zero_()
            b -= lr * b.grad / batch_size
            b.grad.zero_()
        
    with torch.no_grad():
        y_hat = torch.matmul(features , w) + b
        loss = (y_hat - labels) ** 2 / 2

    print(f"epoch:{i + 1},loss:{float(loss.mean()):f}")
    # print(f'epoch {epoch + 1}, loss {float(tl.mean()):f}')

```

## 遇到的问题: 

* 噪声方差越大 学习率越小
* 初始化参数的分布问题, 参数方差越大, 需更小学习率避免参数更新步长过大
* 参数在Batch后更新

## 需要解决的问题

```python
w = torch.tensor(torch.normal(0, 0.01, true_w.shape), requires_grad = True)
b = torch.tensor(1, dtype = float, requires_grad = True)

w = torch.tensor(torch.normal(0, 0.01, (2, 1)), requires_grad = True)
b = torch.tensor(1.0, requires_grad = True)
```

这两种初始化到底有哪里不一样, 结果最后会不同

```python
# 有效写法
torch.zeros((5,))      # 一维张量
torch.randn(5,)        # 一维张量

# 无效写法（会报错）
torch.zeros(5)         # 被解释为5个元素的列表参数
```



## 第二次遇到的问题: runtime error 连续求导出错

```python
def synthetic_data(true_w, true_b, size):
    x = torch.normal(0, 0.1, (size, len(true_w)))
    y = torch.matmul(x, w) + true_b
    y += torch.normal(0, 0.1, y.shape)
    return x, y

def data_iterator(batch_size, features, labels):
    size = len(features)
    index = list(range(size))
    random.shuffle(index)

    for i in range(0, size, batch_size):
        j = torch.tensor(index[i:min(i + batch_size, size)])
        yield features.index_select(0, j), labels.index_select(0, j)

def linear_recession(x, w, b):
    return torch.matmul(x, w) + b

def square_loss(y_hat, y):
    return (y_hat - y) ** 2 / 2

def sgd(batch_size, lr, params):
    with torch.no_grad():
        for para in params:
            para -= lr * para.grad / batch_size
            para.grad.zero_()

true_w = torch.tensor([3.2, -2.1])
true_b = torch.tensor([2.0])

features, labels = synthetic_data(true_w, true_b, 1000)

#hyper parameters
epoch = 3
batch_size = 10
lr = 0.03
net = linear_recession
loss = square_loss

#initial parameters
w = torch.tensor(torch.normal(0, 0.1, (2,)), requires_grad = True)
b = torch.tensor([1.0], requires_grad = True)

for i in range(epoch):
    for x, y in data_iterator(batch_size, features, labels):
        l = loss(net(x,w,b), y)
        l.sum().backward()

        sgd(batch_size, lr, [w, b])
    
    train_l = loss(net(features,w,b), y).mean()
    print(f"epoch:{i + 1}, loss:{float(train_l):f}")
```

出错的原因, 每个epoch输出测试数据没有**关闭计算图**

