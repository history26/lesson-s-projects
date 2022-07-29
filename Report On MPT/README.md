# MPT
本项目中有关Merkle Patricia trie的实现代码引用于https://github.com/chacaldev/merkle-patricia-trie  
**Merkle Tree**  
Merkle Tree是一种数据结构，用于验证计算机只见那存储和传输数据的一致性，可以节省存储和网络资源。Merkle trees同时也是区块链的基本组成部分。  
Merkle tree是区块链的重要数据结构，其作用十四快速归纳和校验区块数据的存在性和完整性。一般意义上来说是，通过哈希大量聚集数据“块的一种方式”，其依赖于将这些数据“块”分成较小单位的数据块，每一个bucket块仅包含几个数据“块”，然后取每个bucket单位数据块再次进行哈希，之后不断重复该步骤，直到剩余的哈希总数成1.（百度百科中关于Merkle tree作用的介绍）[1]  
*Merkle tree构成原理*  
Merkle tree通常包含区块提的底层（交易）数据库，区块头的根哈希值（Merkle根）以及所有沿底层区块数据到根哈希的分支。梅克尔树运算过程一般是将区块体的数据进行分组哈希， 并将生成的新哈希值插入到梅克尔树中，如此递归直到只剩最后一个根哈希值并记为区块头的 Merkle根。比特币采用的二叉Merkle tree就是最常见一种Merkle tree，其中美国哈希节点总是包含两个相邻的数据块或哈希值。特点如下：  
1.Merkle tree是一种树，大多数是二叉树，也可以多叉树，无论是几叉树，他们都具有树结构的所有特点；  
2.Merkle tree的叶子节点的value是数据集合的单位数据或者单位数据的hash；  
3.非叶子节点的value根据其下的所有叶子节点值，按照hash算法计算得出的；  
*优点*  
Merkle tree有许多优点，首先极大地提高了区块链的运行效率和可扩展性，使得区块头只需包含根哈希值而不必封装所有底层数据,，这使得哈希运算可以高效地运行在智能手机甚至物联网设备上；其次是梅克尔树可支持 “简化支付验证” 协议, 即在不运行完整区块链网络节点的情况下，也能够对（交易）数据进行检验。  
[1]  
实现图解如下，  
![图片](https://user-images.githubusercontent.com/96277679/180729133-05f3ecb4-0f24-49d3-a744-8334ecde7be0.png)  
*在比特币网络中区块链的实际应用案例*  
假设Alice向Bob发送5个比特币，通过使用Merkle tree，除了要对各个节点之间的数据一致性进行验证之外，还可以对一个交易是否属于某个区块进行快速验证。轻节点只需要下载很少的数据就可以验证交易的有效性。  
![图片](https://user-images.githubusercontent.com/96277679/180731540-99bea376-2df6-4cb8-a170-331a8fab83b2.png)  
如上图，要验证交易T（D）在某个区块之中，需要依赖的数据仅仅是HC,HAB,HEFGH和根节点（HABCDEFGH）。 [2] 
**Merkle Patricia Trie**  
*Trie*  
Patria Trie也是一种树形数据结构（简称为Trie，来源于英文单词retrieve）。使用场景包括:(1)搜索引擎的自动补全功能；(2)IP路由等；  
Trie的特点是某个节点的key是从根节点到该节点的路径，即不同key有相同的前缀时，他们共享前缀所对应的路径。  
以此可以实现对前缀相同数据的快速查找，内存开销较少。  [2]
下图为Trie实现的一个实例，  
![图片](https://user-images.githubusercontent.com/96277679/180735487-c0afbb4d-5f1a-4c5e-9719-84ab1e9e5203.png)  
![图片](https://user-images.githubusercontent.com/96277679/180734661-26035005-89ad-4d0a-af66-f07aefd78b0d.png)  
*MPT简介*  
Merkle Patricia Trie（简称MPT），是在Trie的基础上，给每个节点计算一个哈希值，在Substrate中，该值通过对节点内容进行Blake2运算取得，用来索引数据库和计算根节点。即MPT用到两种key的类型。  
第一种是Trie路径对应的key，由runtime模块的存储单元决定。使用Substrate开发的应用链，它所拥有的各个模块的存储单元会通过交易进行修改，成为链上状态。每个存储单元的状态都是通过键值对以trie节点的形式进行索引或者保存的，这里键值对的value是原始数据（如数值、布尔）的SCALE编码结果，并作为MPT节点内容的一部分进行保存；
key是模块、存储单元等哈希组合，且和存储数据紧密相关。
单值类型（即Storage Value），它的key是Twox128(module_prefix) + Twox128(storage_prefix)；  
简单映射类型（即map），可以表示一系列的键值数据，它的存储位置和map中的键相关，即Twox128(module_prefix) + Twox128(storage_prefix) + hasher(encode(map_key))；  
链接映射类型（即linked_map），和map类似，key是Twox128(module_prefix) + Twox128(storage_prefix) + hasher(encode(map_key))；它的head存储在Twox128(module) + Twox128("HeadOf" + storage_prefix)；  
双键映射类型（即double_map），key是twox128(module_prefix)+twox128(storage_prefix)+hasher1(encode(map_key1))+hasher2(encode(map_key2))。  

另一种是数据库存储和计算merkle root使用的key，可以通过对节点内容进行哈希运算得到，在键值数据库（即RocksDB，和LevelDB相比，RocksDB有更多的性能优化和特性）中索引相应的trie节点。Trie节点主要有三类，即叶子节点（Leaf）、有值分支节点（BranchWithValue）和无值分支节点（BranchNoValue）；有一个特例，当trie本身为空的时候存在唯一的空节点（Empty）。根据类型不同，trie节点存储内容有稍许不同，通常会包含header、trie路径的部分key、children节点以及value。[2]
Trie路径的key和value，  
![图片](https://user-images.githubusercontent.com/96277679/180741471-71f31307-3241-40cc-97c8-bd877d5deda1.png)  
将数据转换成trie结构，  
![图片](https://user-images.githubusercontent.com/96277679/180741603-bffac9ca-d72b-4b12-996d-9a552096c4db.png)  
添加每个节点的哈希值，（哈希算法使用Blake2）  
![图片](https://user-images.githubusercontent.com/96277679/180741687-17b02410-fb38-428d-b31e-7a73cff0971c.png)  
数据库的存储大致如下图所示，  
![图片](https://user-images.githubusercontent.com/96277679/180741924-f9ba9708-9964-45d4-9814-1c37b0a42c80.png)  
可以通过一个简化案例对MPT有更深层次的理解，  
![图片](https://user-images.githubusercontent.com/96277679/180737778-0a403664-a7e8-439c-a075-7f5133118908.png)  
右上角显示的是四个账户地址及其余额（简化版的世界状态）:
![图片](https://user-images.githubusercontent.com/96277679/180737951-de13c738-03b3-46ce-9e39-81ddd1909d6c.png)  
以地址作为 key，以余额作为要存储的 value，生成了一个 Patricia Trie（具体生成的细节后面会描述）；然后自底向上的遍历过程中，不断向上生成 hash，最后得到根节点的 root hash（体现了 Merkle Tree 的特点），即获得了 state root。   
生成的Patricia Trie中可以看到三种类型的节点：  
Leaf（叶节点）：没有子节点，表示为 [key, value] 键值对，从 root 到此节点的 key 的累加值表示完整 key 值（完整地址），value 用于存储上面账户地址中实际的余额  
Extertion（扩展节点）：拥有一个分支节点作为子节点，表示为 [key, value] 键值对，key 值表示至少有两个 key 的分支共享从 root 到此节点的 key 的累加值（地址的前一部分），只用于指向分支节点，不存储实际值  
Branch（分支节点）：有 17 个子项的数据结构，其中前 16 项对应 16 进制的 0-F，表示从 root 到此节点的 key 的累加值产生了分叉，分叉值恰好分别对应 0-F 的匹配项。若恰好有一个 key 值结束于此，则第 17 项存储对应的 value  
通过这些节点类型，可以将上面四个账户的地址和余额进行表示。[3]  

**总结**  
Merkle tree作为区块链的基本组成部分。虽然没有Merkle Tree的区块链也是可以的，但是会对可扩展性方面产生挑战。正因为有了Merkle tree以太坊节点才可以建立在计算机、笔记本、智能手机、甚至是那些由Slock.it生产的物联网设备。  
**参考资料**
[1]https://baike.baidu.com/item/%E6%A2%85%E5%85%8B%E5%B0%94%E6%A0%91/22456281?fr=aladdin  
[2]https://blog.csdn.net/shangsongwww/article/details/119272573  
[3]https://www.jianshu.com/p/5e2483413537?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation  





