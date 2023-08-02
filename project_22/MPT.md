#  Merkle Patricia Trie

### 介绍

**Merkle Patricia trie**是一种存储键值对的数据结构，就像[哈希表](https://en.wikipedia.org/wiki/Hash_table)。Merkle Patricia Trie 还是以太坊存储层的关键数据结构之一。除此之外，它还允许我们验证数据完整性和键值对的包含情况。

> 📘PMT 将树中相似值的节点分组在一起。这样，搜索“HELP”会引导您沿着与搜索“HELLO”相同的路径进行搜索 - 前三个字母是不同单词的共享条目。有利于空间效率和读/写效率。

通常有两种不同类型的数据：

- **永恒的**
  - 一旦交易发生，该记录将被永久密封
    - 这意味着一旦您在块的交易树中找到交易，您就可以一遍又一遍地返回相同的路径以检索相同的结果
- **短暂的**
  - 就以太坊而言，账户状态一直在变化！（即用户收到一些以太币，与合约交互等）
  - `nonce`, , ,`balance``storageRoot``codeHash`

永久数据（如挖掘的交易）和临时数据（如以太坊账户（余额、随机数等））应该*单独*存储。默克尔树非常适合永久数据。而MPT 非常适合短暂数据，以太坊有充足的供应。

与交易历史不同，以太坊账户状态需要经常更新。账户的余额和随机数经常改变，并且频繁插入新账户，频繁插入和删除存储中的密钥。

Merkle Patricia Tree 是以下各项的组合：

- Patricia Trie：一种高效的[Radix Trie](https://en.wikipedia.org/wiki/Radix_tree)，一种数据结构，其中“键”代表到达节点所必须采取的路径
- Merkle Tree：哈希树，其中每个节点的哈希值都是根据其子节点哈希值计算的。我们将从探索 Merkle Patricia Trees 的“Patricia Trie”部分开始，然后整合它们的“Merkle Tree”部分。

### Trie-字典树

trie 或前缀树是搜索树的一种，是一种用于从集合中查找特定键的树数据结构。这些键通常是字符串，节点之间的链接不是由整个键定义，而是由单个字符定义。为了访问键（恢复其值、更改它或删除它），将按照节点之间的链接（代表键中的每个字符）深度优先遍历 trie。

与二叉搜索树不同，特里树中的节点不存储其关联的键。相反，节点在 trie 中的位置定义了与其关联的键。这将每个键的值分布在整个数据结构中，并且意味着并非每个节点都必须具有关联的值。

正如字典树的名字一样**我们的核心其实是整理公共前缀**。Trie的思路其实是一样的，举例来说，下面是我们的4个账户：

| 地址     | 状态 |
| -------- | ---- |
| 0x811344 | 1ETH |
| 0x879337 | 2ETH |
| 0x8fd365 | 3ETH |
| 0x879397 | 4ETH |

将这些账户转换为字典树的结构储存：

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_22/P1.png)

### Patricia Trie

这是一种空间优化特里树，其中作为唯一子节点的每个节点都与其父节点合并。结果是每个内部节点的子节点数量最多为基数树的基数 r，其中 r 是正整数且为 2 的 x 次方，且 x ≥ 1。与常规树不同，边可以标记为元素序列以及单个元素。这使得基数树对于小集合（特别是当字符串很长时）和共享长前缀的字符串集合更加有效。

对于非常稀疏的路径，完全可以进一步压缩：

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_22/P2.png)

可见Patricia Trie对于稀疏的结构压缩效果很好，而实际当中以太坊中的地址是160bit，能表达的地址数为2^160,是一个非常庞大的天文数字，故整颗树也呈稀疏状，这是为何用Patricia Trie进行进一步压缩的原因。

基数树对于构建具有可以表示为字符串的键的关联数组非常有用。它们在 IP 路由领域有特殊的应用，其中包含大范围值（除了少数例外）的能力特别适合 IP 地址的分层组织。它们还用于信息检索中文本文档的倒排索引。

###  Merkle Patricia Trie

**根据对以上的研究，我认为Patricia Merkle 树是两种不同类型树的组合，保证安全性的同时提高了效率。（紧凑；Patricia 树，安全；Merkle 树）**

-Patricia Trie：剔除重复节点并压缩只有一个子节点的节点

-Merkle Tree：使验证交易变得更加容易，因为只需要发送根节点，并且一次可以验证一个分支。

Merkel-Patricia树的实现方式展示：

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_22/P3.png)

在这个图中右上角有4个`[key, value]`对，我们要存储这4对数据。`key`每个方框里是一个`nibble`，`next node`里面存着下一个节点的哈希值。比如说，从这四个路径中可以提取出公共路径`a7`，因此可以建立一个扩展节点A, [00 a7, hashB]，`a7`是一个偶数长度的扩展节点，前缀为00，`hashB`是下一个节点B的`hash`值；下一个`nibble`取值有1, 7, f，因此节点B为一个分支节点，其中index为1，7，f的位置保存下一个节点的`hash`值，`value`为空。

这个分支节点为：[ EMPTY, hashC, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, hashD, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, hashE, value]。
`hashC, hashD, hashE`为下一层节点的`hash`值……每一个节点和分支都可以如此分析。

这里既通过哈希保证了安全，如果我们想要加入或修改一个节点，也会集成Patricia Trie的优点只改动一小部分，不会像Merkel Tree一样动一大部分树。

### 安全性

相比于Trie-字典树，节点与节点之间的联系不再采用内存指针的方式，而是采用`hash`值的方式，比如上图中的第一个节点中，这个值的节点存储执行下一个节点的`hash`值，然后将这个`hash`值与实际节点对应关系存储在`[key, value]`的数据库中。当有人篡改子节点值时，也必须要修改父节点里的`hash`值，直到根节点，所以我们只需要验证根节点的`hash`值，就知道底层数据是否正确。

### 编码

MPT树的key值共有三种不同的编码方式，以满足不同场景的不同需求。

三种编码方式分别为：

Raw编码：原生的key编码，是MPT对外提供接口中使用的编码方式，当数据项被插入到树中时，Raw编码被转换成Hex编码；

 Hex编码：16进制扩展编码，用于对内存中树节点key进行编码，当树节点被持久化到数据库时，Hex编码被转换成HP编码；

 HP编码：16进制前缀编码，用于对数据库中树节点key进行编码，当树节点被加载到内存时，HP编码被转换成Hex编码；

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_22/P4.png)

### 以太坊中的 MPT

以太坊的 Merkle Patricia Trie 本质上是一个键值映射，它提供了以下标准方法：

```c
type Trie interface { 
  // 作为基本键值映射的方法
  Get(key []byte) ([]byte, bool) { 
  Put(key []byte, value []byte) 
  Del(key []byte, value [ ]字节）布尔值
}
```

而以太坊中实际情况还要复杂，数据还需要通过RLP编码。

1. State Trie(世界状态树)
   路径是`sha3(ethereumAddress)`，`value`是`rlp([nonce,balance,storageRoot,codeHash])`
2. Transactions Trie(交易树)
   路径是`rlp(transactionIndex)`，`value`是`rlp(transaction)`
3. Receipts Trie(交易收据树)
   路径是`rlp(transactionIndex)`，`value`是`rlp(transaction receipt)`





参考资料：

https://www.youtube.com/watch?v=TelOgcqjKG8&list=PLOGGvFbKWOAQJWncBsun4a1ln5ScTzJu2&index=18

https://medium.com/@kbaiiitmk/merkle-patricia-trie-in-ethereum-a-silhouette-c8d04155b490
