# SM2 with RFC6979
**SM2实现**  
本项目中有关sm2算法实现原理参考了  
https://blog.csdn.net/samsho2/article/details/80772228
https://blog.csdn.net/weixin_44885334/article/details/121994537
# 运行要求   
下载安装gmpy2库;  
将所有文件放入同一文件夹中;  
每个模块都有对应程序可以执行。  
# 基础操作  
在SM2.py和SM3.py文件中实现。SM3文件中是关于SM3国密算法的实现，由于本项目重心在于对SM2 with RFC6979的实现，所以对SM3算法不再赘述。仅介绍重要函数。  
*SM3加密函数*
SM3加密算法共分为四个步骤:消息填充、消息扩展、迭代压缩、输出密文  
![图片](https://user-images.githubusercontent.com/96277679/181663267-4502f523-0269-4ea5-9047-4f35088543fa.png)  
**椭圆曲线上的基本运算**
*椭圆曲线上的点加*  
![图片](https://user-images.githubusercontent.com/96277679/181663456-7317bbce-d2e8-4f80-916f-f3735eb8e48c.png)  
*椭圆曲线上的点乘*  
![图片](https://user-images.githubusercontent.com/96277679/181663551-e791ef40-50ff-4ffe-844c-4565fed95acd.png)  
# SM2加解密（SM2.py文件中实现）   
**原理**  
*密钥生成*  
![图片](https://user-images.githubusercontent.com/96277679/181663773-e724f029-05f4-4294-b77f-c7326038e7a9.png)  
*加密*  
![图片](https://user-images.githubusercontent.com/96277679/181663684-59799d7a-a49e-4fee-84cc-5d718fd1dc51.png)  
*解密*  
![图片](https://user-images.githubusercontent.com/96277679/181663730-f66941b4-7054-4f62-a339-440be41def3d.png)  
**算法实现**  
由SM2算法原理实现的SM2加解密操作,  
加密  
![图片](https://user-images.githubusercontent.com/96277679/181663864-57da9680-529c-4cad-947e-b2aa3500542e.png)  
解密  
![图片](https://user-images.githubusercontent.com/96277679/181663970-50e0b464-390e-476e-a880-010c6973fc8d.png)  
**运行结果**  
![图片](https://user-images.githubusercontent.com/96277679/181664793-f6833bdc-2753-4f46-bef0-9156b7c3ab04.png)  
选取SM2推荐曲线参数进行实例运行。  
![图片](https://user-images.githubusercontent.com/96277679/181664105-a0ffbde2-7c0f-413e-bdd8-1ba98250f0cc.png)  
对明文"sample"进行加解密，结果如下   
![图片](https://user-images.githubusercontent.com/96277679/181664280-eb075aee-a9f5-43aa-84c1-6747ea702f06.png)  
解密结果与明文相同，加解密实现成功。  
# 数字签名（签名.py文件中实现）  
**原理**  
*签名*   
签名者用户A的密钥对包括其私钥dA和公钥PA=[dA]G= (xA,yA)  
1  签名者用户A具有长度为entlenA比特的可辨别标识IDA，  
2  ENTLA是由整数entlenA转换而成的两个字节  
3  ZA=H256(ENTLA || IDA || a || b || xG || yG|| xA || yA)。  
4  待签名的消息为M，  
5  数字签名(r,s)  
![图片](https://user-images.githubusercontent.com/96277679/181664647-f0952a6b-edd8-4278-8ef1-c127ef47d679.png)    
*验证*  
1  签名者用户A的密钥对包括其私钥dA和公钥PA=[dA]G= (xA,yA)  
2  签名者用户A具有长度为entlenA比特的可辨别标识IDA，  
3  ENTLA是由整数entlenA转换而成的两个字节    
4  ZA=H256(ENTLA || IDA || a || b || xG || yG|| xA || yA)。  
5  消息为M，数字签名(r,s)  
![图片](https://user-images.githubusercontent.com/96277679/181664717-8d1a96f0-b682-4234-9c71-047d27dffb2f.png)  
实现签名的关键  
(x′1; y′1)  
= [s′]G + [t]PA  
= [s′]G + [s′] PA + [r′] PA  
= [s′]G +[s′][dA] G +[r′·dA] G  
= [(1+ dA)×s′] G+[r′·dA] G  
= [k − r · dA) ] G+[r′·dA] G  
= [k] G   
= ( x1, y1 )  
**算法实现**   
*预处理*  
根据ID计算摘要  
![图片](https://user-images.githubusercontent.com/96277679/181666893-ba29e32f-02cc-48c2-b3e3-86b755cf2d01.png)  
在这里使用默认ID值    
*签名*  
![图片](https://user-images.githubusercontent.com/96277679/181666955-0fa48ab2-a6ba-4902-9117-5e558ce71c5d.png)    
*验证*    
![图片](https://user-images.githubusercontent.com/96277679/181667012-5198c14b-b06b-4bca-93dd-929b17b8be81.png)  
**运行结果**  
选取SM2推荐曲线参数进行实例运行。    
![图片](https://user-images.githubusercontent.com/96277679/181667269-7e8e1357-81bd-4b67-9c3f-b4a9145ed9c7.png)  
对明文消息"sample"进行签名和验证操作，运行结果如下  
![图片](https://user-images.githubusercontent.com/96277679/181667638-181c5729-ca0b-4b9a-9681-06f49f28f023.png)  
成功实现验证 
# 密钥交换（密钥交换.py文件中实现） 
**原理**  
*计算摘要*
![图片](https://user-images.githubusercontent.com/96277679/181668086-ce5274f0-4fc7-487c-b293-08f3e2516a57.png)  
生成交换数据  
![图片](https://user-images.githubusercontent.com/96277679/181668299-100c24b8-8d0f-47be-87c9-f8839a1712a9.png)  
生成协商密钥  
![图片](https://user-images.githubusercontent.com/96277679/181668437-d7a854ac-a716-4526-8183-2015afccb9f3.png)  
协商密钥确认  
![图片](https://user-images.githubusercontent.com/96277679/181668491-97b47066-1f12-402f-b607-ae7be7ce46bd.png)  
本次算法以用户A向用户B发起密钥交换为例,算法原理为  
用户A执行  
![图片](https://user-images.githubusercontent.com/96277679/181777063-2cde112e-e731-491e-bc8a-43d21dd8f8fd.png)  
用户B执行  
![图片](https://user-images.githubusercontent.com/96277679/181777131-73ddd6b0-7a7e-4e19-9c82-af322732a6c3.png)  
用户A执行  
![图片](https://user-images.githubusercontent.com/96277679/181777183-d2dcb54c-cb49-4fce-9ab6-41fd0fcfe5af.png)  
用户B执行  
![图片](https://user-images.githubusercontent.com/96277679/181777248-9b91f6b8-5a2a-4d7d-8bd8-a0230393c0ac.png)  
**算法实现**  
用户A生成交换数据  
![图片](https://user-images.githubusercontent.com/96277679/181778490-2bae7e28-50d6-47a7-8353-5cda9f54b53a.png)    
用户B由交换数据生成交换密钥  
![图片](https://user-images.githubusercontent.com/96277679/181778548-4dc08928-7ef7-4e4c-86d9-74724a507a4f.png)  
用户A生成交换密钥  
![图片](https://user-images.githubusercontent.com/96277679/181778619-e52dc3e8-2055-44a1-99c5-e5621e4e7626.png)    
用户B进行验证  
![图片](https://user-images.githubusercontent.com/96277679/181778644-4321a74a-1792-408f-a58a-e1f164bfc9b9.png)    
**运行结果**  
选取给定的标准参数，同时设置用户A，B的ID为不同的默认ID  
![图片](https://user-images.githubusercontent.com/96277679/181669650-6b32bac8-b148-4e37-968f-064cad847b31.png)  
经过生成，可以以得到用户A和用户B的协商密钥，且经过验证，协商密钥通过验证。  
成功实现密钥交换。  



























