# SM2 Implement ECMH 
*实现原理*    
ECMH体系下的SM2加密实现，基本原理与SM2加密实现原理相同，唯一区别点在于将集合里面的元素看作椭圆曲线上的点，以此对其实现加密（哈希）。   
*运行前提*  
下载安装gmssl库（pip install gmssl）  
*基本操作*  
二次剩余的计算和判断  
由勒让德符号的定义实现，二次剩余的计算  
![图片](https://user-images.githubusercontent.com/96277679/181738615-0a308bcc-4d8b-477d-9552-e0a349ac143e.png)  
Tonelli-Shanks算法用于求二次剩余  
在执行这个算法之前需要实现对二次（非）剩余的判断（可以使用欧拉准则）  
![图片](https://user-images.githubusercontent.com/96277679/181772590-5d6567df-99a8-4315-b6ce-a56b9f84a131.png)  
Tonelli-Shanks算法步骤如下，  
![图片](https://user-images.githubusercontent.com/96277679/181772934-b3e937ae-8e3c-4fe6-8a7f-c5ceca1632ca.png)   
![图片](https://user-images.githubusercontent.com/96277679/181772978-c3bcaa38-76a2-4984-8379-0821fca8f994.png)  
具体实现如下图,  
![图片](https://user-images.githubusercontent.com/96277679/181738662-b7097434-73a1-4b0a-8d62-7f406a4e8519.png)  
下图为SM2加密实现过程中的必要函数  
主要作用是实现椭圆曲线上两点相加和k倍点乘的运算  
假设椭圆曲线上有三个点P,Q,R在同一直线上，椭圆曲线的加法定义为P+Q+R=O(O是加法中的单位元，类似于实数加法中的0)，其几何描述为一条直线上的三个点的和为O，即 P + Q = O - R。
椭圆曲线多倍点记做P =[k]Q，表示k个Q点相加的结果为P。  
代码实现如下图，  
椭圆曲线两点相加算法  
![图片](https://user-images.githubusercontent.com/96277679/181738742-abbbbba0-1b78-410e-8581-0229b11a698f.png)  
椭圆曲线k倍积算法  
![图片](https://user-images.githubusercontent.com/96277679/181738914-ab279f72-e5f7-46ca-a53a-302b76dc60d2.png)  
**关键实现**  
以下为SM2算法的总体实现，通过调用上述基本操作，实现对ECMH体系下的SM2加密操作。  
SM2公私钥是用户通过产生一个随机数，将该随机数作为私钥，同时利用私钥和已知椭圆曲线上一点（给定参数），生成私钥对应的公钥。  
公私钥生成算法  
![图片](https://user-images.githubusercontent.com/96277679/181739016-9f164abe-5245-4815-8f61-deca0b1f36cc.png)  
加密算法与SM2 with RFC6979加密算法相同，这里是通过循环调用集合里面的元素实现ECMH体系下SM2的加密操作。  
以集合元素作为曲线点进行哈希  
![图片](https://user-images.githubusercontent.com/96277679/181739209-8e3fcb5e-38cf-4bcb-8c58-988e09ca2210.png)  
# 运行结果  
参数选取如下（给定标准参数）  
![图片](https://user-images.githubusercontent.com/96277679/181740236-c06d68be-02dd-4cc4-9274-c9aaf2bdbf02.png)  
哈希结果  
![图片](https://user-images.githubusercontent.com/96277679/181740348-61445617-9a79-416f-b737-bb0d1ba1ab79.png)  
可以看到成功实现哈希（加密）。  
# 参考文献  
Tonelli-Shanks算法：https://blog.csdn.net/qq_51999772/article/details/122642868  
SM2算法原理：https://blog.csdn.net/shujiezhang/article/details/6784957  
https://blog.csdn.net/chexlong/article/details/103293311  








