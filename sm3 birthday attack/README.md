# sm3 birthday attack
此项目为sm3算法的naive birthday attack的实现。其中也包括sm3算法本体的实现。
函数中代码说明：
![VU OGA`A7F0MSZ4M0ZV6`TX](https://user-images.githubusercontent.com/96007188/181716475-bac63304-5619-40a7-9cb4-2ad3c5444830.png)
此函数为将整数转化为指定位数的二进制数的函数，方便了用户直接输入和取随机数作为输入。
![4WI8XY2~4$U6K~F}43SFM`3](https://user-images.githubusercontent.com/96007188/181718745-e651fee6-8341-45f3-bdc5-fd741e9d458a.png)
将整数转化为二进制并左移s位的函数。
![6B9Z{PKOIKM41$$(7PNV@Q8](https://user-images.githubusercontent.com/96007188/181718999-2618c1d3-aa78-4588-8a9f-7fd95b5825a1.png)
消息填充的函数，首先向消息最前面填充0至4的整数倍，然后在消息后面先填充一个1，然后再填充数个0，使得消息的总长度模512的余数为448，剩下的64位用于表示消息的长度。
这样就按照指定的格式将消息调整到512的整数倍，以便于后面的分块。
