# Find a key with hash value "sdu_cst_20220610" under a message composed of your name followed by your student ID。
代码参考说明：
https://github.com/cmuratori

该代码的目标是Find a key with hash value "sdu_cst_20220610" under a message composed of your name followed by your student ID。
     首先，我们先明确meow_hash代码，通过给定一个message和1024比特的key，可以得到128比特的hash value。具体过程为：将key分为8组，每组128比特，将message按32字节划分为组，最后不足32字节之处填充，依次将mi与key进行一系列操作，使message与key充分混淆，输出结果再进行一系列运算，最后将8组合为一组，输出128比特的hash value。
     ![image](https://user-images.githubusercontent.com/71961291/181770476-700aa520-de68-4dfd-b589-019f37c55a66.png)

     代码过程可逆，所以已知message和hash value，通过对一些未知数的随机赋值，可以得到key。所以针对该project，我们将源代码头文件对应部分MeowHash函数进行逆运算，输出key值。
     运行结果：
 
 
 
 
 ![image](https://user-images.githubusercontent.com/71961291/181772658-d42b16a6-03db-4e78-abf4-58d235cd1da0.png)



   




