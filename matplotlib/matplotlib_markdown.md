## Quick start

```python
date_list = [1,2,3,4]
stock1 = [4,8,2,6]
stock2 = [10,12,5,3]

plt.plot(date_list, stock1, "ro--", label = '股票代码:abd')
plt.plot(date_list, stock2, "b^--", label = '股票代码:def')

plt.title("折线图")
plt.xlabel("时间")
plt.ylabel("股价")

#设置xy坐标刻度
plt.xticks([1,2,3,4])
plt.yticks(np.arange(2,13))

plt.legend()

#辅助线网格
plt.grid()

plt.xlim(2.5, 4.5)
plt.ylim(1.5, 6.5)

plt.show()
```

