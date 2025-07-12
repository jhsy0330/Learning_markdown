## Softmax regression

Requirements(概率公理化)

- Probits sum up to 1
- Each output probabilties is even nonnegative

#### why using exponential function

This does indeed satisfy the requirement that the conditional class probability increases with increasing O

it is monotonic, and all probabilities are nonnegative
$$
\hat{\mathbf{y}} = \mathrm{softmax}(\mathbf{o}) \quad \textrm{where}\quad \hat{y}_i = \frac{\exp(o_i)}{\sum_j \exp(o_j)}.
$$


the softmax operation preserves the ordering among its arguments, we do not need to compute the softmax to determine which class has been assigned the highest probability.
$$
\operatorname*{argmax}_j \hat y_j = \operatorname*{argmax}_j o_j.
$$
疑问: 指数函数不是线性, , 一阶导递增, 为什么不能用一个线性的函数 简单加起来的方法去实现公理化? 



### Vectorization

### Loss Function