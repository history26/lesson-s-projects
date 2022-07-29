# SM2 Implement ECMH  
*实现原理*    
ECMH体系下的SM2加密实现，基本原理与SM2加密实现原理相同，唯一区别点在于将集合里面的元素看作椭圆曲线上的点，以此对其实现加密（哈希）。   
*运行前提*  
下载安装gmssl库（pip install gmssl）  
*基本操作*  
二次剩余的计算和判断  
![图片](https://user-images.githubusercontent.com/96277679/181738615-0a308bcc-4d8b-477d-9552-e0a349ac143e.png)  
![图片](https://user-images.githubusercontent.com/96277679/181738662-b7097434-73a1-4b0a-8d62-7f406a4e8519.png)  
椭圆曲线两点相加算法  
![图片](https://user-images.githubusercontent.com/96277679/181738742-abbbbba0-1b78-410e-8581-0229b11a698f.png)  
椭圆曲线k倍积算法  
![图片](https://user-images.githubusercontent.com/96277679/181738914-ab279f72-e5f7-46ca-a53a-302b76dc60d2.png)  
**关键实现**  
公私钥生成算法  
![图片](https://user-images.githubusercontent.com/96277679/181739016-9f164abe-5245-4815-8f61-deca0b1f36cc.png)  
以集合元素作为曲线点进行哈希  
![图片](https://user-images.githubusercontent.com/96277679/181739209-8e3fcb5e-38cf-4bcb-8c58-988e09ca2210.png)  
#运行结果  
参数选取如下（给定标准参数）  
![图片](https://user-images.githubusercontent.com/96277679/181740236-c06d68be-02dd-4cc4-9274-c9aaf2bdbf02.png)  
哈希结果  
![图片](https://user-images.githubusercontent.com/96277679/181740348-61445617-9a79-416f-b737-bb0d1ba1ab79.png)  








