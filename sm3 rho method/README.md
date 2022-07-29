 # sm3 rho method  
此项目为对sm3算法运用rho method寻找一个循环。  
## 代码说明：  
代码前面的部分为sm3的实现，代码的说明见sm3 birthday attack中。  
不同的是后面的攻击函数，代码如下:  
![OH)WRRBKLOO9BMO$56@X9J7](https://user-images.githubusercontent.com/96007188/181743201-37e4dfcb-7401-4dd3-97fa-26b8fd022de1.png)  
设置两个变量x1，x2，初始时将一个随机数赋值给x1，然后让x2=sm3(x1)，并进入循环：  
注意为了让循环能够顺利形成又不超出计算能力，下面的每个sm3运算结果都只取前n位。
循环中，让x1=sm3(x1), x2=sm3(sm3(x2))然后比较二者是否相等，若不相等，进入下一个循环。若相等，则说明一定存在一个循环，然后对x1，依次计算sm(x1)，sm(sm(x1)),sm(sm(sm(x1)))...直到出现循环为止。并将循环print出来。  

