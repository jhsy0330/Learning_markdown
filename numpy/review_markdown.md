### 一、数组创建与初始化

#### 1. **基础创建**

```python
np.array([[1,2,3],[4,5,6]])  # 从列表创建
np.zeros((3,3))              # 全零数组
np.ones((2,4), dtype=int)    # 全一数组
np.empty((2,3))              # 未初始化数组（内存残留值）
np.full((3,3), 5)            # 全为5的数组
```

#### 2. **序列生成**

```python
np.arange(0, 10, 2)          # [0,2,4,6,8]（类似Python的range）
np.linspace(1, 5, 5)         # 等差数列 [1,2,3,4,5]
np.logspace(0, 2, 3)         # 等比数列 [1,10,100]
```

#### 3. **随机数生成**

```python
np.random.seed(0)            # 固定随机种子
np.random.rand(2,3)          # [0,1)均匀分布
np.random.randn(2,3)         # 标准正态分布
np.random.randint(0, 10, (2,3))  # 随机整数
```

------

### 二、数组属性与操作

#### 1. **核心属性**

| 属性        | 说明           | 示例                  |
| ----------- | -------------- | --------------------- |
| `.ndim`     | 维度数         | `arr.ndim → 2`        |
| `.shape`    | 形状（元组）   | `arr.shape → (3,4)`   |
| `.size`     | 元素总数       | `arr.size → 12`       |
| `.dtype`    | 元素类型       | `arr.dtype → float64` |
| `.itemsize` | 单个元素字节数 | `arr.itemsize → 8`    |

#### 2. **形状操作**

```python
arr.reshape(2,3)             # 改变形状（不修改数据）
arr.resize((3,3))            # 直接修改原数组形状
arr.ravel()                  # 展平为一维（返回视图）
arr.flatten()                # 展平为一维（返回副本）
```

#### 3. **数组拼接与分割**

```python
np.concatenate([a,b], axis=0)  # 沿轴拼接
np.vstack((a,b))             # 垂直堆叠（行方向）
np.hstack((a,b))             # 水平堆叠（列方向）
np.split(arr, indices, axis) # 按位置分割
```

------

### 三、数学与统计函数

#### 1. **数学运算**

```python
np.add(a, b)                 # 逐元素加法
np.subtract(a, b)            # 逐元素减法
np.multiply(a, b)            # 逐元素乘法
np.divide(a, b)              # 逐元素除法
np.power(a, 2)               # 幂运算（等价于a**2）
np.sqrt(a)                   # 平方根（非负数）
np.exp(a)                    # 指数函数（e^a）
np.log(a)                    # 自然对数
```

#### 2. **统计计算**

```python
np.sum(a, axis=0)            # 沿轴求和
np.mean(a)                   # 平均值
np.median(a)                 # 中位数
np.std(a, ddof=1)            # 标准差（样本标准差ddof=1）
np.var(a, ddof=1)            # 方差（样本方差）
np.min(a), np.max(a)         # 最小/最大值
np.argmin(a), np.argmax(a)   # 最小/最大值索引
np.percentile(a, 75)         # 75%分位数
```

#### 3. **线性代数**

```python
np.dot(a, b)                 # 矩阵乘法
np.linalg.inv(a)             # 矩阵求逆
np.linalg.det(a)             # 行列式
np.linalg.eig(a)             # 特征值与特征向量
```

------

### 四、索引与切片

#### 1. **基础索引**

```python
arr[0, 1]                    # 获取第0行第1列元素
arr[1:3, 2:4]                # 切片（行1-2，列2-3）
arr[-1, :]                   # 最后一行所有列
```

#### 2. **高级索引**

```python
arr[[0,2], [1,3]]            # 布尔索引（取(0,1)和(2,3)）
arr[arr > 5]                 # 布尔掩码筛选
np.where(arr > 5, 1, 0)      # 条件替换
```

#### 3. **花式索引**

```python
rows = np.array([0,1])
cols = np.array([2,3])
arr[rows, cols]              # 取(0,2)和(1,3)位置的值
```

------

### 五、广播机制与运算优化

#### 1. **广播规则**

- **维度对齐**：从右向左扩展维度，缺失的维度视为1。

  ```python
  a = np.array([[1,2,3],[4,5,6]])  # 形状 (2,3)
  b = np.array([10,20,30])         # 形状 (3,)
  a + b → [[11,22,33],[14,25,36]]  # b广播为(2,3)
  ```

#### 2. **原地操作**

```python
np.add(a, b, out=a)          # 直接修改a，节省内存
```

------

### 六、文件操作与数据交互

```python
np.save('data.npy', arr)     # 保存为二进制文件
np.load('data.npy')          # 加载二进制文件
np.savetxt('data.txt', arr)  # 保存为文本（默认空格分隔）
np.loadtxt('data.txt')       # 加载文本文件
```

------

### 七、实用技巧

#### 1. **类型转换**

```python
arr.astype(np.float32)       # 转换数据类型
```

#### 2. **唯一值与排序**

```python
np.unique(arr)               # 去重并排序
np.sort(arr, axis=0)         # 沿轴排序
```

#### 3. **随机操作**

```python
np.random.permutation(arr)   # 随机排列
np.random.shuffle(arr)       # 原地打乱
```

------

### 八、性能优化建议

1. **避免循环**：尽量使用向量化操作（如 `np.vectorize`）。
2. **预分配内存**：使用 `np.empty` 或 `np.zeros` 预分配空间。
3. **使用视图**：`ravel()` 和 `flatten()` 返回视图而非副本。
4. **并行计算**：利用 `dtype=np.float32` 减少内存占用。

------

### 九、常见错误与调试

- **维度不匹配**：检查 `shape` 属性，使用 `reshape` 或 `newaxis` 调整。
- **广播失败**：确保维度对齐，必要时手动扩展维度。
- **数据类型冲突**：使用 `astype()` 统一数据类型。

------