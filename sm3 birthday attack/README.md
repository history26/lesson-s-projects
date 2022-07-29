## sm3 birthday attack
此项目为sm3算法的naive birthday attack的实现。其中也包括sm3算法本体的实现。  
sm3结构设计有参考https://blog.csdn.net/weixin_42369053/article/details/118303945?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-118303945-blog-121637732.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-118303945-blog-121637732.pc_relevant_default&utm_relevant_index=2
#函数中代码说明：  
![VU OGA`A7F0MSZ4M0ZV6`TX](https://user-images.githubusercontent.com/96007188/181716475-bac63304-5619-40a7-9cb4-2ad3c5444830.png)  
此函数为将整数转化为指定位数的二进制数的函数，方便了用户直接输入和取随机数作为输入。  
![4WI8XY2~4$U6K~F}43SFM`3](https://user-images.githubusercontent.com/96007188/181718745-e651fee6-8341-45f3-bdc5-fd741e9d458a.png)  
将整数转化为二进制并左移s位的函数。  
![6B9Z{PKOIKM41$$(7PNV@Q8](https://user-images.githubusercontent.com/96007188/181718999-2618c1d3-aa78-4588-8a9f-7fd95b5825a1.png)    
消息填充的函数，首先向消息最前面填充0至4的整数倍，然后在消息后面先填充一个1，然后再填充数个0，使得消息的总长度模512的余数为448，剩下的64位用于表示消息的长度。  
这样就按照指定的格式将消息调整到512的整数倍，以便于后面的分块。  
![image](https://user-images.githubusercontent.com/96007188/181721669-54a2b106-6f04-42bf-89eb-18d7053a0e38.png)  
消息扩展函数。按sm3算法要求生成132个消息字，其中前68个消息一组，后64个消息一组。  
![image](https://user-images.githubusercontent.com/96007188/181722978-74062969-50a5-42d8-8686-7c9918c6ff9a.png)  
sm3轮函数中内置的函数Tj,FF,GG,逻辑较为简单，GG因为包含了二进制取反部分而较为麻烦。  
![0T%FRG8M@O}}F)}@`OQBO F](https://user-images.githubusercontent.com/96007188/181723432-910c6aa2-5a15-449e-8174-0d00baaa93a5.png)  
压缩函数，计算逻辑如下图：  
![image](https://user-images.githubusercontent.com/96007188/181723893-d5e2676a-2220-4f2b-ab84-095eef909bda.png)  

